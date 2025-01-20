# 30 Days DevOps Challenge - Weather Dashboard

## Project Overview
This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:
- **External API Integration** (OpenWeather API)
- **Cloud Storage** (AWS S3)
- **Infrastructure as Code**
- **Version Control** (Git)
- **Python Development**
- **Error Handling**
- **Environment Management**

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
```
weather-dashboard/
  src/
    __init__.py
    weather_dashboard.py
  tests/
  data/
  .env
  .gitignore
  requirements.txt
```

## Steps I Took

### **Summary of the Journey**

In this project, I focused on setting up a weather data collection system by integrating the OpenWeather API with AWS S3 for storage. The journey involved several key stages, starting from system setup and installing essential tools like Git, Python, and AWS CLI. After cloning and pushing the repository, I encountered challenges with Python package installations due to system-wide environment restrictions. To resolve this, I transitioned to using virtual environments.

I also tackled issues like automating the creation of a unique S3 bucket name using environment variables and script-based solutions. During the application run, I faced errors related to AWS S3 bucket creation, which I resolved by ensuring correct region specifications and valid bucket names. After successfully configuring everything, I verified the S3 bucket and cleaned up resources to finalize the setup.

This journey was a hands-on experience in applying DevOps practices, from version control and environment management to cloud resource configuration and error handling.


1. **Update environment** 
```
sudo apt update
```

2. **Install Github**
```
sudo apt install gh
```

3. **Authenticate Github**
```
gh auth login
```

4. **Clone Repo**
```
git clone https://github.com/ShaeInTheCloud/30days-weather-dashboard.git
```

5. **Create Blank Repo**
```
https://github.com/joesghub/weather-dashboard.git
```

6. **Update remote origin**
```
git remote add origin https://github.com/joesghub/weather-dashboard.git
```

7. **Push Cloned Repo**
```
git push -u origin main
```

8. **Install Python and Pip**
```
sudo apt install -y python3 python3-pip 
```

9. **Install Requirements**
```
pip install -r requirements.txt 
```
**Issues downloading requirements**

I received the following error when trying to install the requirements.txt file:
> error: externally-managed-environment
> 
> × This environment is externally managed
> 
> ╰─> To install Python packages system-wide, try apt install
> 
>    python3-xyz, where xyz is the package you are trying to
> 
>    install.

The contents of the requirements.txt file:
> boto3==1.26.137
> 
> python-dotenv==1.0.0
> 
> requests==2.28.2


When I tried to install packages using ```pip install -r requirements.txt```, the system detected that:
- I was attempting to install packages into the system-wide Python environment.
- Modifying the system Python environment directly could potentially break OS-level software or dependencies.

The requirements I need are available as pre-built Debian packages (python3-boto3, python3-dotenv, etc.). It would be better if I usedthe recommended tool for managing system-level dependencies in Debian-based systems like Ubuntu. Installation via ```apt``` ensures the system's package manager handled dependency resolution, maintaining system integrity.

However, instead of using ```apt``` to download the requirements to my entire environment, I could use a Virtual Environment. Virtual environments help to isolate certain requiremnts and packages so they do not become the default tools for your entire system/environment. 

10. **Install Python Venv and Reinstall Requirements.txt**

To proceed, I needed to download python3 venv, create the environment, activate it, and install my requirements

```
sudo apt install -y python3-venv

python3 -m venv venv

source venv/bin/activate 

pip install -r requirements.txt
```


11. **Install AWS CLI**

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

sudo apt install unzip

unzip awscliv2.zip

sudo ./aws/install

