import pickle
from flask import Flask, request, jsonify
import os

#Load the model from the MlFlow Registry :
import mlflow
import boto3
import logging


#Local MLFlow Server
#mlflow.set_tracking_uri("http://127.0.0.1:5000")
#run_id = '410d302e047e4a389cd0ad29458f327c'

# Ensure AWS credentials are set
os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_key'
os.environ['AWS_REGION'] = 'your_region'  # Replace with your region

session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_REGION']
)
# Example: Using the session to create a client
s3_client = session.client('s3')

run_id = '845b2d40804f423bb03fdc81565f9598'
logged_model = f's3://mlflow-flask-adocker-artifacts/1/{run_id}/artifacts/models'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

def prepare_feature(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']

    return features

def predict(features):
    preds = model.predict(features)    
    return float(preds[0])

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_feature(ride)
    pred = predict(features)
    result = {
        'duration' : pred,
        'model_version' : run_id
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
    #serve(app, host='0.0.0.0', port=9696)
