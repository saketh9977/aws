set -e

local_image_name='s3-etl:v1'

# step-1: create ECR repository using AWS console
# step-2: open the repository created on AWS console & select 'view push commands' - the following commands -

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r4a0e7l4
docker tag $local_image_name public.ecr.aws/r4a0e7l4/ecr_repo_4536:latest
docker push public.ecr.aws/r4a0e7l4/ecr_repo_4536:latest

# now, follow ecs_setup.txt