aws --version
```

12. **Configure AWS CLI**

```
aws configure
```

13. **Retrieve OpenWeather API Key**

[Open Weather API Site](https://openweathermap.org/api)

14. **Fill in .env file with Keys and Names**


**Issues automating the bucket name creation so it is globally unique**

 ``` AWS_BUCKET_NAME=weather_dashboard_${RANDOM} ```

The original application referenced the .env file to get a unique bucket name, however .env files do not interpret shell-specific variables [like ${RANDOM}] dynamically. The value will be treated as a literal string, meaning AWS_BUCKET_NAME will always equal "weather_dashboard_${RANDOM}". To ensure unique names were created dynamically, I needed to generate them in the script itself, not the .env file. I went with a combined solution of referencing the .env file for the prefix of my S3 bucket name and generating a suffix dynamically in my script. 

I wanted to use a method that relies on the .env file because I also store the OpenWeather API key in the file. Personally I rather have two pieces of information in the .env file to ensure it is working before making the API calls. My backup for the referencing of the prefix is a default prefix value which is included as a variable arguments. 

```
AWS_BUCKET_PREFIX=weather_dashboard

prefix = os.getenv('AWS_BUCKET_PREFIX', 'weather_dashboard')
```


15. **Run Application**

**Issues generating the S3 bucket in a Region**

> Error creating bucket: An error occurred (IllegalLocationConstraintException) when calling the CreateBucket operation: The unspecified location constraint is incompatible for the region 
> 
> specific endpoint this request was sent to.

```
self.s3_client = boto3.client('s3', region_name='us-west-1')
...
self.s3_client.create_bucket(Bucket=self.bucket_name)
print(f"Successfully created bucket {self.bucket_name} in us-west-1.")
```

The CreateBucket request ```self.s3_client.create_bucket(Bucket=self.bucket_name)``` doesn't include a 'CreateBucketConfiguration' when using a region-specific endpoint, and the bucket's region is inferred incorrectly. In regions other than us-east-1, you must specify the LocationConstraint in the CreateBucketConfiguration.

The script used the us-west-1 endpoint (https://s3.us-west-1.amazonaws.com) but didn't specify a LocationConstraint. As a result, AWS inferred that the bucket was being created in the default region (us-east-1), which is incompatible with the region-specific endpoint.

When using region_name='us-west-1' in the boto3.client, the LocationConstraint ensures alignment with the specified region.

```
CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-1'
                }
```
```
self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-1'
                }
            )
```

I also took an opportunity to use the ```time.sleep()``` function from Python's time module to introduce a pause in the execution of the script. This will give some time for the bucket to be created and propagated before I proceed with saving data.

***Issues naming the S3 bucket***

> Error creating bucket: An error occurred (InvalidBucketName) when calling the CreateBucket operation: The specified bucket is not valid.

- Bucket names can only contain lowercase letters, numbers, hyphens (-), and must start and end with a lowercase letter or number. Names like "weather_dashboard_6u3mv1" are invalid because they do not meet the AWS naming standards.

Learning this, I went ahead and updated the script so the underscrores were all hyphens. Afterward, the script ran successfully!

![Running Application Successfully](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/%20running%20python%20application.png?raw=true)

17. **Check S3 Bucket**

![Dynamically generated s3 bucket](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/dynamically%20generated%20s3%20bucket.png?raw=true)

![Weather data in s3 bucket](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/weather%20data%20in%20s3%20bucket.png?raw=true)

![Json for cities weather](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/json%20for%20cities%20weather.png?raw=true)

![NY weather data overview](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/ny%20weather%20data%20overview.png?raw=true)

![NY weather data contents](https://github.com/joesghub/weather-dashboard/blob/main/screenshots/ny%20weather%20data%20contents.png?raw=true)


18. **Clean up Resources**

I do not happen to be on a free AWS account so I removed my S3 bucket contents, deleted the bucket, and stopped my instance running the application.

Altogether this project cost me about $0.31 from creation of resources to confirmation of application success!
## What I Learned

- AWS S3 bucket creation and management
- Environment variable management for secure API keys
- Python best practices for API integration
- Git workflow for project development
- Error handling in distributed systems
- Cloud resource management

## Future Enhancements

- Add weather forecasting
- Implement data visualization
- Add more cities
- Create automated testing
- Set up CI/CD pipeline


