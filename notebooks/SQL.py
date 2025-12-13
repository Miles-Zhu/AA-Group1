# creat new table
# TRUNCATE TABLE app_reviews_medizin;
# TRUNCATE TABLE apple_apps_medizin;
query = """
CREATE TABLE apple_apps_medizin (LIKE apple_apps INCLUDING ALL);
INSERT INTO apple_apps_medizin
SELECT
	*
FROM apple_apps
WHERE category IN (
    'Medizin',
    'Gesundheit und Fitness',
    'Lifestyle'
);
"""

query = """
CREATE TABLE app_reviews_medizin (LIKE app_reviews INCLUDING ALL);
INSERT INTO app_reviews_medizin
SELECT r.*
FROM app_reviews r
JOIN apple_apps a
    ON r.app_id = a.app_id
WHERE category IN (
    'Medizin',
    'Gesundheit und Fitness',
    'Lifestyle'
);
"""

# query the columns of the table
query = """
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name   = 'apple_apps';
"""

# query the number of rows in the table
query = """
SELECT COUNT(*) FROM app_reviews;
"""

# 检查空值
query = """
SELECT 
    COUNT(*) FILTER (WHERE review_id IS NULL) AS missing_review_id, 
    COUNT(*) FILTER (WHERE app_id IS NULL) AS missing_app_id, 
    COUNT(*) FILTER (WHERE date IS NULL) AS missing_date, 
    COUNT(*) FILTER (WHERE developerresponse IS NULL) AS missing_developerresponse, 
    COUNT(*) FILTER (WHERE review IS NULL) AS missing_review, 
    COUNT(*) FILTER (WHERE rating IS NULL) AS missing_rating, 
    COUNT(*) FILTER (WHERE isedited IS NULL) AS missing_isedited, 
    COUNT(*) FILTER (WHERE username IS NULL) AS missing_username, 
    COUNT(*) FILTER (WHERE title IS NULL) AS missing_title 
FROM app_reviews;
"""

query = """
SELECT 
    COUNT(*) FILTER (WHERE app_id IS NULL) AS missing_app_id, 
    COUNT(*) FILTER (WHERE link IS NULL) AS missing_link, 
    COUNT(*) FILTER (WHERE app_name IS NULL) AS missing_app_name, 
    COUNT(*) FILTER (WHERE developer_name IS NULL) AS missing_developer_name, 
    COUNT(*) FILTER (WHERE category IS NULL) AS missing_category, 
    COUNT(*) FILTER (WHERE price IS NULL) AS missing_price, 
    COUNT(*) FILTER (WHERE description IS NULL) AS missing_description, 
    COUNT(*) FILTER (WHERE similar_apps IS NULL) AS missing_similar_apps, 
    COUNT(*) FILTER (WHERE review_count IS NULL) AS missing_review_count, 
    COUNT(*) FILTER (WHERE review_average IS NULL) AS missing_review_average, 
    COUNT(*) FILTER (WHERE review_one IS NULL) AS missing_review_one, 
    COUNT(*) FILTER (WHERE review_two IS NULL) AS missing_review_two, 
    COUNT(*) FILTER (WHERE review_three IS NULL) AS missing_review_three, 
    COUNT(*) FILTER (WHERE review_four IS NULL) AS missing_review_four, 
    COUNT(*) FILTER (WHERE review_five IS NULL) AS missing_review_five, 
    COUNT(*) FILTER (WHERE ipad_version IS NULL) AS missing_ipad_version, 
    COUNT(*) FILTER (WHERE ipod_version IS NULL) AS missing_ipod_version, 
    COUNT(*) FILTER (WHERE mac_version IS NULL) AS missing_mac_version, 
    COUNT(*) FILTER (WHERE size IS NULL) AS missing_size, 
    COUNT(*) FILTER (WHERE languages IS NULL) AS missing_languages, 
    COUNT(*) FILTER (WHERE age IS NULL) AS missing_age, 
    COUNT(*) FILTER (WHERE privacy_linked IS NULL) AS missing_privacy_linked, 
    COUNT(*) FILTER (WHERE privacy_unlinked IS NULL) AS missing_privacy_unlinked, 
    COUNT(*) FILTER (WHERE privacy_tracked IS NULL) AS missing_privacy_tracked, 
    COUNT(*) FILTER (WHERE privacy_not_collected IS NULL) AS missing_privacy_not_collected, 
    COUNT(*) FILTER (WHERE version_history IS NULL) AS missing_version_history, 
    COUNT(*) FILTER (WHERE in_app_purchases IS NULL) AS missing_in_app_purchases, 
    COUNT(*) FILTER (WHERE privacy_policy_link IS NULL) AS missing_privacy_policy_link, 
    COUNT(*) FILTER (WHERE rank_from_pickle IS NULL) AS missing_rank_from_pickle 
FROM apple_apps;
"""

