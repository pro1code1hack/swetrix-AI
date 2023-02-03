import pandas as pd
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

    def fit(self) -> 'Model':
        """
        Fit the model to the data.
        """
        self.model.fit(self.data)
        return self

    def predict(self, period: TimeMetrics) -> pd.DataFrame:
        """
        Predict the future values.
        :param period: The period for which we want to predict the values.
        """
        future = self.model.make_future_dataframe(periods=period.value)
        return self.model.predict(future)

    def plot(self, forecast: pd.DataFrame) -> None:
        """
        Plot the results.
        :param forecast: The forecasted data.
        """
        fig1 = self.model.plot(forecast)
        fig2 = self.model.plot_components(forecast)
        plot_plotly(self.model, forecast)
        plot_components_plotly(self.model, forecast)
        fig1.show()
        fig2.show()
