import boto3
import json
from jinja2 import Template
import uuid

s3_client = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime', 'us-west-2')

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # One of a few different checks to ensure we don't end up in a recursive loop.
    if "transcription-job" not in key: 
        print("This demo only works with *-transcript.json.")
        return
    
    try:
        file_content = ""
        
        response = s3_client.get_object(Bucket = bucket, Key = key)
        
        file_content = response['Body'].read().decode('utf-8')
        
        transcript = extract_transcript_from_file_content(file_content)
        
        print(f"Successfully read file {key} from bucket {bucket}.")

        print(f"Transcript: {transcript}")
        
        summary = bedrock_summarisation(transcript)
        
        result_key = key.replace(".json", "result.txt")
    
        
        s3_client.put_object(
            Bucket = bucket,
            Key = result_key,
            Body = summary,
            ContentType = 'text/plain'
        )
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully summarized {key} from bucket {bucket}. Summary: {summary}")
    }
    
    
    
    
def extract_transcript_from_file_content(file_content):

    transcript_json = json.loads(file_content)

    output_text = ""
    current_speaker = None

    items = transcript_json['results']['items']

    # Iterate through the content word by word:
    for item in items:
        speaker_label = item.get('speaker_label', None)
        content = item['alternatives'][0]['content']
        
        # Start the line with the speaker label:
        if speaker_label is not None and speaker_label != current_speaker:
            current_speaker = speaker_label
            output_text += f"\n{current_speaker}: "
        
        # Add the speech content:
        if item['type'] == 'punctuation':
            output_text = output_text.rstrip()  # Remove the last space
        
        output_text += f"{content} "
        
    return output_text


def bedrock_summarisation(transcript):
    

    try:
        with open('resources/promptTemplateV2.txt', "r") as file:
            template_string = file.read()
    except FileNotFoundError:
        print("Template file promptTemplate.txt not found.")
        return None

    template = Template(template_string)
    
    data = {
        'transcript': transcript,
        'topics': ['charges', 'quality', 'price']
    }
    
    prompt = template.render(data)
    print(prompt)

    kwargs = {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 100,
                "temperature": 0,
                "stopSequences": [],
                "topP": 0.1
            }
        })
    }

    try:
        response = bedrock_runtime.invoke_model(**kwargs)
        response_body = json.loads(response['body'].read())
        generation = response_body['results'][0]['outputText']
        print(generation)
        return generation
    except Exception as e:
        print(f"Error invoking model: {e}")
        return None
    
        
