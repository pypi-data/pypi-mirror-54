from typing import List, Union, Optional
from uuid import UUID
from pyarrow import csv, Table

from datalogue.clients.http import _HttpClient, HttpMethod, MultiPartData, MultiPartFile
from datalogue.models.schema import AbstractDataSchema, Schema
from datalogue.models.datastore import Datastore, _datastore_from_payload, FileFormat, Cell, _cell_from_payload, NodeClassifications

from datalogue.errors import DtlError
from datalogue.utils import _parse_list, ResponseStream
from datalogue.anduin.client import _AnduinClient
from datalogue.anduin.models.stream import StreamStatus
from functools import reduce

class _DatastoreClient:
    """
    Client to interact with the Datastores objects
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/scout"

    def create(self, datastore: Datastore) -> Union[DtlError, Datastore]:
        """
        Creates a data source

        :param datastore: data source to be created
        :return: string with error message if failed, the data source otherwise
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores", HttpMethod.POST, datastore._as_payload())

        if isinstance(res, DtlError):
            return res

        return _datastore_from_payload(res)

    def update(self, datastore: Datastore) -> Union[DtlError, Datastore]:
        """
        Updates the backend with the new status of the existing datastore

        :param datastore: to be persisted
        :return:
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore.id),
            HttpMethod.PUT,
            datastore._as_payload()
        )

        if isinstance(res, DtlError):
            return res

        return _datastore_from_payload(res)

    def list(self, page: int = 1, item_per_page: int = 25) -> Union[DtlError, List[Datastore]]:
        """
        List all the datastores that are saved

        TODO pagination

        :param page: page to be retrieved (ignored)
        :param item_per_page: number of items to be put in a page (ignored)
        :return: Returns a List of all the available datastores or an error message as a string
        """

        res = self.http_client.make_authed_request(self.service_uri + "/datastores", HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return _parse_list(_datastore_from_payload)(res)

    def search(self,
        names: List[str] = [],
        labels: List[str] = [],
        classes: List[str] = [],
        samples: List[str] = [],
        page: int = 1,
        item_per_page: int = 25)-> Union[DtlError, List[Datastore]]:
        """
        Search existing datastores for a given different fields. If nothing is defined for any field,
        it returns every datastore (basically matches all)

        :param names: a list of datastore names
        :param labels: a list of column labels
        :param classes: a list of classes that columns are classified
        :param samples: a list values that samples might contain
        :param page: page to be retrieved
        :param item_per_page: number of items to be put in a page
        :return: Returns a List of all the available datastores or an error message as a string
        """

        queries = []

        if len(names) > 0:
            queries.append( "(" + reduce(lambda n1, n2: n1 + " OR " + n2, map(lambda n: f"name:{n}", names)) + ")")

        if len(labels) > 0:
            queries.append("(" + reduce(lambda l1, l2: l1 + " OR " + l2, map(lambda l: f"schema.nodes.label:{l}", labels)) + ")")

        if len(classes) > 0:
            #TODO Should we consider userOntology?
            queries.append("(" + reduce(lambda c1, c2: c1 + " OR " + c2, map(lambda c: f"schema.nodes.ontology.tag:{c}", classes)) + ")")

        if len(samples) > 0:
            queries.append("(" + reduce(lambda s1, s2: s1 + " OR " + s2, map(lambda s: f"samples.nodes.value:{s}", samples)) + ")")

        query = ""
        if len(queries) > 0:
            query = reduce(lambda q1, q2: q1 + " AND " + q2, queries)
        else:
            #If there is not query, we will bring everything
            query = "*"

        payload = {
            "query": query,
            "page": page,
            "size": item_per_page,
            "type": "datastore"
        }

        res = self.http_client.make_authed_request(self.service_uri + "/search", HttpMethod.POST, payload)
        return _parse_list(_datastore_from_payload)(res)

    def get_schema(self, datastore_id: UUID) -> Union[DtlError, AbstractDataSchema]:
        """
        From the provided id, get the corresponding Datastore schema

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """
        res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id) + "/schema", HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return Schema._from_payload(res).data_schema

    def print(self, datastore_id: UUID, full_path: bool = False) -> Union[DtlError, None]:
        """
        From the provided id, get the corresponding Datastore schema

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """
        res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id) + "/schema", HttpMethod.GET)
        if isinstance(res, DtlError):
            if res.message.__contains__("Route not found"):
                res.message = "Invalid ID, please verify that your data store exists with dtl.datastore.list()"
            return res
        schema = Schema._from_payload(res)
        schema.print(full_path)

    def get(self, datastore_id: UUID) -> Union[DtlError, Datastore]:
        """
        From the provided id, get the corresponding Datastore

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """

        res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id), HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return _datastore_from_payload(res)

    def delete(self, datastore_id: UUID) -> Union[DtlError, bool]:
        """
        Deletes the given Datastore

        :param datastore_id: id of the datastore to be deleted
        :return: true if successful, false otherwise
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id), HttpMethod.DELETE)

        if isinstance(res, DtlError):
            return res
        else:
            return True

    def download(self, datastore_id: UUID, file_format: FileFormat, path: str, limit: Optional[int] = None) -> Union[DtlError, str]:
        """
        Downloads the resource in a file

        :param datastore_id: id of the resource to download
        :param file_format: File format of the downloaded resource
        :param path: location to save the file
        :param limit: limit the number of elements to be downloaded
        :return: An error or the path to the downloaded file
        """

        params = {
            "fileFormat": file_format.value,
        }

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                return DtlError("limit should be a positive integer")

            params["limit"] = limit

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/download",
            HttpMethod.GET, params=params, stream=True
        )

        if isinstance(res, DtlError):
            return res

        with open(path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024 * 32):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return path

    def load_arrow_table(self, datastore_id: UUID, limit: Optional[int] = None, batch_size: int = 1024) -> \
            Union[DtlError, Table]:
        """
        Loads the resource in an in memory arrow buffer.
        This can be used either with Nvidia RAPIDS or pandas

        pandas:
        df = dtl.client.datastore.load_arrow_table(datastore_id).to_pandas()

        :param datastore_id: if of the resource to load
        :param limit: elements to be loaded in the frame
        :param batch_size: size of the batch to be retrieved at a time from the collection
        :return:
        """

        params = {
            "fileFormat": FileFormat.Csv.value
        }

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                return DtlError("limit should be a positive integer")

            params["limit"] = limit

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/download",
            HttpMethod.GET, params=params, stream=True
        )

        if isinstance(res, DtlError):
            return res

        stream = ResponseStream(res.iter_content(batch_size))

        return csv.read_csv(stream)

    def upload(self, datastore_id: UUID, file_format: FileFormat, path: str, params: dict = {}) -> Union[DtlError, None]:
        """
        Enable to upload a file to the specified resource through the platform

        :param datastore_id: id of the resource to upload the data through
        :param file_format: format of the file to be uploaded
        :param path: location of the file to upload on disk
        :return:
        """

        with open(path, 'rb') as f:
            files = [MultiPartFile("content", f)]

            data = [
                MultiPartData("file-format", file_format.value),
                MultiPartData("params", "{}"),
            ]

            res = self.http_client.post_multipart_data(
                self.service_uri + "/datastores/" + str(datastore_id) + "/upload",
                files, data
            )

            if isinstance(res, DtlError):
                return res
    
    def analyze(self, datastore_id: UUID, model_id: UUID) -> Union[DtlError, UUID]:
        """
        Starts datastore analysis

        :param datastore_id: id of the resource to be analyzed
        :param model_id: id of the classifier to use in the analysis
        :return analysis_id: id of the analysis
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/classify?classifier=" + str(model_id), HttpMethod.PUT)

        if isinstance(res, DtlError):
            return res

        return UUID(res["streamId"])

    def get_analysis_status(self, analysis_id: UUID) -> Union[DtlError, StreamStatus]:
        """
        Gets datastore analysis status

        :param analysis_id: id of the stream created
        :return:
        """
        res = self.http_client.make_authed_request('/anduin/status/' + str(analysis_id), HttpMethod.GET)
        if isinstance(res, DtlError):
            return res

        return StreamStatus.from_payload(res)

    def set_classifications(self, datastore_id: UUID, classifications=List[NodeClassifications]) -> Union[DtlError, None]:
        """
        Sets the schema classifications
        :param datastore_id: id of the datastore where the schema classification will be updated
        :param classifications: List of Node Classification that specifies which datastore path will be updated and the ontology class to use
        """

        for classification in classifications:
            res = self.http_client.make_authed_request(
                self.service_uri + "/datastores/" + str(datastore_id)+ "/classifications",
                HttpMethod.PUT,
                classification._as_payload()
            )

            if isinstance(res, DtlError):
                return res

        return None
