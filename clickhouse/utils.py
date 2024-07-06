import base64
import pickle
from client import clickhouse_client


"""
Clickhouse does not support the pickled objects yet, and it is a problem.
There is a solution to use `base64` encoding, store the model as a string and then decode it and use as a pickle object 

Though it is a subject of discussion in the future. I personally prefer to store the model in S3 bucket, but this will require an 
additional time for development which we do not have to test the model completely in production.  
"""

def serialize_model(file_path):
    with open(file_path, 'rb') as f:
        pickled_model = f.read()
    base64_model = base64.b64encode(pickled_model).decode('utf-8')
    return base64_model


def deserialize_model(base64_model):
    pickled_model = base64.b64decode(base64_model.encode('utf-8'))
    model = pickle.loads(pickled_model)
    return model



# TESTING THIS FOR NOW, SHOULD BE REMOVED LATER
def insert_model():
    serialized_model = serialize_model('trained_model.pkl')
    training_tmp_data = [(['dv', 'br', 'os', 'lc', 'me', 'unique'], ['year', 'month', 'day'], ['traffic_next_1_hr'], serialized_model)]
    clickhouse_client.insert_data('training_tmp', training_tmp_data)
    print("Model inserted successfully.")


def fetch_model():
    result = clickhouse_client.execute_query("SELECT model FROM training_tmp LIMIT 1")
    if result:
        serialized_model = result[0]
        model = deserialize_model(serialized_model)
        return model
    else:
        print("No model found")
        return None
    

import json
def serialize_data(data):
    """Serialize the provided JSON data for ClickHouse insertion"""
    serialized_data = []
    
    pid = data['pid']
    next_1_hour = json.dumps(data.get('next_1_hour', {}))
    next_4_hour = json.dumps(data.get('next_4_hour', {}))
    next_8_hour = json.dumps(data.get('next_8_hour', {}))
    next_24_hour = json.dumps(data.get('next_24_hour', {}))
    next_72_hour = json.dumps(data.get('next_72_hour', {}))
    next_168_hour = json.dumps(data.get('next_168_hour', {}))
    
    serialized_data.append((pid, next_1_hour, next_4_hour, next_8_hour, next_24_hour, next_72_hour, next_168_hour))
    return serialized_data


def insert_predictions(predictions):
    """Insert sample JSON data into the predictions table"""
    serialized_data = serialize_data(json.loads(predictions))
    clickhouse_client.insert_data('predictions', serialized_data)


# base64_model = fetch_model() # works
# model = deserialize_model(base64_model) # works

"""
Query executes too long, though it may be fine for now, as model weights 300MB approximately

select * from training_tmp LIMIT 1;
1 rows in set. Elapsed: 2.633 sec. 

"""
