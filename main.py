from wsgiref import simple_server
from flask import Flask, request, render_template, Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from training_Validation_Insertion import train_validation
from trainingModel import trainModel
import json

path='D:\ACADEMIC\ML Projects\Power Consumption Forecasting\Training_Raw_file'
#train_valObj = train_validation(path)
#train_valObj.train_validation()
trainModelObj = trainModel(path)
trainModelObj.trainingModel()
# os.putenv('LANG', 'en_US.UTF-8')
# os.putenv('LC_ALL', 'en_US.UTF-8')

# app = Flask(__name__)
# dashboard.bind(app)
# CORS(app)

# @app.route("/", methods=["GET"])
# @cross_origin()
# def home():
#     return render_template('index.html')

# @app.route("/train", methods=['POST'])
# @cross_origin()
# def trainRouteClient():
#     try:
#         if request.json and 'folderPath' in request.json:
#             path = request.json['folderPath']
#         else:
#             return Response("Invalid input format", status=400)
        
#         train_valObj = train_validation(path)
#         train_valObj.train_validation()
#         trainModelObj = trainModel()
#         trainModelObj.trainingModel()
#         return Response("Training successful")
#     except ValueError as ve:
#         return Response("Error Occurred! %s" % ve, status=500)
#     except KeyError as ke:
#         return Response("Error Occurred! %s" % ke, status=500)
#     except Exception as e:
#         return Response("Error Occurred! %s" % e, status=500)

# port = int(os.getenv("PORT", 5000))
# if __name__ == "__main__":
#     host = '0.0.0.0'
#     httpd = simple_server.make_server(host, port, app)
#     httpd.serve_forever()
