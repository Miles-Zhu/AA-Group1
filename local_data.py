import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
# load libraries
import numpy as np
import seaborn as sns
import sweetviz as sv

apps = pd.read_csv('db/apps_medizin_not.csv')
reviews = pd.read_csv('db/reviews_medizin_not.csv')

# Merge on app_id
df = reviews.merge(apps, on="app_id", how="left")

# df = pd.read_sql(query, engine)
msno.matrix(df)
plt.show()


# Set Seaborn style
# sns.set_style("whitegrid")

# Create histogram
# plt.figure(figsize=(8, 6))
# sns.histplot(df['review_average'], bins=25, kde=True, color='royalblue')
# plt.xlabel("review_average")
# plt.ylabel("Frequency")
# plt.title("review_average of health APP")
# plt.show()


# Create scatterplot
# plt.figure(figsize=(8, 6))
# sns.scatterplot(x=df['review_average'], y=df['review_count'], color='royalblue', alpha=0.6)
# plt.xlabel("review_average")
# plt.ylabel("review_count")
# plt.title(" review_average vs review_count")
# plt.show()

