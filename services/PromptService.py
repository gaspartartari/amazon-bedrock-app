from jinja2 import Template
import boto3
import json

class PromptService:
    
    @staticmethod
    def prompt(job_name):
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

        try:
            with open(f'{job_name}.txt', "r") as file:
                transcript = file.read()
        except FileNotFoundError:
            print(f"File {job_name}.txt not found.")
            return None

        try:
            with open('resources/promptTemplate.txt', "r") as file:
                template_string = file.read()
        except FileNotFoundError:
            print("Template file promptTemplate.txt not found.")
            return None

        template = Template(template_string)
        
        data = {
            'transcript': transcript
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
                    "temperature": 1,
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
