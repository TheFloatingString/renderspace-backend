# RenderSpace backend

### Setup Instructions

Install dependencies:

`pip install -r requirements.txt`

Set up environment variables in a file called `.env` in root directory:

```
COSMOS_CONNECTION_STRING = "<STR>"
OPENAI_API_KEY_MIC24 = "<STR>"
```

Run the web app:

```
python app.py
```

For student view:

```localhost:5000/view/student_side```

For company view:

```localhost:5000/view/company_side```
