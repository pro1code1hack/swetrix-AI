import os
from dotenv import load_dotenv
from clickhouse_driver import Client

class ClickHouseClient:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('CLICKHOUSE_HOST')
        self.port = os.getenv('CLICKHOUSE_PORT')
        self.user = os.getenv('CLICKHOUSE_USER')
        self.password = os.getenv('CLICKHOUSE_PASSWORD')
        self.database = os.getenv('CLICKHOUSE_DATABASE')
        
        self.client = Client(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
    
    def execute_query(self, query: str):
        return self.client.execute(query)
    
    def insert_data(self, table: str, data: list):
        self.client.execute(f"INSERT INTO {table} VALUES", data)


clickhouse_client = ClickHouseClient()
result = clickhouse_client.execute_query("SELECT * FROM training_data")
print(result)
