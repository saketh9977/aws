# What does it do?
1. Queries S3 to fetch a json file containing list of pincodes.
2. For each pincode, it queries [this REST API](https://api.postalpincode.in/pincode/110020) to fetch the following details -
    - area name
    - circle
    - district
    - state
    - country
3. The transformed data along with timestamp is stored in DynamoDB
4. It uses an ECS cluster with an EC2 instance which pulls docker image from ECR.

# How to test it locally?
## Prerequisites
1. A json file on S3 containing list of pincodes
2. AWS CLI setup using `aws configure`
## Test
1. **Method 1**:
   1. Install packages using `pip install -r requirements.txt`
   2. Run `python3 app.py`
2. **Method 2**:
   1. Build docker image using `docker build -t test-ecs-ec2 .`
   2. Run the container using `docker run --name test23 -d test-ecs-ec2`.
   3. Check container logs using `docker logs test23`

# Deployment
You can either use "cloudformation" or "manage resources manually" as follows -
1. Create a repository in AWS ECR
2. Click `view push commands` and follow the steps to -
    1. Build an image locally
    2. Tag it to the repository created in step 1
    3. Push image to this repository
3. Create an ECS cluster using an EC2 instance
4. Create a task definition by attaching the above ECR image, specifying CPU, memory requirements etc.
5. You can either -
   1. Run a task: ECS -> `Clusters` in left-panel -> `Tasks` tab -> `Run New Task` button
   2. Schedule a task: ECS -> `Clusters` in left-panel -> `Scheduled Tasks` tab -> `Create` button -> enter a `Cron expression`
6. Prerequisites:
    1. EC2 instance in ECS cluster should have necessary policies in "IAM role (attached to EC2)" to access S3 & DynamoDB
    2. A json file on S3 containing list of pincodes
7. Delete the AWS resources created, if you no longer need them.
