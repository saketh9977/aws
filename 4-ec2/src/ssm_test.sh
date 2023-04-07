set -e

echo "ssm_test.sh: starting..."

date
pwd
aws s3 ls s3://test-4323/
date

echo "ssm_test.sh: ending..."