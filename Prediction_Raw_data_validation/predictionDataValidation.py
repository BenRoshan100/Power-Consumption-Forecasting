from datetime import datetime
from os import listdir
import os 
import re 
import json 
import shutil 
import pandas as pd
from application_logging.logger import App_Logger 

class Prediction_Data_validation:

    def __init__(self,path):
        self.Batch_Directory = path 
        self.schema_path='schema_prediction.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
        
            number_of_columns = dic['NumberofColumns']
            first_column_types = dic['Columns']['First_Column']
            
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = f"Total Columns: {number_of_columns}\tExpected First column types: {first_column_types}"
            self.logger.log(file, message)
            file.close()
            return number_of_columns, first_column_types

        except ValueError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "ValueError: Value not found inside schema_training.json")
            file.close()
            raise ValueError
        except KeyError as e:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, f"KeyError: Key {str(e)} not found inside schema_training.json")
            file.close()
            raise KeyError(f"Key {str(e)} not found inside schema_training.json")
        except Exception as e:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        
    def validateColumnLength(self, NoOfColumns):
        log_file_path = "Prediction_Logs/columnValidationLog.txt"
        try:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, "Column Length Validation started successfully")
                for file in listdir(self.Batch_Directory):
                    if file.endswith('.csv'):  
                        try:
                            csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                            if csv.shape[1] != NoOfColumns:
                                self.logger.log(f, f"Invalid Column Length for the file: {file}")
                                return False
                        except OSError as e:
                            self.logger.log(f, f"Error reading the file: {file}, Error: {e}")
                            raise OSError(e)
                        except Exception as e:
                            self.logger.log(f, f"Error processing the file: {file}, Error: {e}")
                            raise e
                self.logger.log(f, "Column Length Validation Completed!")
                return True
        except OSError as e:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, f"Error Occured while accessing the directory: {e}")
            raise OSError(e)
        except Exception as e:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, f"Error Occured: {e}")
            raise e
        
    def validate_column_type(self,column,expected_types):
        actual_type=str(column.dtype)
        if actual_type=='datetime64[ns]':
            actual_type='datetime64'
        elif actual_type=='int64':
            actual_type='int64'
        elif actual_type=='float64':
            actual_type='float64'
        else:
            actual_type='object'

        return actual_type in expected_types
    
    def validateColumnTypes(self, first_column_types):
        log_file_path = "Prediction_Logs/ColumnTypeValidationLog.txt"
        try:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, "Column Type Validation started successfully")
                for file in listdir(self.Batch_Directory):
                    if file.endswith('.csv'): 
                        try:
                            csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                            if not self.validate_column_type(csv.iloc[:, 0], first_column_types):
                                self.logger.log(f, f"Invalid type for first column in file {file}. Expected one of {first_column_types}, got {str(csv.iloc[:, 0].dtype)}")
                        except Exception as e:
                            self.logger.log(f, f"Error processing the file: {file}, Error: {e}")
                            raise e
                self.logger.log(f, "Column Type Validation Completed!")
        except Exception as e:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, f"Error Occured: {e}")
            raise e

    def validateMissingValuesInWholeColumn(self):
        log_file_path = "Prediction_Logs/missingValuesInColumn.txt"
        try:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, "Missing Values Validation Started!!")
                for file in listdir(self.Batch_Directory):
                    if file.endswith('.csv'): 
                        try:
                            csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                            for column in csv.columns:
                                if csv[column].isnull().all():
                                    self.logger.log(f, f"All values missing in column: {column} for file: {file}.")
                                    return False
                        except Exception as e:
                            self.logger.log(f, f"Error processing the file: {file}, Error: {e}")
                            raise e
                self.logger.log(f, "Missing Values Validation Completed!")
            return True
        except OSError as e:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, f"Error occured while accessing the directory: {e}")
            raise OSError(e)
        except Exception as e:
            with open(log_file_path, 'a+') as f:
                self.logger.log(f, f"Error Occured: {e}")
            raise e