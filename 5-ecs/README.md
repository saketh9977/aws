### What is this?
Package your ETL in a docker image and run your ETL docker container on AWS ECS as a task

### Local Testing & Deployment:
1. Build docker image using - `bash build_image.sh`
2. Test it by running container locally using - `bash run_container.sh`
3. Follow steps in ecr_push.sh to push image to ECR and to setup ECS to run task
4. Task Logs can be seen on CloudWatch LogGroups
