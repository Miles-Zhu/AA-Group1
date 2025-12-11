from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine  # use SQLAlchemy connecting to the database

# load the environment variables
load_dotenv() 
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
db = os.getenv("PG_DATABASE")

# connect to the database
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

# query the data: app_reviews | apple_apps 
 
# query the columns of the table
# query = """
# SELECT column_name
# FROM information_schema.columns
# WHERE table_schema = 'public'
#   AND table_name   = 'apple_apps';
# """

# query the number of rows in the table
# query = """
# SELECT COUNT(*) FROM app_reviews;
# """

query = """

"""

# read the data into a pandas dataframe
df = pd.read_sql(query, engine)
print(df)
