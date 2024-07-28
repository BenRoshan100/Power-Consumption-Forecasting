from sklearn.model_selection import train_test_split
from application_logging import logger
from data_preprocessing import preprocessing
from best_model_finder import tuner
from file_operations import file_methods
import os
from data_ingestion import data_loader

class trainModel:
    
    def __init__(self,path):
        self.log_writer=logger.App_Logger()
        self.file_object=open("Training_Logs/ModelTrainingLog.txt",'a+')
        self.base_path=path
    
    def trainingModel(self):
        self.log_writer.log(self.file_object,'Start of training')
        try:
            validation_complete_path=os.path.join(self.base_path,'validation_complete')
            data_getter=data_loader.Data_Getter(self.file_object,self.log_writer,validation_complete_path)
            data=data_getter.get_data_train()
            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)

            columns=data.columns
            if len(columns)<2:
                raise ValueError("Insufficient number of columns")
            
            first_column=columns[0]
            second_column=columns[1]

            data=preprocessor.convert_columns(data,first_column,second_column)
            if data.iloc[:,0].isnull().sum()>0:
                data=preprocessor.remove_missing_dates(data)
            if data.iloc[:,1].isnull().sum()>0:
                data=preprocessor.impute_missing_values(data)


            data=preprocessor.extract_date_features(data)

            categorical_columns=['weekday_name','season','week_type']
            data=preprocessor.ordinal_encode_columns(data,categorical_columns)

            label_column=data.columns[1]
            X,y=preprocessor.split_features_labels(data,label_column)

            X_train,X_test,y_train,y_test=preprocessor.train_test_split(X,y)
            self.log_writer.log(self.file_object,'Data preprocessing completed successfully')
            
            """Model Training starts here"""

            model_trainer=tuner.Model_Trainer(self.file_object,self.log_writer)
            df_prophet=data[[first_column,second_column]]
            xgboost_model,model_name1,prophet_model,model_name2=model_trainer.get_trained_model(X_train,y_train,X_test,y_test,df_prophet)
            
            file_op=file_methods.File_Operation(self.file_object,self.log_writer)

            save_model=file_op.save_model(xgboost_model,model_name1,prophet_model,model_name2)
            
            self.log_writer.log(self.file_object,'Successful End of Training')
            self.file_object.close()
        
        except Exception as e:
            self.log_writer.log(self.file_object,'Unsuccessful End of Training')
            self.file_object.close()
            raise e