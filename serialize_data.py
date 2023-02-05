# TODO add hourly data
from dataclasses import Field

import pandas as pd
from json import dumps
from datetime import datetime


class Serializer:
    # TODO daily
    def __init__(self):
        """
        #TODO think how to serialize data in a better(efficient) way
        """
        self.period_data = {}
        self.hourly_data = {}

    def append_for_period(self, field, data: pd.DataFrame):
        data = data.rename(columns={'ds': 'x', 'yhat': field.value}, inplace=False)[['x', field.value]]
        if 'x' not in self.period_data:
            self.period_data['x'] = data['x'].apply(datetime.strftime, format="%Y-%m-%d %H:%M:%S").values.tolist()
        self.period_data[field.value] = data[field.value].apply(round, 1).values.tolist()

    def append_daily(self, field, data: pd.DataFrame):
        data = data.rename(columns={'ds': 'x', 'yhat': field.value}, inplace=False)[['x', field.value]]
        if 'x' not in self.period_data:
            self.period_data['x'] = data['x'].apply(datetime.strftime, format="%Y-%m-%d").values.tolist()
        self.period_data[field.value] = data[field.value].apply(round, 1).values.tolist()

    def get_json(self):
        return dumps(self.period_data)
