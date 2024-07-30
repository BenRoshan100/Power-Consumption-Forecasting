from datetime import datetime
from os import listdir
import os
import json
import pandas as pd
from application_logging.logger import App_Logger

class Raw_Data_validation:

    def __init__(self, path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)

            number_of_columns = dic['NumberofColumns']
            first_column_types = dic['Columns']['First_Column']
            second_column_types = dic['Columns']['Second_Column']

            with open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+') as file:
                message = f"Total Columns: {number_of_columns}\tExpected First column types: {first_column_types}\tExpected Second column types: {second_column_types}\n"
                self.logger.log(file, message)

            return number_of_columns, first_column_types, second_column_types

        except ValueError:
            with open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+') as file:
                self.logger.log(file, "ValueError: Value not found inside schema_training.json")
            raise ValueError
        except KeyError as e:
            with open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+') as file:
                self.logger.log(file, f"KeyError: Key {str(e)} not found inside schema_training.json")
            raise KeyError(f"Key {str(e)} not found inside schema_training.json")
        except Exception as e:
            with open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+') as file:
                self.logger.log(file, str(e))
            raise e

    def validateColumnLength(self, NoOfColumns):
        try:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Column Length Validation started successfully")
                for file in [f for f in listdir(self.Batch_Directory) if f.endswith('.csv')]:
                    csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                    if csv.shape[1] != NoOfColumns:
                        self.logger.log(f, f"Invalid Column Length for the file: {file}")
                        return False
                self.logger.log(f, "Column Length Validation Completed!")
            return True
        except OSError as e:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, f"Error Occured while moving the file: {e}")
            raise OSError
        except Exception as e:
            with open("Training_Logs/columnValidationLog.txt", 'a+') as f:
                self.logger.log(f, f"Error Occured: {e}")
            raise e

    def validate_column_type(self, column, expected_types):
        actual_type = str(column.dtype)
        if actual_type == 'datetime64[ns]':
            actual_type = 'datetime64'
        elif actual_type == 'int64':
            actual_type = 'int64'
        elif actual_type == 'float64':
            actual_type = 'float64'
        else:
            actual_type = 'object'

        return actual_type in expected_types

    def validateColumnTypes(self, first_column_types, second_column_types):
        try:
            with open("Training_Logs/ColumnTypeValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Column Type Validation started successfully")
                for file in [f for f in listdir(self.Batch_Directory) if f.endswith('.csv')]:
                    csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                    if not self.validate_column_type(csv.iloc[:, 0], first_column_types):
                        self.logger.log(f, f"Invalid type for first column in file {file}. Expected one of {first_column_types}, got {str(csv.iloc[:, 0].dtype)}")
                    if not self.validate_column_type(csv.iloc[:, 1], second_column_types):
                        self.logger.log(f, f"Invalid type for second column in file {file}. Expected one of {second_column_types}, got {str(csv.iloc[:, 1].dtype)}")
                self.logger.log(f, "Column validation completed")
        except Exception as e:
            with open("Training_Logs/columnTypeValidationLog.txt", 'a+') as f:
                self.logger.log(f, "Error Occured: {e}")
            raise e

    def validateMissingValuesInWholeColumn(self):
        try:
            with open("Training_Logs/missingValuesInColumn.txt", 'a+') as f:
                self.logger.log(f, "Missing Values Validation Started!!")
                for file in [f for f in listdir(self.Batch_Directory) if f.endswith('.csv')]:
                    csv = pd.read_csv(os.path.join(self.Batch_Directory, file))
                    for column in csv.columns:
                        if csv[column].isnull().all():
                            self.logger.log(f, f"All values missing in column: {column} for file: {file}.")
                            return False
                self.logger.log(f, "Missing Values Validation Completed!")
            return True
        except OSError as e:
            with open("Training_Logs/missingValuesInColumn.txt", 'a+') as f:
                self.logger.log(f, f"Error occured while moving file: {e}")
            raise OSError
        except Exception as e:
            with open("Training_Logs/missingValuesInColumn.txt", 'a+') as f:
                self.logger.log(f, f"Error Occured: {e}")
            raise e
