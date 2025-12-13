from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine  # use SQLAlchemy connecting to the database
import missingno as msno
import matplotlib.pyplot as plt

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
#####################################################
#          STEP-1.creat new Table:                  #
# app_reviews_medizin | apple_apps_medizin          #
#####################################################

#####################################################
#          STEP-2.review Data                       #
#####################################################
## 2.1 check NULL
# query = """
# SELECT * 
# FROM apple_apps_medizin;
# """


query = """
SELECT * 
FROM app_reviews_medizin;
"""

# read the data into a pandas dataframe
df = pd.read_sql(query, engine)
# print(df)

msno.matrix(df)
plt.show()

## 2.2 check 0 & ''  => want to replace?
# check1 = df.isna().sum()
# check2 = (df == 0).sum()
# print(check1)

#####################################################
#          STEP-3.Outliers Data                     #
#   Count Error-value => Delete or Replace?         #
#####################################################
# query = """
# SELECT 
#     COUNT(*) FILTER (WHERE review_average < 0 OR review_average > 5) AS Err_review_average,
#     COUNT(*) FILTER (WHERE review_one < 0) AS Err_review_one,
#     COUNT(*) FILTER (WHERE review_two < 0) AS Err_review_two,
#     COUNT(*) FILTER (WHERE review_three < 0) AS Err_review_three,
#     COUNT(*) FILTER (WHERE review_four < 0) AS Err_review_four,
#     COUNT(*) FILTER (WHERE review_five < 0) AS Err_review_five,
#     COUNT(*) FILTER (WHERE size <= 0) AS Err_size
# FROM apple_apps_medizin;
# """

# query = """
# SELECT 
#     COUNT(*) FILTER (WHERE rating < 0 OR rating > 5) AS Err_rating
# FROM app_reviews_medizin;
# """

# show Error-value count
# df = pd.read_sql(query, engine)
# print(df)

#####################################################
#          STEP-4.Variable Cleaning                 #
#   Count Error-value => Delete or Replace?         #
#####################################################

# query = """
# SELECT
# 	privacy_not_collected,
# 	privacy_not_collected_bool
# FROM apple_apps_medizin;
# """
# df = pd.read_sql(query, engine)
# print(df)

###############################################################
#          STEP-5.Data Wrangling                              #
# removal & transformation & Binning & Reshaping & Sampling   #
###############################################################

###############################################################
#          STEP-6.Export to csv                               #
###############################################################
# app_reviews_medizin = pd.read_sql("SELECT * FROM app_reviews_medizin", engine)
# apple_apps_medizin = pd.read_sql("SELECT * FROM apple_apps_medizin", engine)

# app_reviews_medizin.to_csv("app_reviews_medizin.csv", index=False)
# apple_apps_medizin.to_csv("apple_apps_medizin.csv", index=False)





