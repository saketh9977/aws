# authenticate to ECR
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/u4m6w6n1

# build image locally
docker build -t lola .

# tag image
docker tag lola:latest public.ecr.aws/u4m6w6n1/lola:latest

# push image to ECR
docker push public.ecr.aws/u4m6w6n1/lola:latest