
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.load_data import df, cols, next_hrs
from models.train_model import train_model, save_model 
from datetime import datetime

def train():
    """Celery task which is called for a model training"""
    model = train_model(df,cols, next_hrs)
    save_model(f'pickled_model_{datetime.now()}', model)
