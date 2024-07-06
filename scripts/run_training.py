
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clickhouse.client import clickhouse_client
from clickhouse.utils import serialize_model
from data.load_data import pre_process_data 
from models.train_model import train_model, save_model 
from datetime import datetime

def train():
    """Celery task which is called for a model training
        - Gets data from ``load_data`` module
        - Saves model to ``.pkl`` format
        - Serialises model to ``base64`` encoding
        - Inserts data to the DB
    """
    timestamp = datetime.now()
    file_path = f'pickled_model_{timestamp}' 

    df, cat_features, cols, next_hrs = pre_process_data()
    model = train_model(df,cols, next_hrs)
    save_model(file_path, model)

    serialized_model = serialize_model(file_path)
    training_tmp_data = [(cat_features, cols.to_list(), next_hrs, serialized_model)]

    clickhouse_client.insert_data('training_tmp', training_tmp_data)
    print("Training has been completed and data is inserted to the database!")
