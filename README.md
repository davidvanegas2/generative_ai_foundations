# Generative AI on AWS with Bedrock

This repository is dedicated to exploring Generative AI on AWS with the help of Amazon Bedrock. The examples provided here are based on the use cases covered in a Udemy course on Generative AI on AWS.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Use Cases](#use-cases)
  - [Poster Generation with Stability's Stable Diffusion Model](#poster-generation-with-stabilitys-stable-diffusion-model)
  - [Summarization of Manufacturing Logs with Cohere's Command Model](#summarization-of-manufacturing-logs-with-coheres-command-model)
  - [Chatbot Creation with Message History and RAG Implementation](#chatbot-creation-with-message-history-and-rag-implementation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This repository contains implementations of various use cases utilizing Generative AI models on AWS with Bedrock. Each use case is stored in its own folder and provides detailed instructions on how to set up and run the example.

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/generative-ai-aws-bedrock.git
    cd generative-ai-aws-bedrock
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Use Cases

### Poster Generation with Stability's Stable Diffusion Model
**Folder:** `image_media_industry`

**Description:** This use case demonstrates how to generate posters using Stability's Stable Diffusion model. The Stable Diffusion model is a powerful generative model for creating high-quality images.

**Instructions:**
1. Navigate to the `image_media_industry` folder:
    ```sh
    cd image_media_industry
    ```

2. Follow the instructions in the `README.md` file within the folder to set up and run the poster generation example.

### Summarization of Manufacturing Logs with Cohere's Command Model
**Folder:** `manufacturing_logs_summarization`

**Description:** This use case focuses on summarizing manufacturing logs using Cohere's Command model. The Command model is designed for natural language processing tasks, including summarization.

**Instructions:**
1. Navigate to the `manufacturing_logs_summarization` folder:
    ```sh
    cd manufacturing_logs_summarization
    ```

2. Follow the instructions in the `README.md` file within the folder to set up and run the summarization example.

### Chatbot Creation with Message History and RAG Implementation
**Folder:** `RAG_chatbot_HR`

**Description:** This use case demonstrates the creation of a chatbot that maintains message history and integrates Retrieval-augmented Generation (RAG) for enhanced responses. RAG combines generative models with retrieval-based approaches to provide more accurate and contextually relevant answers.

**Instructions:**
1. Navigate to the `RAG_chatbot_HR` folder:
    ```sh
    cd chatbot_with_rag
    ```

2. Follow the instructions in the `README.md` file within the folder to set up and run the chatbot example. This will include setting up message history storage, configuring the RAG system, and testing the chatbot functionality.

## Prerequisites
- Python 3.7+
- An AWS account with appropriate permissions to use Amazon Bedrock
- Git
- A virtual environment tool (e.g., `venv`)

## Usage
To use any of the provided use cases, follow these general steps:
1. Navigate to the desired use case folder.
2. Follow the specific setup and execution instructions provided in the `README.md` file within the folder.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-feature-branch`
5. Submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
