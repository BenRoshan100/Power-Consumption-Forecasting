from datetime import datetime 
from Prediction_Raw_data_validation.predictionDataValidation import Prediction_Data_validation
from application_logging import logger
import os 
import shutil 


class pred_validation:
    def __init__(self,path):
        self.raw_data=Prediction_Data_validation(path)
        self.file_object=open("Prediction_Logs/Prediction_Main_log.txt",'a+')
        self.log_writer=logger.App_Logger() 
    
    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object,'Start of Validation files!')

            NoOfColumns,FirstColumnTypes=self.raw_data.valuesFromSchema()

            if not self.raw_data.validateColumnLength(NoOfColumns):
                self.log_writer.log(self.file_object,'Column length validation failed')
                return

            if not self.raw_data.validateMissingValuesInWholeColumn():
                self.log_writer.log(self.file_object,'Missing values in entire volumn')
                return
            
            self.raw_data.validateColumnTypes(FirstColumnTypes)
            
            validation_complete_dir = os.path.join(self.raw_data.Batch_Directory, "validation_complete")
            if not os.path.exists(validation_complete_dir):
                os.makedirs(validation_complete_dir)
            

            for file in os.listdir(self.raw_data.Batch_Directory):
                if file != "validation_complete":
                    shutil.copy(os.path.join(self.raw_data.Batch_Directory, file), validation_complete_dir)
            
            self.log_writer.log(self.file_object, 'Validation completed and files copied to validation_complete folder.')

        except Exception as e:
            raise e