from helpers.LambdaHelperTranscribe import Lambda_Helper_transcribe
from helpers.S3Helper import S3_Helper
from helpers.DisplayHelper import Display_Helper
import os
import time

lambda_helper = Lambda_Helper_transcribe()
s3_helper = S3_Helper()
display_helper = Display_Helper()


text_bucket_name = os.environ['MYS3BUKETTESTINGV1']
audio_bucket_name = os.environ['MYAPPBUCKETAUDIO']

lambda_helper.lambda_environ_variables= {'MYS3BUKETTESTINGV1' : text_bucket_name}

lambda_helper.deploy_function(
    ['lambda_function_transcribe/lambda_function.py'],
    function_name='LambdaFunctionTranscribe',
    handler='lambda_function_transcribe.lambda_fuction.lambda_handler'
)

lambda_helper.filter_rules_suffix = "mp3"
lambda_helper.add_lambda_trigger(audio_bucket_name, function_name="LambdaFunctionTranscribe")

s3_helper.upload_file(audio_bucket_name, 'callcenter.mp3')
s3_helper.list_objects(audio_bucket_name)

time.sleep(30)


s3_helper.list_objects(text_bucket_name)


# s3_helper.download_object(text_bucket_name, 'results.txt')

# display_helper.text_file('results.txt')


