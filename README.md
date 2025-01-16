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

1. **Update System Environment:**
   ```bash
   sudo apt update
   ```

2. **Install Git:**
   - Installed Git to manage the code repository.

3. **Authenticate GitHub:**
   - Authenticated GitHub to connect the repository with my account.

4. **Clone the Repository:**
   - Cloned the repository to my local machine:
     ```bash
     git clone https://github.com/ShaeInTheCloud/30days-weather-dashboard.git
     ```

5. **Update Remote Origin:**
   - Updated the remote origin to point to the correct GitHub repository.

6. **Create a Blank GitHub Repository:**
   - Created a new blank repository on GitHub to push the local clone.

7. **Push Cloned Repo to GitHub:**
   - Pushed the cloned repository to the newly created GitHub repo:
     ```bash
     git push -u origin master
     ```

8. **Install Python and Pip:**
   - Installed Python and pip if not already installed:
     ```bash
     sudo apt install python3 python3-pip
     ```

9. **Install Project Requirements:**
   - Attempted to install dependencies from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - **Issue:** An error occurred: `externally-managed-environment`
     - This error occurred because I was trying to install the packages into the system-wide Python environment.
     - To resolve the issue, I used `apt` to install the packages as pre-built Debian packages:
       ```bash
       sudo apt install python3-boto3 python3-dotenv python3-requests
       ```

   - **Best Practice:** To avoid system-wide changes and maintain clean Python environments:
     1. Create a virtual environment:
        ```bash
        python3 -m venv venv
        ```
     2. Activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```
     3. Install the required packages inside the virtual environment:
        ```bash
        pip install -r requirements.txt
        ```

10. **Install AWS CLI:**
    - Installed the AWS Command Line Interface (CLI) to manage AWS services:
      ```bash
      sudo apt install awscli
      ```

11. **Configure AWS CLI:**
    - Configured the AWS CLI with my AWS credentials:
      ```bash
      aws configure
      ```

12. **Retrieve OpenWeather API Key:**
    - Retrieved an API key from OpenWeather and added it to the `.env` file.

13. **Fill in the .env File:**
    - Added the necessary keys to the `.env` file, including the OpenWeather API key and AWS bucket name.

14. **Issue with Automating Bucket Name Creation:**
    - **Problem:** The original `.env` file contained the following line to generate a unique bucket name:
      ```bash
      AWS_BUCKET_NAME=weather_dashboard_${RANDOM}
      ```
    - **Issue:** `.env` files don’t interpret shell-specific variables like `${RANDOM}` dynamically.
    - **Solution:** I had to modify the script to generate the unique bucket name dynamically, instead of relying on the `.env` file:
      ```python
      AWS_BUCKET_PREFIX = os.getenv('AWS_BUCKET_PREFIX', 'weather_dashboard')
      ```
      This way, I could still use a prefix from the `.env` file and dynamically generate the suffix within the script.

15. **Activate Virtual Environment:**
    - Activated the virtual environment to ensure that the dependencies were installed and used correctly.

16. **Run the Application:**
    - Ran the application:
      ```bash
      python src/weather_dashboard.py
      ```

    **Error Handling During Bucket Creation:**

    a. **Error: IllegalLocationConstraintException**  
       When trying to create an S3 bucket in the `us-west-1` region, I encountered an error because the region wasn't specified correctly in the `CreateBucket` request. 
       - **Solution:** Add the `LocationConstraint` to the `CreateBucketConfiguration`:
         ```python
         self.s3_client.create_bucket(
             Bucket=self.bucket_name,
             CreateBucketConfiguration={'LocationConstraint': 'us-west-1'}
         )
         ```

    b. **Error: InvalidBucketName**  
       While creating the bucket, I encountered an error about the bucket name being invalid because it contained underscores, which are not allowed by AWS.  
       - **Solution:** Replaced underscores with hyphens to make the bucket name valid:
 

17. **Check the S3 Bucket:**
    - Verified that the bucket was created successfully and all configurations were correct.

18. **Clean Up Resources:**
    - Cleaned up any AWS resources, including the S3 bucket, to avoid unnecessary charges.

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


