# 帮写一段代码实现 apps表和 reviews表 数据的统一，其中 apps包含：'review_average'=> 平均评分，'review_one', 'review_two', 'review_three', 'review_four', 'review_five' 分别记录获得1星-5星的数量，平均评分由这5个字段各自的 【分值*数量/总评论数】获得。另外 reviews 表包含了所有的评论，其中的 rating 即是本条评论的评分。所以我们需要做的事情是：1、以 app_id为关联，聚合统计1-5星的数量（rating提供）。2、完成上一步骤后，计算覆盖 apps表中的 'review_average'，'review_one', 'review_two', 'review_three', 'review_four', 'review_five' 。3、注意是聚合计算，保证准确性
import pandas as pd
import numpy as np

# ---------- 0) 基础清洗：确保 rating 是数值 & 只保留 1-5 ----------
reviews_clean = reviews.copy()
reviews_clean["rating"] = pd.to_numeric(reviews_clean["rating"], errors="coerce")

reviews_clean = reviews_clean[reviews_clean["rating"].isin([1, 2, 3, 4, 5])].copy()

# ---------- 1) 以 app_id 聚合统计 1-5 星数量 ----------
star_counts = (
    reviews_clean
    .groupby(["app_id", "rating"])
    .size()
    .unstack("rating", fill_value=0)
)

# 确保 1-5 星列都存在（哪怕某些星级在数据里从未出现）
star_counts = star_counts.reindex(columns=[1, 2, 3, 4, 5], fill_value=0)

# 改成 apps 表里的列名
star_counts = star_counts.rename(columns={
    1: "review_one",
    2: "review_two",
    3: "review_three",
    4: "review_four",
    5: "review_five",
}).reset_index()

# ---------- 2) 计算加权平均评分 review_average ----------
count_cols = ["review_one", "review_two", "review_three", "review_four", "review_five"]

star_counts["review_count_calc"] = star_counts[count_cols].sum(axis=1)

weighted_sum = (
    1 * star_counts["review_one"]
    + 2 * star_counts["review_two"]
    + 3 * star_counts["review_three"]
    + 4 * star_counts["review_four"]
    + 5 * star_counts["review_five"]
)

star_counts["review_average_calc"] = np.where(
    star_counts["review_count_calc"] > 0,
    weighted_sum / star_counts["review_count_calc"],
    np.nan
)

# ---------- 3) 覆盖写回 apps（聚合结果以 app_id 对齐，保证准确性） ----------
apps_updated = apps.copy()

apps_updated = apps_updated.merge(
    star_counts[["app_id"] + count_cols + ["review_average_calc"]],
    on="app_id",
    how="left",
    suffixes=("", "_from_reviews")
)

# 覆盖 apps 中的字段（没有 reviews 的 app 用 0 / NaN）
for c in count_cols:
    apps_updated[c] = apps_updated[f"{c}_from_reviews"].fillna(0).astype(int)
    apps_updated.drop(columns=[f"{c}_from_reviews"], inplace=True)

apps_updated["review_average"] = apps_updated["review_average_calc"]
apps_updated.drop(columns=["review_average_calc"], inplace=True)

# 可选：如果你也想同步 apps 的 review_count（总评论数）
# apps_updated["review_count"] = apps_updated[count_cols].sum(axis=1).astype(int)

# 结果：apps_updated 就是统一后的 apps 表
