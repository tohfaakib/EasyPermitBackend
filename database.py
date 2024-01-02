from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure
from settings import AppSettings

settings = AppSettings()

def db_connection():
    try:
        uri = f"mongodb+srv://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_CLUSTER_URL}/?retryWrites=true&w=majority"
        client = MongoClient(uri)

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            raise e
        return client
    except ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")


client = db_connection()

db = client[settings.MONGODB_DATABASE_NAME]
table_name = db[settings.MONGODB_TABLE_NAME]