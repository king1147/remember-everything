#!/bin/bash

set -e

# Configuration
export DOCKER_BUILDKIT=0
export AWS_REGION=eu-central-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME=message-receiver
APP_FUNCTION_NAME=message-receiver-app
MIGRATE_FUNCTION_NAME=message-receiver-migrate
ECR_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME

echo "Starting deployment..."

echo "Building Docker image..."
docker build --platform linux/amd64 -t $REPO_NAME .

echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "Tagging image..."
docker tag $REPO_NAME:latest $ECR_URI:latest

echo "Pushing to ECR..."
docker push $ECR_URI:latest

echo "Updating Migration Lambda..."
aws lambda update-function-code \
    --function-name $MIGRATE_FUNCTION_NAME \
    --image-uri $ECR_URI:latest \
    --region $AWS_REGION \
    --query 'LastUpdateStatus' \
    --output text

echo "Waiting for update to complete..."
aws lambda wait function-updated --function-name $MIGRATE_FUNCTION_NAME

echo "Running database migrations..."
aws lambda invoke \
  --function-name $MIGRATE_FUNCTION_NAME \
  --log-type Tail \
  --query 'StatusCode' \
  --output text \
  response.json

cat response.json
echo ""

echo "Updating App Lambda..."
aws lambda update-function-code \
    --function-name $APP_FUNCTION_NAME \
    --image-uri $ECR_URI:latest \
    --region $AWS_REGION \
    --query 'LastUpdateStatus' \
    --output text

echo "Waiting for update to complete..."
aws lambda wait function-updated --function-name $APP_FUNCTION_NAME

echo "Deployment completed successfully!"