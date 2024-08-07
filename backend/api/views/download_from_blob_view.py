# download_problem_view.py

import logging
import os

from api.models import StorageLocation
from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class DownloadFromBlobViewSet(ViewSet):
    """
    This class is responsible for handling all requests related to downloading a storage location file from the blobstorage.
    """

    logger = logging.getLogger(__name__)

    @action(detail=False, methods=["GET"])
    def storage_location(self, request):
        id = request.GET.get('id')
        storage_location = None
        try:
            storage_location = StorageLocation.objects.get(pk=id)
        except Exception as e:
            self.logger.error(e, exc_info=True)
        
        if not storage_location:
            # Storage location not found for id.
            return HttpResponse(status=404)
        
        if not storage_location.is_downloadable:
            # Forbidden, when not downloadable.
            return HttpResponse(status=403)
        
        return self.download_file(storage_location.filepath, storage_location.container)
    

    def download_file(self, file_path, container):
        """ Generic download function for files from blob storage """
        
        try:
            # Setup connection
            connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            blob_service_client = BlobServiceClient.from_connection_string(
                str(connection_string)
            )
            blob_client = blob_service_client.get_blob_client(
                container=container, blob=file_path
            )

            download_stream = blob_client.download_blob()

            # Return the file content
            response = HttpResponse(
                download_stream.readall(), content_type="application/octet-stream", status=200
            )
            response["Content-Disposition"] = (
                f"attachment; filename={os.path.basename(file_path)}"
            )
            return response
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response({"error": "File download failed"}, status=status.HTTP_400_BAD_REQUEST)
