# FastAPI Weather API

This guide provides instructions for setting up and using a FastAPI-based Weather API. The API has the following
endpoints:

- `/api/weather`: Retrieves weather data.
- `/api/weather/stats`: Provides statistics about the weather data.
- `/docs`: Offers documentation using OpenAPI.

## Prerequisites

Before using this API, ensure you have the following prerequisites:

- Python (3.7 or higher)
- Virtualenv
- AWS account (if deploying to AWS)

## Installation and Usage

Follow these steps to install and use the API:

1. Create and activate a virtual environment:

   ```bash
   pip3 install virtualenv
   python3 -m virtualenv venv
   ```

2. Activate the virtual environment:

    - Windows: `venv\Scripts\activate`
    - Linux and macOS: `source venv/bin/activate`

3. Install required dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Navigate to the `src` directory:

   ```bash
   cd src
   ```

5. Ingest the data:

   ```bash
   python3 ingest_data.py
   ```

6. Run the server:

   ```bash
   uvicorn app:app --reload
   ```

7. Access the API endpoints:

    - Weather Records: http://127.0.0.1:8000/api/weather/
    - Weather Stats: http://127.0.0.1:8000/api/weather/stats
    - API Documentation UI: http://127.0.0.1:8000/docs

## Running Tests

To run tests:

1. If not in `src` then navigate to the `src` directory:

   ```bash
   cd src
   ```

2. Run pytest:

   ```bash
   pytest
   ```

## AWS Deployment

For AWS deployment, follow these steps:

1. Create a Python project with an `app.py` file containing FastAPI application code.

2. Create a new AWS Lambda function with Python 3.8 or later runtime.

3. Package your Python code and dependencies as a ZIP file, and upload it to AWS Lambda.

4. Set the handler function in your Lambda function to your FastAPI application function's name.

5. Create an API Gateway (REST API or HTTP API) that integrates with your Lambda function.

6. Deploy the APIs to publicly accessible endpoints.

7. Use Amazon RDS to store ingested data.

