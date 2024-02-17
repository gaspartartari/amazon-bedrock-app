import time
from helpers.DisplayHelper import Display_Helper
from helpers.LambdaHelper import Lambda_Helper
import os

from helpers.S3Helper import S3_Helper

# Create an instance of the Lambda_Helper class
lambda_helper = Lambda_Helper()

s3_helper = S3_Helper()

display_helper = Display_Helper()


# Now call deploy_function on this instance
lambda_helper.deploy_function(["lambda_function.py", "resources/promptTemplateV2.txt"], function_name="LambdaFunctionSummarize")

lambda_helper.filter_rules_suffix = "json"
lambda_helper.add_lambda_trigger(os.environ['MYS3BUKETTESTINGV1'])

s3_helper.upload_file(os.environ['MYS3BUKETTESTINGV1'], 'demo-transcript.json')
   

s3_helper.list_objects(os.environ['MYS3BUKETTESTINGV1'])