import boto3
import os
from helpers.CloudWatchHelper import CloudWatch_Helper

class ConfigService:
    @staticmethod
    def setup_logging():
        bedrock = boto3.client('bedrock', region_name="us-west-2")
        cloudwatch = CloudWatch_Helper()

        log_group_name = '/my/amazon/bedrock/logs'
        loggingConfig = {
            'cloudWatchConfig': {
                'logGroupName': log_group_name,
                'roleArn': os.environ['LOGGINGROLEARN'],
                'largeDataDeliveryS3Config': {
                    'bucketName': os.environ['LOGGINGBUCKETNAME'],
                    'keyPrefix': 'amazon_bedrock_large_data_delivery',
                }
            },
            's3Config': {
                'bucketName': os.environ['LOGGINGBUCKETNAME'],
                'keyPrefix': 'amazon_bedrock_logs',
            },
            'textDataDeliveryEnabled': True,
        }

        bedrock.put_model_invocation_logging_configuration(loggingConfig=loggingConfig)
        print("Logging configuration set up successfully.")
