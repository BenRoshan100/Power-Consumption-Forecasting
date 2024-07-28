import pickle 
import os 
import shutil 

class File_Operation:
    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object 
        self.model_directory = 'models/'

    def save_model(self,model1,filename1,model2,filename2):
        self.logger_object.log(self.file_object,'Entered the save_model method of the File_Operation class')
        try:
            path=os.path.join(self.model_directory,filename1)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path+'/'+filename1+'.sav','wb') as f:
                pickle.dump((model1),f)
            self.logger_object.log(self.file_object,'Model File'+filename1+' saved. Exited the save_model method of the Model_Finder class')


            path=os.path.join(self.model_directory,filename2)
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path+'/'+filename2+'.sav','wb') as f:
                pickle.dump((model2),f)
            self.logger_object.log(self.file_object,'Model File'+filename2+' saved. Exited the save_model method of the Model_Finder class')

            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in save_model method of the Model_Finder class. Exception message: '+str(e))
            raise Exception()
    
    def find_correct_model_file(self):
        self.logger_object.log(self.file_object,'Entered the find_correct_model_file method of the Model_Finder class.')
        try:
            self.folder_name=self.model_directory
            self.model_name = None 
            for self.file in os.listdir(self.folder_name):
                self.model_name=self.file
            self.model_name = self.model_name.rsplit('.', 1)[0]
            self.logger_object.log(self.file_object, 'Exited the find_correct_model_file method of Model Finder class.')
            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,'Exeption occurred in find_correct_model_file method of Model Finder class. Exception: '+str(e))
            self.logger_object.log(self.file_object,'Exited the find_correct_model_file method of Model Finder class with failure.')
            raise Exception()
            
        
    def load_model(self,filename):
        print(f'Checking filename: {filename}')
        self.logger_object.log(self.file_object,'Entered the load_model method of the File_Operation class')
        try:
            with open(self.model_directory+filename+'/'+filename+'.sav','rb') as f:
                self.logger_object.log(self.file_object,'Model File'+ filename +'loaded. Exited the load_model method of Model_Finder class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in load_model method of Model_Finder class.Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Model File'+ filename+ ' could not be loaded. Exited the load_model method of Model_Finder class')
            raise Exception()