import boto3
import botocore

class UploadFileService:

    @staticmethod
    def upload_file(file_name, bucket_name):
        s3_client = boto3.client('s3', region_name='us-west-2')

        try:
            s3_client.upload_file(file_name, bucket_name, file_name)
            print(f"File '{file_name}' uploaded successfully.")
        except botocore.exceptions.ClientError as e:
            print(f"Failed to upload '{file_name}'. Error: {e}")
