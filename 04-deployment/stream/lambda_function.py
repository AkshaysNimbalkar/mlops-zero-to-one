import json
import base64
import boto3
import os
import mlflow
import traceback

kinesis_client = boto3.client('kinesis')
PREDICTION_STREAM_NAME = os.getenv('PREDICTION_STREAM_NAME', 'ride-prediction')

run_id = os.getenv('run_id', '845b2d40804f423bb03fdc81565f9598')
logged_model = f's3://mlflow-flask-adocker-artifacts/1/{run_id}/artifacts/models'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    if 'PULocationID' in ride and 'DOLocationID' in ride:
        features = {
            'PU_DO' : f"{ride['PULocationID']}_{ride['DOLocationID']}",
            'trip_distance' : ride.get('trip_distance', 0)
        }
  
    else:
        features = {
            'PU_DO': "Unknown_PU_DO",
            'trip_distance': ride.get('trip_distance', 0)
        }
        
    return features

def predict(features):
    pred = model.predict(features)
    return float(pred[0])

def lambda_handler(event, context):
    prediction_events = []
    
    for record in event['Records']:
        try:
            encoded_data = record['kinesis']['data']
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            ride_event = json.loads(decoded_data)
            
            ride = ride_event['ride']
            ride_id = ride_event['ride_id']
            
            features = prepare_features(ride)
            prediction = predict(features)
            
            prediction_event = {
                'model': 'ride_duration_prediction',
                'version': '123',
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
            }
            
            response = kinesis_client.put_record(
                StreamName=PREDICTION_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)
            )
            
            prediction_events.append(prediction_event)

        except Exception as e:
            print(f"Error processing record {record}: {str(e)}")
            traceback.print_exc()  # Provides a stack trace which is helpful for debugging

    return {
        "prediction": prediction_events
    }