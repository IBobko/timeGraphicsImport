# Time Graphics Import Project

## Description

This project is designed to work with the Google Sheets API for managing data within spreadsheets. The project is built
with Python and uses libraries such as `pandas`, `google-auth`, `google-api-python-client`, and others.

## Setup

### 1. Clone the Repository

First, clone the repository:

```bash
git clone <your-repository-url>
cd timeGraphicsImport
```

### Create a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # for macOS and Linux
venv\Scripts\activate  # for Windows
```

### Install Dependencies

Install the dependencies listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```

If you need to update or add new dependencies, use the command:

```bash
pip freeze > requirements.txt
```

### Create a .env File

For managing sensitive information such as API keys, a .env file is used. Create a .env file in the root directory of
the project with the following content:

```plaintext
GOOGLE_API_CREDENTIALS_PATH=/media/nox/Samsung_T5/credentials.json
```

Replace the path with the actual path to your credentials.json file.

### Run the Project

To run the project, use the appropriate script or command, depending on your use case:

```bash
python data_transfer.py import --excel_file_path '/home/nox/Девяностые СССР-РФ.xlsx' --spreadsheet_id '1cWsqTIX1TUR5dQoINP5NhBSV--uHHQaFSbf_RJg5omE'

```

Make sure to activate your virtual environment before running any scripts.
License

