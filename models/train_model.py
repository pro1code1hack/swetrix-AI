from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import pickle


def train_model(df, cols, next_hrs):
    """
    Train the model, fit data into the model and predict_values 
    """
    model = DecisionTreeRegressor()
    model.fit(df[cols],df[next_hrs])
    y_pred = model.predict(df[cols])
    
    accuracy = r2_score(df[next_hrs], y_pred)
    print(f"R^2 score: {accuracy:.2f}")
    accuracy = mean_absolute_error(df[next_hrs], y_pred)
    print(f"mean_absolute_error: {accuracy:.2f}")
    return model


def save_model(file_path, model):
    """
    Save the model into .pkl format
    """
    pickle_out = open(file_path,"wb") # TODO save to the db
    pickle.dump(model, pickle_out)
    pickle_out.close()
