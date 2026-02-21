# Dropbox Clone

A cloud-based file storage application inspired by Dropbox, built with Flask and AWS S3. Users can register, upload/download files, and manage their storage. Includes an admin dashboard and AWS Lambda integration for SNS notifications on new user registration.

## Tech Stack

- **Backend:** Python 3, Flask, Flask-Login, Flask-Migrate
- **Database:** MySQL, SQLAlchemy
- **Cloud Storage:** AWS S3 (Boto3)
- **Serverless:** AWS Lambda, API Gateway, SNS (Serverless Framework)
- **Templating:** Jinja2, HTML/CSS

## Features

- User registration and login with hashed passwords
- File upload to AWS S3 with public URL generation
- File update (overwrite existing files)
- File deletion from S3 and database
- Paginated file listing per user
- 10 MB file size limit enforcement
- Admin dashboard to view and manage all user files
- Lambda-triggered SNS notification on user registration

## Prerequisites

- Python 3.6+
- MySQL server
- AWS account with S3 and Lambda access
- Node.js (for Serverless Framework deployment)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Dropbox-Clone
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key` |
| `DATABASE_URL` | MySQL connection string | `mysql://root:pass@localhost/putbox` |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 | `your-secret` |
| `S3_BUCKET` | S3 bucket name | `my-bucket` |
| `S3_DOMAIN` | S3 bucket domain | `bucket.s3-us-west-1.amazonaws.com` |
| `LAMBDA_SNS_URL` | Lambda SNS endpoint URL | `https://api-gw-url/...` |

## How to Run

```bash
source venv/bin/activate
python3 app.py
```
Access the application at `http://localhost:5000/`

### Deploy Lambda Functions
```bash
cd lambda
npm install
serverless deploy --stage beta
```

## Project Structure

```
Dropbox-Clone/
├── app.py                      # Application entry point
├── project/
│   ├── __init__.py             # Flask app configuration
│   ├── core/
│   │   └── views.py            # Home page route
│   ├── users/
│   │   ├── models.py           # User and Storage models
│   │   ├── views.py            # User auth and file operations
│   │   └── lambda_sns.py       # Lambda SNS notification helper
│   ├── admin/
│   │   ├── admin_cred.py       # Admin user creation script
│   │   └── views.py            # Admin dashboard routes
│   ├── error_pages/
│   │   └── handler.py          # Error handlers
│   └── templates/              # HTML templates
└── lambda/
    ├── serverless.yml          # Serverless Framework config
    └── project_files/          # Lambda function code
```

## License

MIT
