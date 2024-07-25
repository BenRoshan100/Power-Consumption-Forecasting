from sklearn.model_selection import train_test_split
from application_logging import logger
from data_preprocessing import preprocessing
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
        
        except Exception as e:
            self.log_writer.log(self.file_object,'Unsuccessful End of Training')
            self.file_object.close()
            raise e