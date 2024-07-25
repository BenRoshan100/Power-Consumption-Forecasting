from datetime import datetime
from os import listdir
import os 
import re 
import json 
import shutil 
import pandas as pd
from application_logging.logger import App_Logger 

class Raw_Data_validation:

    def __init__(self,path):
        self.Batch_Directory = path 
        self.schema_path='schema_training.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
        
            number_of_columns = dic['NumberofColumns']
            first_column_types = dic['Columns']['First_Column']
            second_column_types = dic['Columns']['Second_Column']
            
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = f"Total Columns: {number_of_columns}\tExpected First column types: {first_column_types}\tExpected Second column types: {second_column_types}\n"
            self.logger.log(file, message)
            file.close()
            return number_of_columns, first_column_types, second_column_types

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "ValueError: Value not found inside schema_training.json")
            file.close()
            raise ValueError
        except KeyError as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, f"KeyError: Key {str(e)} not found inside schema_training.json")
            file.close()
            raise KeyError(f"Key {str(e)} not found inside schema_training.json")
        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        
    def validateColumnLength(self, NoOfColumns):
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column Length Validation started successfully")
            for file in listdir(self.Batch_Directory):
                csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                if csv.shape[1] != NoOfColumns:
                    self.logger.log(f, f"Invalid Column Length for the file: {file}")
                    f.close()
                    return False
            self.logger.log(f, "Column Length Validation Completed!")
            f.close()
            return True
        except OSError as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, f"Error Occured while moving the file: {e}")
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, f"Error Occured: {e}")
            f.close()
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
    
    def validateColumnTypes(self,first_column_types,second_column_types):
        try:
            f=open("Training_Logs/ColumnTypeValidationLog.txt",'a+')
            self.logger.log(f,"Column Type Validation started successfully")
            for file in listdir(self.Batch_Directory):
                csv=pd.read_csv(os.path.join(self.Batch_Directory,file))
                if not self.validate_column_type(csv.iloc[:,0],first_column_types):
                    self.logger.log(f,f"Invalid type for first column in file {file}. Expected one of {first_column_types}, got {str(csv.iloc[:,0].dtype)}")
                if not self.validate_column_type(csv.iloc[:,1],second_column_types):
                    self.logger.log(f,f"Invalid type for second column in file {file}. Expected one of {second_column_types}, got {str(csv.iloc[:,1].dtype)}")
                self.logger.log(f,"Column validation completed")
                f.close()
        except Exception as e:
            f=open("Training_Logs/columnTypeValidationLog.txt", 'a+')
            self.logger.log(f,"Error Occured: {e}")
            f.close()
            raise e

    def validateMissingValuesInWholeColumn(self):
        try:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, "Missing Values Validation Started!!")
            for file in listdir(self.Batch_Directory):
                csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                for column in csv.columns:
                    if csv[column].isnull().all():
                        self.logger.log(f, f"All values missing in column: {column} for file: {file}.")
                        f.close()
                        return False
            self.logger.log(f, "Missing Values Validation Completed!")
            f.close()
            return True
        except OSError as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, f"Error occured while moving file: {e}")
            f.close()
            raise OSError 
        except Exception as e:
            f = open("Training_Logs/missingValuesInColumn.txt", 'a+')
            self.logger.log(f, f"Error Occured: {e}")
            f.close()
            raise e 