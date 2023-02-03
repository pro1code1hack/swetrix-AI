from enums import Fields, TimeMetrics
from process_data import Reader, Data
from model_training import Model
from time_tracking import calculate_time


@calculate_time
def main():
    data_json = Reader('data.json').read_json()
    # print(data_json)

    # Iterate over the fields and create the model for each of them.
    # TODO make it dynamically and separate function OR for each field create a separate model.

    data = Data(data_json).create_ds_column()  # Create the ds column (our timeseries column).
    for field in Fields:
        print("Creating predictions for the field: {}".format(field))
        # Skip the x field as it is our DS field.
        if field == Fields.x:
            continue
        data = data.create_y_column(field)
        print(data.processed_data.head())
        model = Model(data.processed_data).fit()
        forecast = model.predict(TimeMetrics.ONE_WEEK)
        model.plot(forecast)


if __name__ == '__main__':
    main()
