from typing import Any
from sqlalchemy import create_engine  # use SQLAlchemy connecting to the database
import pandas as pd
import numpy as np

# Stored in the `.env` file.  <- Replace it with real params.
host = "localhost"
port = 5432
user = "postgres"
password = 123456
db = "DatenBank"

# connect to the database
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
# query the raw data.
query_apps = "SELECT * FROM apple_apps;"
query_reviews = "SELECT * FROM app_reviews;"
apps = pd.read_sql(query_apps, engine)
reviews = pd.read_sql(query_reviews, engine)
# Check the data has been loaded correctly.
# apps.head()

# TODO: mark empty string values ("") as missing values (NULL).
for _df in (apps, reviews):
    obj_cols = _df.select_dtypes(include=["object", "string"]).columns
    if len(obj_cols):
        _df[obj_cols] = _df[obj_cols].replace('', np.nan)

# TODO: imputation the date if need.
apps['privacy_not_collected_bool'] = (
    apps['privacy_not_collected']
        .astype(str)
        .str.strip() # 去两端空白
        .str.lower() # 统一转为小写
        .eq('true')  # 判断条件
)
# print(apps['privacy_not_collected'].value_counts(dropna=False))   # check result (也包括NULL值)

apps['price_eur'] = (
    apps['price']
        .astype(str)
        .str.replace('\xa0', '', regex=False)   # delete ' '
        .str.replace('€', '', regex=False)      # delete €
        .str.replace(',', '.', regex=False)     # , => .
        .str.strip()                            # 去两端空白
)
# print(apps['price_eur'].head(10)) # check result

# TODO: 
cols_0 = ['size']
cols_int_0 = ['review_one', 'review_two', 'review_three', 'review_four', 'review_five']
apps = apps[
    apps['review_average'].between(0, 5, inclusive='both') &  # 0 <= Each <= 5
    (apps[cols_0] > 0).all(axis=1) &                          # Each > 0
    (apps[cols_int_0] >= 0).all(axis=1) &                     # Each >= 0
    (apps[cols_int_0] % 1 == 0).all(axis=1)                   # only integer values;
]
reviews = reviews[
    reviews['rating'].between(0, 5, inclusive='both')         # 0<= Each <=5
]
apps["review_count"] = reviews.groupby("app_id")["app_id"].transform("count")  # apps 表中的 review_count 和实际 reviews 表中的数据统计不符，进行统一。 
# 备用，另一种更安全的替换 - map
# review_counts = reviews_medizin.groupby("app_id").size()
# apps["review_count"] = (
#     apps["app_id"]
#     .map(review_counts)
#     .fillna(0)
#     .astype(int)
# )

# 拆分实验组和对照组
categories_medizin = {
    "Medizin",
    "Gesundheit und Fitness",
    "Lifestyle"
}
# 拆分 apps 表
apps_medizin = apps[apps["category"].isin(categories_medizin)].copy()
apps_medizin_not = apps[~apps["category"].isin(categories_medizin)].copy()
# 获取 A / B 组的 app_id (用 set 查找更快、语义更清楚)
app_ids_medizin = set[Any](apps_medizin["app_id"])
app_ids_medizin_not = set[Any](apps_medizin_not["app_id"])
# 按 app_id 拆分 reviews 表（关键）
reviews_medizin = reviews[reviews["app_id"].isin(app_ids_medizin)].copy()
reviews_medizin_not = reviews[reviews["app_id"].isin(app_ids_medizin_not)].copy()


# check the shape of data A & B
print(
    "apps             – Anzahl Zeilen:", apps.shape[0], "\n" 
    "apps_medizin     – Anzahl Zeilen:", apps_medizin.shape[0], round(apps_medizin.shape[0]*100 / apps.shape[0], 2), "% \n" 
    "apps_medizin_not – Anzahl Zeilen:", apps_medizin_not.shape[0], round(apps_medizin_not.shape[0]*100 / apps.shape[0], 2), "%"
)
print(
    "reviews             – Anzahl Zeilen:", reviews.shape[0], "\n" 
    "reviews_medizin     – Anzahl Zeilen:", reviews_medizin.shape[0], round(reviews_medizin.shape[0]*100 / reviews.shape[0], 2), "% \n"  
    "reviews_medizin_not – Anzahl Zeilen:", reviews_medizin_not.shape[0], round(reviews_medizin_not.shape[0]*100 / reviews.shape[0], 2), "%"
)
print("apps – Anzahl Spalten:", apps.shape[1])
print("reviews – Anzahl Spalten:", reviews.shape[1])

# TODO: 导出 csv 数据
# apps_medizin.to_csv("db/apps_medizin.csv", index=False)
# reviews_medizin.to_csv("db/reviews_medizin.csv", index=False)
# apps_medizin_not.to_csv("db/apps_medizin_not.csv", index=False)
# reviews_medizin_not.to_csv("db/reviews_medizin_not.csv", index=False)
