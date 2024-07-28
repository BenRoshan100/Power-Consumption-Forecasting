import pandas  
from file_operations import file_methods
from data_preprocessing import preprocessing
from application_logging import logger 
from data_ingestion import data_loader
import os
from Prediction_Raw_data_validation.predictionDataValidation import Prediction_Data_validation

class prediction:
    def __init__(self,path):
        self.file_object=open("Prediction_Logs/Prediction_Log.txt",'a+')
        self.log_writer=logger.App_Logger()
        self.base_path=path
        if path is not None:
            self.pred_data_val=Prediction_Data_validation(path)
    
    def predictionFromModel(self):
        try:
            validation_complete_path=os.path.join(self.base_path,'validation_complete')
            self.log_writer.log(self.file_object,'Start of Prediction')
            data_getter=data_loader.Data_Getter(self.file_object,self.log_writer,validation_complete_path)
            data=data_getter.get_data_predict()
            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)
            columns=data.columns
            first_column=columns[0]
            data=preprocessor.convert_columns(data,first_column)
            if data.iloc[:,0].isnull().sum()>0:
                data=preprocessor.remove_missing_dates(data)

            data=preprocessor.extract_date_features(data)
            categorical_columns=['weekday_name','season','week_type']
            data=preprocessor.ordinal_encode_columns(data,categorical_columns)

            file_loader=file_methods.File_Operation(self.file_object,self.log_writer)
            dates=list(data[first_column])
            xgb_model=file_loader.load_model('XGBoost')
            prophet_model=file_loader.load_model('Prophet')
            numeric_data=data.select_dtypes(include=[float, int, bool])
            xgb_result=list(xgb_model.predict(numeric_data))
            prophet_data = data.rename(columns={first_column: 'ds'})
            future = prophet_model.make_future_dataframe(periods=len(prophet_data))
            forecast = prophet_model.predict(future)
            prophet_result = forecast['yhat'][:len(prophet_data)]
            xgb_final_result=pandas.DataFrame(list(zip(dates,xgb_result)),columns=['Date', 'Forecasts'])
            prophet_final_result=pandas.DataFrame(list(zip(dates,prophet_result)),columns=['Date', 'Forecasts'])
            xgb_final_result.to_csv("Prediction_Output_File/Predictions_XGBoost.csv",header=True,mode='w')
            prophet_final_result.to_csv("Prediction_Output_File/Predictions_Prophet.csv",header=True,mode='w')
            self.log_writer.log(self.file_object,'End of Prediction')
        except Exception as e:
            self.log_writer.log(self.file_object,'Error occurred while running prediction. Error:: %s' %e)
            raise e 
        return xgb_final_result.head(),prophet_final_result.head()


