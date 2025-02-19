import pandas as pd
import os

class Data_Getter:

    def __init__(self,file_object,logger_object,path):
        self.training_file_path= path
        self.prediction_file_path= path
        self.file_object =file_object
        self.logger_object = logger_object

    def get_data_train(self):

        self.logger_object.log(self.file_object, 'Entered the get_data method of Data_Getter class')
        try: 
            data=pd.DataFrame()

            for file in os.listdir(self.training_file_path):
                if file.endswith('.csv'):
                    file_path=os.path.join(self.training_file_path, file)

                    df=pd.read_csv(file_path)
                    data=pd.concat([data,df],ignore_index=True)

            self.logger_object.log(self.file_object,'Data Load successfully')
            return data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occued in get_data method of Data_Getter class. Exception message:'+str(e))
            self.logger_object.log(self.file_object,'Data Load Unsuccessful. Exited get_data method of Data_Getter class.')
            raise Exception()
        
    def get_data_predict(self):

        self.logger_object.log(self.file_object, 'Entered the get_data method of Data_Getter class for Prediction')
        try: 
            data=pd.DataFrame()

            for file in os.listdir(self.prediction_file_path):
                if file.endswith('.csv'):
                    file_path=os.path.join(self.prediction_file_path, file)

                    df=pd.read_csv(file_path)
                    data=pd.concat([data,df],ignore_index=True)
            self.logger_object.log(self.file_object, 'Data Load successful for Prediction. Exited the get_data method of Data_Getter class')
            return data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occued in get_data method of Data_Getter class. Exception message:'+str(e))
            self.logger_object.log(self.file_object,'Data Load Unsuccessful. Exited get_data method of Data_Getter class.')
            raise Exception()