query = """
SELECT 
	rank_from_pickle,
	review_average,
	review_one,
	review_two,
	review_three,
	review_four,
	review_five
FROM apple_apps_medizin;
"""

query = """
SELECT 
	review_count,
	review_average,
	review_one,
	price,
	rank_from_pickle,
	size,
	age,
	languages,
  privacy_not_collected,
	privacy_tracked,
	privacy_linked,
	privacy_policy_link,
	privacy_unlinked,
	privacy_tracked
FROM apple_apps_medizin;
"""

## Variable Cleaning
query = """
ALTER TABLE apple_apps_medizin
ADD COLUMN privacy_not_collected_bool BOOLEAN;

UPDATE apple_apps_medizin
SET privacy_not_collected_bool = 
    CASE 
        WHEN privacy_not_collected ILIKE '%True%' THEN TRUE
        ELSE FALSE
    END;

SELECT
	privacy_not_collected,
	privacy_not_collected_bool
FROM apple_apps_medizin;
"""

## 检测数据

# 找出表1的空值
SELECT
    developerresponse,
    review
FROM app_reviews_medizin
WHERE review IS NULL
   OR trim(review) = ''
   OR lower(review) IN ('nan', 'null', 'none');

# 找出表2的空字符串和NULL值
SELECT
    COUNT(*) FILTER (WHERE iphone_version IS NULL OR iphone_version = '') AS null_or_empty_iphone_version,
    COUNT(*) FILTER (WHERE ipad_version IS NULL OR ipad_version = '') AS null_or_empty_ipad_version,
    COUNT(*) FILTER (WHERE ipod_version IS NULL OR ipod_version = '') AS null_or_empty_ipod_version,
    COUNT(*) FILTER (WHERE mac_version IS NULL OR mac_version = '') AS null_or_empty_mac_version,
    COUNT(*) FILTER (WHERE privacy_linked IS NULL OR privacy_linked = '') AS null_or_empty_privacy_linked,
    COUNT(*) FILTER (WHERE privacy_unlinked IS NULL OR privacy_unlinked = '') AS null_or_empty_privacy_unlinked,
    COUNT(*) FILTER (WHERE privacy_tracked IS NULL OR privacy_tracked = '') AS null_or_empty_privacy_tracked,
    COUNT(*) FILTER (WHERE privacy_not_collected IS NULL OR privacy_not_collected = '') AS null_or_empty_privacy_not_collected,
    COUNT(*) FILTER (WHERE privacy_policy_link IS NULL OR privacy_policy_link = '') AS null_or_empty_privacy_policy_link,
    COUNT(*) FILTER (WHERE rank_from_pickle IS NULL) AS null_or_empty_rank_from_pickle
FROM apple_apps_medizin;

# 修改price数据： 0
SELECT
    app_id,
    rank_from_pickle,
	review_count,
	price
FROM apple_apps_medizin
WHERE price NOT LIKE '%€%';

ALTER TABLE apple_apps_medizin
ADD COLUMN price_eur NUMERIC;
UPDATE apple_apps_medizin
SET price_eur =
    CASE
        WHEN price IS NULL OR trim(price) = '' THEN NULL
        ELSE
            REPLACE(
                regexp_replace(price, '[^0-9,]', '', 'g'),
                ',', '.'
            )::numeric
    END;
# 检查排序
SELECT
    price,
    price_eur
FROM apple_apps_medizin
ORDER BY price_eur DESC;

# 删除不符合规则的数据
DELETE FROM app_reviews_medizin
WHERE review = 'None'
   OR review = 'null';