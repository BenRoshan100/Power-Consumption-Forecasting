from wsgiref import simple_server
from flask import Flask, request, render_template, Response, jsonify
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
dashboard.bind(app)
CORS(app)

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json and 'folderPath' in request.json:
            path = request.json['folderPath']
        else:
            return Response("Invalid input format", status=400)
        
        train_valObj = train_validation(path)
        train_valObj.train_validation()
        trainModelObj = trainModel()
        trainModelObj.trainingModel()
        return Response("Training successful")
    except ValueError as ve:
        return Response("Error Occurred! %s" % ve, status=500)
    except KeyError as ke:
        return Response("Error Occurred! %s" % ke, status=500)
    except Exception as e:
        return Response("Error Occurred! %s" % e, status=500)

@app.route("/predict", methods=["POST"])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
        elif request.form is not None:
            path = request.form['filepath']
        else:
            return Response("Invalid input format", status=400)
        
        pred_val = pred_validation(path)
        pred_val.prediction_validation()
        pred = prediction(path)
        xgboost_predictions, prophet_predictions = pred.predictionFromModel()
        
        # Get sample records
        xgboost_sample = xgboost_predictions.head(5).to_dict(orient='records')
        prophet_sample = prophet_predictions.head(5).to_dict(orient='records')
        
        # Convert to JSON
        xgboost_json = xgboost_predictions.to_json(orient='records')
        prophet_json = prophet_predictions.to_json(orient='records')
        
        response_data = {
            'xgboost': json.loads(xgboost_json),
            'prophet': json.loads(prophet_json),
            'xgboost_sample': xgboost_sample,
            'prophet_sample': prophet_sample
        }
        
        return jsonify(response_data)
    except ValueError as ve:
        return Response("Error Occurred! %s" % ve, status=500)
    except KeyError as ke:
        return Response("Error Occurred! %s" % ke, status=500)
    except Exception as e:
        return Response("Error Occurred! %s" % e, status=500)

port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
