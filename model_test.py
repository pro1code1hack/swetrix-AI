import pandas as pd
from matplotlib import pyplot
from numpy import sqrt
from pandas import to_datetime
# Path: model_training.py

from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from enums import Fields, TimeMetrics
from model_training import Model
from process_data import Data, Reader


def test():
    """
    #TODO: Розбити часовий ряд на тренувальну та тестову вибірки (train/test split)
    #TODO: на тестовой выборке нужно оттестировать модель, а на тренировочной(обученой) - обучить
    #TODO: посчитать метрики качества модели
    По факту это тестовая функция, которая будет использоваться для тестирования модели.
    :return:
    """
    data_json = Reader('data.json').read_json()
    df = pd.DataFrame(data_json)

    train = pd.DataFrame()
    train['ds'] = to_datetime(df['x'])

    for field in Fields:
        if field == Fields.x:
            continue
        train['y'] = df[field.value]
        model = Prophet()
        model.fit(train)
        forecast = model.predict(train)
        y_true = df[field.value].values
        y_pred = forecast['yhat'].values
        mae = mean_absolute_error(y_true, y_pred)
        print('MAE: %.3f' % mae)
        mse = mean_squared_error(y_true, y_pred)
        print('MSE: %.3f' % mse)
        rmse = sqrt(mean_squared_error(y_true, y_pred))
        print('RMSE: %.3f' % rmse)
        pyplot.plot(y_true, label='Actual')
        pyplot.plot(y_pred, label='Predicted')
        pyplot.legend()
        pyplot.show()
        print(df.head())
        print(df.columns)


test()
