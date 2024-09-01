
# Serverless Conversation Analysis with AWS Lambda, Amazon S3, and Amazon Bedrock

This project demonstrates a serverless architecture that leverages AWS Lambda, Amazon S3, and Amazon Bedrock for processing, analyzing, and summarizing conversation transcripts. Designed as part of a hands-on learning module from DeepLearning.AI, this solution automates the transcription of audio files, applies advanced summarization and sentiment analysis using Amazon Bedrock Large Language Models (LLMs), and stores the results securely in Amazon S3.

## 🚀 Features

- **Serverless Computing:** Utilize AWS Lambda for scalable, on-demand execution of application logic without the overhead of server management.
- **Automated Processing Pipeline:** Automatically triggers transcription and analysis workflows when audio files are uploaded to Amazon S3.
- **State-of-the-Art Summarization:** Leverages Amazon Bedrock LLMs to generate concise and accurate summaries, extracting key points and insights.
- **Sentiment Analysis:** Analyze the emotional tone and overall sentiment of conversations, providing critical insights into customer interactions.
- **Robust Storage with Amazon S3:** Seamless integration with Amazon S3 for the storage and retrieval of audio files, transcripts, and analysis results.

## 🛠️ How It Works

1. **Audio Upload to S3:** Users upload audio files (.mp3) to a designated Amazon S3 bucket, which automatically triggers a Lambda function for transcription.
2. **Transcription via Amazon Transcribe:** The triggered Lambda function uses Amazon Transcribe to convert speech to text, generating a transcript of the conversation.
3. **Summarization & Sentiment Analysis:** Another Lambda function, powered by Amazon Bedrock LLMs, processes the transcript to summarize key points and assess sentiment.
4. **Result Storage in S3:** The summarized text and sentiment analysis output are securely stored back in Amazon S3, making them readily available for review and further analysis.

## 📦 Setup and Deployment

1. **AWS Account Configuration:** Ensure your AWS account is set up with the necessary permissions to use AWS Lambda, Amazon S3, Amazon Transcribe, and Amazon Bedrock services.
2. **Environment Variable Configuration:** Set up environment variables in your Lambda functions for S3 bucket names, IAM roles, and any other required configurations.
3. **Deploy Lambda Functions:** Use the provided deployment scripts to set up Lambda functions that handle transcription, summarization, and sentiment analysis.
4. **Prepare S3 Buckets:** Create and configure Amazon S3 buckets to manage the storage of input audio files, transcripts, and analytical outputs.

## 🎓 Acknowledgements

A heartfelt thanks to DeepLearning.AI for providing the knowledge and practical skills that were instrumental in building this project. The short course on cloud computing and machine learning applications provided a solid foundation for integrating advanced AWS services into scalable solutions.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
