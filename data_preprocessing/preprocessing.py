import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

class Preprocessor:

    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object =logger_object