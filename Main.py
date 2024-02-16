from jinja2 import Template
from config.ConfigService import ConfigService
from services.PromptService import PromptService
from services.TranscribeService import TranscribeService
from services.UploadFileService import UploadFileService



def main():
    # Your main code logic here
    print("This is the main function.")


    ConfigService.setup_logging()

    bucket_name = 'mybucketfortranscriptionapp'

    file_name = 'resources/callcenter.mp3'

    UploadFileService.upload_file(file_name, bucket_name)

    status, job_name = TranscribeService.transcribe(file_name, bucket_name)
    print(status, job_name)
    
    if status != 'COMPLETED':
        print(f"Transcription job {job_name} failed with status: {status}")
        return  # or handle the error as needed



    generation = PromptService.prompt(job_name)



if __name__ == "__main__":
    main()

