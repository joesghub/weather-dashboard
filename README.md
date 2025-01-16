# 30 Days DevOps Challenge - Weather Dashboard

Day 1: Building a weather data collection system using AWS S3 and OpenWeather API

# Weather Data Collection System - DevOps Day 1 Challenge

## Project Overview
This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:
- External API Integration (OpenWeather API)
- Cloud Storage (AWS S3)
- Infrastructure as Code
- Version Control (Git)
- Python Development
- Error Handling
- Environment Management

## Features
- Fetches real-time weather data for multiple cities
- Displays temperature (°F), humidity, and weather conditions
- Automatically stores weather data in AWS S3
- Supports multiple cities tracking
- Timestamps all data for historical tracking

## Technical Architecture
- **Language:** Python 3.x
- **Cloud Provider:** AWS (S3)
- **External API:** OpenWeather API
- **Dependencies:** 
  - boto3 (AWS SDK)
  - python-dotenv
  - requests

## Project Structure
weather-dashboard/
  src/
    __init__.py
    weather_dashboard.py
  tests/
  data/
  .env
  .gitignore
  requirements.txt

## Setup Instructions
1. Clone the repository:
--bash
git clone https://github.com/ShaeInTheCloud/30days-weather-dashboard.git

3. Install dependencies:
bashCopypip install -r requirements.txt

4. Configure environment variables (.env):
CopyOPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name

4.Configure AWS credentials:
bashCopyaws configure

5. Run the application:
python src/weather_dashboard.py


## Steps I Took

1. Update environment - sudo apt update
2. Install Github
3. Authenticate Github
4. Clone Repo
5. Update remote origin
6. Create Blank Repo
7. Push Cloned Repo
8. Install Python and Pip
9. Install Requirements
a. Issues downloading requirements

error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

Requirements.txt:
boto3==1.26.137
python-dotenv==1.0.0
requests==2.28.2

When I tried to install packages using pip install -r requirements.txt, the system detected that:
- I was attempting to install packages into the system-wide Python environment.
- Modifying the system Python environment directly could potentially break OS-level software or dependencies.

Using sudo apt install resolved the issue because:
- The packages you needed were available as pre-built Debian packages (python3-boto3, python3-dotenv, etc.).
- apt is the recommended tool for managing system-level dependencies in Debian-based systems like Ubuntu.
- The installation via apt ensured the system's package manager handled dependency resolution, maintaining system integrity.

To avoid similar issues and maintain clean environments for Python projects:

Use Virtual Environments:
Create a virtual environment:
python3 -m venv venv

Activate it:
source venv/bin/activate

Install your requirements in the virtual environment:
pip install -r requirements.txt
10. Install Python Venv and Reinstall Requirements.txt
11. Install AWS CLI
12. Configure AWS CLI
13. Retrieve OpenWeather API Key
14. Fill in .env file with Keys and Names
a. Issues automating the bucket name creation so it is globally unique

AWS_BUCKET_NAME=weather_dashboard_${RANDOM}

The original application referenced the .env file to get a unique bucket name, however .env files do not interpret shell-specific variables [like ${RANDOM}] dynamically. The value will be treated as a literal string, meaning AWS_BUCKET_NAME will always equal "weather_dashboard_${RANDOM}".

To ensure unique names were created dynamically, I needed to generate them in the script itself, not the .env file.

I went with a combined solution of referencing the .env file for the prefix of my S3 bucket name and generating a suffix dynamically in my script. 

I wanted to use a method that relies on the .env file because I also store the OpenWeather API key in the file. Personally I rather have two pieces of information in the .env file to ensure it is working before making the API calls. My backup for the referencing of the prefix is a default prefix value which is included as a variable arguments. 

AWS_BUCKET_PREFIX=weather_dashboard
prefix = os.getenv('AWS_BUCKET_PREFIX', 'weather_dashboard')

15. Activate Venv
16. Run Application
a. Error creating bucket: An error occurred (IllegalLocationConstraintException) when calling the CreateBucket operation: The unspecified location constraint is incompatible for the region specific endpoint this request was sent to.

self.s3_client = boto3.client('s3', region_name='us-west-1')
...
self.s3_client.create_bucket(Bucket=self.bucket_name)
print(f"Successfully created bucket {self.bucket_name} in us-west-1.")

The CreateBucket request doesn't include a 'CreateBucketConfiguration' when using a region-specific endpoint, and the bucket's region is inferred incorrectly. In regions other than us-east-1, you must specify the LocationConstraint in the CreateBucketConfiguration.

The script used the us-west-1 endpoint (https://s3.us-west-1.amazonaws.com) but didn't specify a LocationConstraint. As a result, AWS inferred that the bucket was being created in the default region (us-east-1), which is incompatible with the region-specific endpoint.

When using region_name='us-west-1' in the boto3.client, the LocationConstraint ensures alignment with the specified region.

CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-1'
                }

self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-1'
                }
            )

I also took an opportunity to use the time.sleep() function from Python's time module to introduce a pause in the execution of the script. This will give some time for the bucket to be created and propagated before I proceed with saving data.

b. Error creating bucket: An error occurred (InvalidBucketName) when calling the CreateBucket operation: The specified bucket is not valid.

Bucket names can only contain lowercase letters, numbers, hyphens (-), and must start and end with a lowercase letter or number. Names like "weather_dashboard_6u3mv1" are invalid because they do not meet the AWS naming standards.

Learning this, I went ahead and updated the script so the underscrores were all hyphens

17. Check S3 Bucket
18. Clean up Resources

## What I Learned

AWS S3 bucket creation and management
Environment variable management for secure API keys
Python best practices for API integration
Git workflow for project development
Error handling in distributed systems
Cloud resource management

## Future Enhancements

Add weather forecasting
Implement data visualization
Add more cities
Create automated testing
Set up CI/CD pipeline