# local testing
docker run \
	-v ~/.aws:/runtime/.aws \
	-e AWS_CONFIG_FILE=/runtime/.aws/credentials \
	--name c_ecs \
	--rm \
	s3-etl:v1
