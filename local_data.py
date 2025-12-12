import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

apps = pd.read_csv('datas/apple_apps_medizin.csv')
reviews = pd.read_csv('datas/app_reviews_medizin.csv')

# Merge on app_id
df = reviews.merge(apps, on="app_id", how="left")

# df = pd.read_sql(query, engine)
msno.matrix(df)
plt.show()

