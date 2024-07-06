from clickhouse.utils import insert_predictions
from models.predict_model import predict_future_data 

def predict():
    """Celery task which is called for a model predictions
        - Predicts the future data
        - Inserts serialised predictions into the DB
    """
    predictions = predict_future_data()
    insert_predictions(predictions)
