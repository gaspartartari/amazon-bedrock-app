import boto3
import botocore
import uuid
import time
import json

class TranscribeService:
    
    @staticmethod
    def transcribe(file_name, bucket_name):
        transcribe_client = boto3.client('transcribe', region_name='us-west-2')
        s3_client = boto3.client('s3',region_name='us-west-2' )

        job_name = 'transcription-job-' + str(uuid.uuid4())
        
        try:
            response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': f's3://{bucket_name}/{file_name}'},
                MediaFormat='mp3',
                LanguageCode='en-US',
                OutputBucketName=bucket_name,
                Settings={
                    'ShowSpeakerLabels': True,
                    'MaxSpeakerLabels': 2
                }
            )
        except Exception as e:
            print(f"Failed to start transcription job: {e}")
            return None, f"Failed to start job: {e}"

        while True:
            try:
                status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
                print("Current job status:", status['TranscriptionJob']['TranscriptionJobStatus'])
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(2)
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print("Final job status:", status['TranscriptionJob']['TranscriptionJobStatus'])
        
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    
            # Load the transcript from S3.
            transcript_key = f"{job_name}.json"
            transcript_obj = s3_client.get_object(Bucket=bucket_name, Key=transcript_key)
            transcript_text = transcript_obj['Body'].read().decode('utf-8')
            transcript_json = json.loads(transcript_text)
            
            output_text = ""
            current_speaker = None
            
            items = transcript_json['results']['items']
            
            print(items)
            
            for item in items:
                
                speaker_label = item.get('speaker_label', None)
                content = item['alternatives'][0]['content']
                
                # Start the line with the speaker label:
                if speaker_label is not None and speaker_label != current_speaker:
                    current_speaker = speaker_label
                    output_text += f"\n{current_speaker}: "
                    
                # Add the speech content:
                if item['type'] == 'punctuation':
                    output_text = output_text.rstrip()
                    
                output_text += f"{content} "
                
            # Save the transcript to a text file
            with open(f'{job_name}.txt', 'w') as f:
                f.write(output_text)
            
            return status['TranscriptionJob']['TranscriptionJobStatus'], job_name