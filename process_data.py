from typing import Optional

import pandas as pd
from enums import Fields, TimeMetrics


class Reader:
    """
    The class for reading the data from the json file.
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def read_json(self) -> Optional[pd.DataFrame]:
        try:
            return pd.read_json(self.path)
        except Exception as e:
            # TODO log error
            print(e)
            return None


class Data:

    def __init__(self, original_data: pd.DataFrame):
        """
        The main class for the data processing.
        Here we will process the data and prepare it for the Prophet model.
        As it requires the data in a specific format, we need to clean it up and prepare it for the model.

        :param original_data: The original data from the json file.
        """
        self.original_data = original_data
        """
        yhat - The forecasted value of our metric (y) at the date (ds)
        yhat_lower - The lower bound of our forecasts
        yhat_upper - The upper bound of our forecasts

        По факту, мы можем использовать yhat_lower и yhat_upper для того, чтобы понять, насколько точны наши прогнозы.
        Если yhat_lower и yhat_upper находятся в пределах y, то  можем сказать, что прогноз точный.
        
                    ds       yhat  yhat_lower  yhat_upper
        171 2023-02-06  27.454010   -9.117108   62.349224
        172 2023-02-07  29.463093   -6.959259   64.551996
        173 2023-02-08  31.472177   -3.982182   63.477517
        174 2023-02-09  33.481260   -1.747542   67.575251
        175 2023-02-10  35.490343    0.355324   68.711358
        """
        self.processed_data = pd.DataFrame()

    def create_ds_column(self) -> 'Data':
        """
        The ds column must be present and named ds. It represents the time.
        """
        self.original_data['x'] = self.processed_data['ds'] = pd.to_datetime(self.original_data['x'])
        return self

    def create_y_column(self, y_column: 'Fields') -> 'Data':
        """
        The y column must be numeric, and represents the measurement we wish to forecast.
        #TODO 1.Maybe it is better to use float instead of int.
        #TODO 2. How to iterate over the list of fields? Maybe we can use the enum class for that and iterate over it,
        #TODO but it breaks the logic of the class and SOLID principles.
        """
        self.original_data[y_column.value] = self.processed_data['y'] = self.original_data[y_column.value].astype(float)
        return self
