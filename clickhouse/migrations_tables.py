from client import ClickHouseClient


def create_tables():
    client = ClickHouseClient()

    training_tmp_query = """
    CREATE TABLE IF NOT EXISTS training_tmp (
        cat_features Array(String),
        cols Array(String),
        next_hrs Array(String),
        model String
    ) ENGINE = MergeTree()
    ORDER BY tuple()
    """

    predictions_query = """
    CREATE TABLE IF NOT EXISTS predictions (
        pid String,
        next_1_hour String,
        next_2_hour String,
        next_3_hour String,
        next_4_hour String,
        next_5_hour String,
        next_6_hour String,
        next_7_hour String,
        next_8_hour String,
        next_9_hour String,
        next_10_hour String,
        next_11_hour String,
        next_12_hour String,
        next_13_hour String,
        next_14_hour String,
        next_15_hour String,
        next_16_hour String,
        next_17_hour String,
        next_18_hour String,
        next_19_hour String,
        next_20_hour String,
        next_21_hour String,
        next_22_hour String,
        next_23_hour String,
        next_24_hour String
    ) ENGINE = MergeTree()
    ORDER BY pid
    """

    client.execute_query(training_tmp_query)
    client.execute_query(predictions_query)


client = ClickHouseClient()

if __name__ == "__main__":
    create_tables()
