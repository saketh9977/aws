# Method 1: ECR

## Test Lambda Locally
1. Build image using `bash build_image.sh`
2. Run container using `bash run_container`
3. Send a POST request to test lambda -
```
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"name": "lola"}'
```

## Push to ECR

**Note**: As of today (02 Jan 2022), you can't use an image in ECR's **public** repository from AWS lambda. Only the images that are in **private** repositories are accessible from  AWS lambda.

1. Ensure you created a public ECR repository on AWS ECR
2. Push your image using `bash push_to_ecr.sh`

# Method 2: Zip

## Create zip and push zip
1. Install dependencies to `package` folder using -
```
    pip install -r requirements.txt --target ./package
```
2. Add package to zip arcchive -
```
    zip -r lola-lambda.zip ./package/*
```
3. Check if everything got zipped by extracting the archive to `extracted` -
```
    unzip lola-lambda.zip -d extracted
```
4. Create lambda using AWS UI. On AWS UI, ensure runtime settings of Lambda are configured properly.
    - `Handler` should follow the following pattern: `python_filename.lambda_event_handler_function name`
5. Push zip to AWS -
```
    aws lambda update-function-code --function-name lola-lambda --zip-file fileb://lola-lambda.zip
```

## Test Lambda
Feel free to use AWS Lambda UI editor to test lambda