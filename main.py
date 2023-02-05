from enums import Fields, TimeMetrics
from process_data import Reader, Data
from model_training import Model
from time_tracking import calculate_time
from serialize_data import Serializer


@calculate_time
def main():
    data_json = Reader('data.json').read_json()
    data = Data(data_json)

    print(data.original_data.head())
    print("-----------------")

    print(data.visits_with_ds.head())
    print(data.uniques_with_ds.head())
    print(data.sdur_with_ds.head())

    model = Model(data.visits_with_ds)
    model.train()

    model = Model(data.uniques_with_ds)
    model.train()

    model = Model(data.sdur_with_ds)
    model.train()



if __name__ == '__main__':
    main()
