
sending stream event data:

KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data $(echo -n "Hello, this is a test." | base64)




event-test:
{
  "Records": [
    {
      "kinesis": {
        "kinesisSchemaVersion": "1.0",
        "partitionKey": "1",
        "sequenceNumber": "49655025671936332063224864712602408900080021025432010802",
        "data": "eyJyaWRlX2lkIjogIjEyMzQ1IiwgInJpZGUiOiB7IlBVbG9jYXRpb25JRCI6ICIxMDAiLCAiRE9Mb2NhdGlvbklEIjogIjIwMCIsICJ0cmlwX2Rpc3RhbmNlIjogIjEyLjUifX0=",
        "approximateArrivalTimestamp": 1724076292.024
      },
      "eventSource": "aws:kinesis",
      "eventVersion": "1.0",
      "eventID": "shardId-000000000003:49655025671936332063224864712602408900080021025432010802",
      "eventName": "aws:kinesis:record",
      "invokeIdentityArn": "arn:aws:iam::905418253593:role/lambda-kinesis-role",
      "awsRegion": "eu-north-1",
      "eventSourceARN": "arn:aws:kinesis:eu-north-1:905418253593:stream/ride_events"
    }
  ]
}




sample test for reading another stream:


KINESIS_STREAM_OUTPUT='ride-prediction'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode


### Putting everything to Docker
docker build -t stream-model-duration:v1 .

winpty docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride-prediction" \
    -e RUN_ID="845b2d40804f423bb03fdc81565f9598" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-north-1" \
    -e AWS_PROFILE="myawsprofile" \
    -v /c/Users/aksha/.aws:/root/.aws \
    stream-model-duration:v1


 ### Create test-docker.py

### Publish docker image to ECR
1. Creating an ECR repo:
aws ecr create-repository --repository-name duration-model

2. logging-in:
$(aws ecr get-login --no-include-email)

aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 905418253593.dkr.ecr.eu-north-1.amazonaws.com

3. pushing local docker image to ecr container registry:

REMOTE_URI="905418253593.dkr.ecr.eu-north-1.amazonaws.com/duration-model"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-duration:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}

### Test new lambda using below test event:
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data $(echo -n '{
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        }, 
        "ride_id": 156
    }' | base64)

4. attach policy to lambda IAM role to have read and list permission of s3 bucket
