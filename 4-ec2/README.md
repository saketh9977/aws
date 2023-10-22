## What is this?
A Python script that -
1. Launches an EC2 instance. Ensures EC2 is up by polling until its state is `running`
    - You can specifiy AMI-ID, while launching EC2 where custom software/libraries are setup for EC2 eg. `gsutil` installation & setup
2. Ensures SSM agent is running on EC2 instance by polling until SSM agent is `Online` on the EC2
    - SSM agent listens for incoming commands and executes them
3. Executes a "shell script located on S3" on EC2 instance using "SSM agent running on EC2".
4. Can also execute a list of bash commands passed as Python args (instead of having a shell script on s3)
5. Stores execution logs on S3.
6. Terminates EC2. Ensures EC2 is terminated by polling until EC2 state is `Terminated`

## Use Case
Transfer 2 TB data from AWS S3 bucket to Google Cloud's GS bucket using `gsutil` command.