import lambda_function



event = {
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


result = lambda_function.lambda_handler(event, None)
print(result)
