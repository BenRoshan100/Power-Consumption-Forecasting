from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import pandas as pd
from prophet import Prophet

class Model_Trainer:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.xgb = xgb.XGBRegressor(objective='reg:squared_error')
        self.prophet = Prophet()

    def get_best_params_for_xgboost(self, train_x, train_y):
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_xgboost function')
        try:
            param_grid_xgboost = {
                'learning_rate': [0.01, 0.1, 0.2, 0.3],
                'max_depth': [3, 5, 7, 10],
                'n_estimators': [50, 100, 200, 300]
            }

            grid = GridSearchCV(xgb.XGBRegressor(objective='reg:squarederror'), param_grid_xgboost, verbose=3, cv=5)
            grid.fit(train_x, train_y)

            self.learning_rate = grid.best_params_['learning_rate']
            self.max_depth = grid.best_params_['max_depth']
            self.n_estimators = grid.best_params_['n_estimators']

            self.xgb = xgb.XGBRegressor(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            self.xgb.fit(train_x, train_y)

            self.logger_object.log(self.file_object, 'XGBoost best params: ' + str(grid.best_params_) + '. Exited the get_best_params_for_xgboost function')
            return self.xgb
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_params_for_xgboost method of Model_Finder: ' + str(e))
            self.logger_object.log(self.file_object, 'XGBoost parameter tuning failed. Exited the get_best_params_for_xgboost method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_prophet(self, df):
        self.logger_object.log(self.file_object, 'Entered the get_best_params_for_prophet function')
        try:
            df = df.rename(columns={df.columns[0]: 'ds', df.columns[1]: 'y'})
            prophet_model = Prophet()
            prophet_model.fit(df)
            self.logger_object.log(self.file_object, 'Prophet model trained. Exited the function')
            return prophet_model
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_params_for_prophet method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Prophet parameter tuning failed. Exited the get_best_params_for_prophet method of the Model_Finder class')
            raise Exception()

    def get_trained_model(self, X_train, y_train, X_test, y_test, df_prophet):
        self.logger_object.log(self.file_object, 'Entered get_best_model method of the Model_Finder class')
        try:
            # Ensure only numeric columns are used for XGBoost
            X_train_numeric = X_train.select_dtypes(include=[float, int, bool])
            X_test_numeric = X_test.select_dtypes(include=[float, int, bool])

            # Train XGBoost model
            xgboost = self.get_best_params_for_xgboost(X_train_numeric, y_train)
            y_pred_xgboost = xgboost.predict(X_test_numeric)
            xgboost_mse = mean_squared_error(y_test, y_pred_xgboost)
            self.logger_object.log(self.file_object, 'MSE for XGBoost: ' + str(xgboost_mse))

            # Train Prophet model
            df_prophet = df_prophet.rename(columns={df_prophet.columns[0]: 'ds', df_prophet.columns[1]: 'y'})
            prophet_model = self.get_best_params_for_prophet(df_prophet)
            future = prophet_model.make_future_dataframe(periods=len(X_test))
            forecast = prophet_model.predict(future)

            # Return both models and their names
            return xgboost, 'XGBoost', prophet_model, 'Prophet'
        except Exception as e:
            self.logger_object.log(self.file_object, 'Exception occurred in get_best_model method of the Model_Finder class. Exception message: ' + str(e))
            self.logger_object.log(self.file_object, 'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()