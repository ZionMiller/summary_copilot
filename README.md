# Sales Call Copilot API

## Overview
Sales Call Copilot is a solution designed to optimize sales team productivity by automating call summaries for internal and external use. It aims to address the challenge of time-consuming follow-ups and information sharing after sales calls. By generating personalized summaries, Sales Call Copilot enables sales teams to focus on revenue-generating activities while maintaining consistent communication and documentation for customers. Additionally, it provides management with a steady stream of updates without sacrificing valuable selling time.
[View video walk through](https://www.loom.com/share/6d53e1ce48394762afd3c1c712784fb9)


#
## Features
* Automated Summaries: Sales Call Copilot automatically generates two summaries for each call - an internal summary and an external summary.
* Personalized Content: The external summary uses first-person language, includes customer names (if available), and provides a personalized thank-you message.
* Key Points and Roadblocks: The internal summary captures essential information such as key points, dates, dollar size, roadblocks, and other relevant details.
* Next Steps and Conclusion: The external summary outlines the next steps to be taken and concludes with a final thank-you message.
* Database Integration: Summaries are saved in a MongoDB database for easy access and retrieval.
#
## Installation
To set up the Sales Call Copilot API, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/your/repo.git
    ```
2. Install the required dependencies:
```pip install -r requirements.txt```
3. MongoDB Setup: If you already have MongoDB installed and running locally, you can skip this step. Otherwise, follow these instructions to [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/)
:
For macOS users, you can use Homebrew:
* ```brew tap mongodb/brew```
* ```brew install mongodb-community```
For other operating systems, refer to the official MongoDB installation guide: [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/)
4. Configure the MongoDB connection details:
* If you are using MongoDB locally with default settings, no additional configuration is required.
* If you are using a remote MongoDB server or have customized connection settings, update the connection details app/mongodb.py to match your configuration.
5. [Obtain an API key from OpenAI](https://openai.com)
:
* Visit the OpenAI website and create an account if you haven't already.
* Follow their documentation to obtain an API key for accessing the OpenAI API.
* Set the API key as an environment variable. Refer to the OpenAI documentation or your specific framework for instructions on how to set environment variables.
* **Important:** Make sure to exclude the `.env` file from version control by adding it to your `.gitignore` file.

Once you have completed these steps, you will have the Sales Call Copilot API set up and ready to use.
#
## Usage
1. Start the Sales Call Copilot API: 
    ```
    cd app

    python main.py
    ```
2. Make a POST request to the `/summaries` endpoint with a JSON payload containing the call transcript. Example:

    ```
    POST /summaries
    Content-Type: application/json

    {
    "transcript": "Here is the call transcript..."
    }
    ```
3. The API will generate the internal and external summaries using the provided transcript and store them in the MongoDB database.
4. Retrieve a summary by making a GET request to the ```/summaries/{summary_id}``` endpoint, where ```{summary_id}``` is the ID of the summary.
5. Delete a summary by making a DELETE request to the ```/summaries/{summary_id}``` endpoint.

#

## Contributing
Contributions are welcome! Please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.