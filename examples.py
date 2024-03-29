
import boto3
import json
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')



prompt = "Write a one sentence summary of Brazil."
kwargs = {
    "modelId": "amazon.titan-text-lite-v1",
    "contentType": "application/json",
    "accept": "*/*",
    "body": json.dumps(
        {
            "inputText": prompt
        }
    )
}
response = bedrock_runtime.invoke_model(**kwargs)

print (response)

response_body = json.loads(response.get('body').read())

print(json.dumps(response_body, indent=4))

print(response_body['results'][0]['outputText'])

prompt = "Write a random motivational speak"

kwargs = {
    "modelId": "amazon.titan-text-express-v1",
    "contentType": "application/json",
    "accept": "*/*",
    "body": json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 100,
                "temperature": 0.9,
                "topP": 0.9
            }
        }
    )
}

response = bedrock_runtime.invoke_model(**kwargs)
response_body = json.loads(response.get('body').read())

generation = response_body['results'][0]['outputText']
print(generation)

print(json.dumps(response_body, indent=4))


with open('transcript.txt', "r") as file:
    dialogue_text = file.read()
    
print(dialogue_text)


prompt = f"""The text between the <transcript> XML tags is a transcript of a conversation. 
Write a short summary of the conversation.

<transcript>
{dialogue_text}
</transcript>

Here is a summary of the conversation in the transcript:"""


print(prompt)


kwargs = {
    "modelId": "amazon.titan-text-express-v1",
    "contentType": "application/json",
    "accept": "*/*",
    "body": json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 50,
                "temperature": 0,
                "topP": 0.9
            }
        }
    )
}

response = bedrock_runtime.invoke_model(**kwargs)
response_body = json.loads(response.get('body').read())

generation = response_body['results'][0]['outputText']
print(generation)

