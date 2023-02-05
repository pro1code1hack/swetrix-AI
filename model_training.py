import pandas as pd
from matplotlib import pyplot
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from enums import TimeMetrics


class Model:
    def __init__(self, data: pd.DataFrame):
        """
        The main class for the data processing.
        Here we will process the data and prepare it for the Prophet model which we also create.
        :param data:
        """
        self.data = data
        self.model = Prophet()

    def train(self):
        # fit the model
        self.model.fit(self.data)
        self.model.plot(self.model.predict(self.data))

        plot_plotly(self.model, self.model.predict(self.data))
        plot_components_plotly(self.model, self.model.predict(self.data))
        # make a prediction

        # SOLUTION! freq = 'H' - hourly -> it means that we want to predict the next 48 hours each hour
        """
        212 2023-02-04 20:00:00  31.843344  -13.115634   74.989653
        """
        future = self.model.make_future_dataframe(periods=48, freq='H')
        forecast = self.model.predict(future)
        # summarize the forecast
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # plot forecast
        self.model.plot(forecast)
        pyplot.show()
        # plot forecast components
        self.model.plot_components(forecast)
        pyplot.show()

