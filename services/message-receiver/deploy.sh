#!/bin/bash

set -e

# Configuration
export DOCKER_BUILDKIT=0
export AWS_REGION=eu-central-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME=message-receiver
FUNCTION_NAME=message-receiver-app

echo "Starting deployment..."

echo "Building Docker image..."
docker build --platform linux/amd64 -t $REPO_NAME .

echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "Tagging image..."
docker tag $REPO_NAME:latest \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

echo "Pushing to ECR..."
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest

echo "Updating Lambda function..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest \
    --region $AWS_REGION

echo "Waiting for update to complete..."
aws lambda wait function-updated --function-name $FUNCTION_NAME

echo "Deployment completed successfully!"