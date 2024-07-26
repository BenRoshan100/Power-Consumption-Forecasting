import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder

class Preprocessor:

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object =logger_object
    
    def convert_columns(self,data,date_column,float_column):
        self.logger_object.log(self.file_object,'Started converting datatypes of columns')
        try:
            data[date_column]=pd.to_datetime(data[date_column],format='%Y-%m-%d %H:%M:%S',errors='coerce')
            data[float_column]=data[float_column].astype(float)
            self.logger_object.log(self.file_object,'Successfully converted columns to appropriate format')
            return data
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in converting columns' + str(e))
            raise e
        
    def remove_missing_dates(self,data):
        self.logger_object.log(self.file_object,'Started removing records with missing dates')
        try:
            data=data.dropna(subset=[data.columns[0]])
            self.logger_object.log(self.file_object,'Successfully removed records with no dates')
            return data 
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in removing records with no dates')
            raise e 
    
    def impute_missing_values(self,data):
        self.logger_object.log(self.file_object,'Started imputing missing values')
        try:
            data.iloc[:,1]=data.iloc[:,1].fillna(methods='ffill')
            self.logger_object.log(self.file_object,'Successfully imputed missing values')
            return data
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in imputing missing values')
            raise e
    
    def extract_date_features(self,data):
        self.logger_object.log(self.file_object,'Started extracting date features')
        try:
            data['date'] = data.iloc[:, 0].dt.date
            data['day'] = data.iloc[:, 0].dt.day
            data['month'] = data.iloc[:, 0].dt.month
            data['year'] = data.iloc[:, 0].dt.year
            data['hour'] = data.iloc[:, 0].dt.hour
            data['weekday_name'] = data.iloc[:, 0].dt.day_name()
            data['season'] = data['month'].apply(self.get_season)
            data['quarter'] = data.iloc[:, 0].dt.quarter
            data['week_of_year'] = data.iloc[:, 0].dt.isocalendar().week
            data['day_of_year'] = data.iloc[:, 0].dt.dayofyear
            data['week_type'] = data.iloc[:, 0].dt.weekday.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
            self.logger_object.log(self.file_object,'Successfully extracted data features')
            return data
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in extracting date features'+str(e))
            raise e 
        
    def ordinal_encode_columns(self,data,columns):
        self.logger_object.log(self.file_object,'Start ordinal encoding')
        try:
            encoder=OrdinalEncoder()
            data[columns]=encoder.fit_transform(data[columns])
            self.logger_object.log(self.file_object,'Successfully ordinal encoded the columns')
            return data,encoder 
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in ordinal encoding'+str(e))
            raise e 
        
    def split_features_labels(self,data,label_column):
        self.logger_object.log(self.file_object,'Started splitting features and labels')
        try:
            X=data.drop(columns=[label_column])
            y=data[label_column]
            self.logger_object.log(self.file_object,'Successfully split features and label')
            return X,y 
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in splitting features and labels' +str(e))
            raise e 
        
    def train_test_split(self,X,y,test_size=0.2,random_state=42):
        self.logger_object.log(self.file_object,'Started train-test split')
        try:
            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=test_size,random_state=random_state)
            self.logger_object.log(self.file_object,'Successfully completed train-test split')
            return X_train,X_test,y_train,y_test
        except Exception as e:
            self.logger_object.log(self.file_object,'Error in train-test split:'+str(e))
            raise e 
        
    @staticmethod 
    def get_season(month):
        if month in [12,1,2]:
            return 'Winter'
        elif month in [3,4,5]:
            return 'Spring'
        elif month in [6,7,8]:
            return 'Summer'
        else:
            return 'Autumn'