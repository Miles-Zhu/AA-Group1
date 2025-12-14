## AA-Group1

![](https://cdn.jsdelivr.net/gh/Miles-Zhu/bucket@main/imgs/20251214002959766.png)
## 1. data

> DatenBank.dump

### 1.1 app_reviews

```bash
# total count
   count
0  520353

# column_name
0          review_id
1             app_id
2               date
3  developerresponse
4             review
5             rating
6           isedited
7           username
8              title
```

### 1.2 apple_apps

```bash
# total count
   count
0  55485

# column_name
0                  app_id
1                    link
2                app_name
3          developer_name
4                category
5                   price
6             description
7            similar_apps
8            review_count
9          review_average
10             review_one
11             review_two
12           review_three
13            review_four
14            review_five
15         iphone_version
16           ipad_version
17           ipod_version
18            mac_version
19                   size
20              languages
21                    age
22         privacy_linked
23       privacy_unlinked
24        privacy_tracked
25  privacy_not_collected
26        version_history
27       in_app_purchases
28    privacy_policy_link
29       rank_from_pickle
```

## 2. category

```bash
# SQL
SELECT category,
COUNT(*) AS count
FROM apple_apps
GROUP BY category
ORDER BY count DESC;

# Result
                       category  count
0        Gesundheit und Fitness  29917  ⭐️
1                       Medizin  12947  ⭐️
2                     Lifestyle   3460  ⭐️
3                         Sport   2739
4                       Bildung   2053
5             Essen und Trinken    774
6              Dienst­programme     665
7                    Wirtschaft    587
8                 Produktivität    469
9                      Shopping    282
10                 Unterhaltung    185
11                       Reisen    182
12             Nachschlagewerke    150
13                     Finanzen    117
14                Soziale Netze    109
15                        Musik    109
16                   Navigation    100
17                       Wetter     79
18                       Puzzle     67
19                  Nachrichten     63
20                       Bücher     51
21               Foto und Video     48
22                       Casual     44
23                   Simulation     37
24  Zeitungen und Zeitschriften     37
25                      Familie     31
26                       Action     30
27                       Spiele     29
28                    Abenteuer     22
29                  Rollenspiel     20
30         Quiz- und Denkspiele     16
31         Emojis und Emotionen     13
32        Sport und Aktivitäten     11
33                    Strategie      9
34                  Brettspiele      8
35                   Wortspiele      4
36              Tiere und Natur      3
37                    Rennsport      3
38          Comics und Cartoons      3
39             Entwickler-Tools      3
40            Grafik und Design      3
41             Orte und Objekte      2
42                      Sticker      2
43                        Leute      1
44                       Karten      1
```

## 3. cleaning data

### 3.1 app_reviews （null）

```bash
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
```

![](https://cdn.jsdelivr.net/gh/Miles-Zhu/bucket@main/imgs/20251212014804576.png)

### 3.2 apple_apps （null）

```bash
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
    COUNT(*) FILTER (WHERE iphone_version IS NULL) AS missing_iphone_version, 
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
```

![](https://cdn.jsdelivr.net/gh/Miles-Zhu/bucket@main/imgs/20251212015256715.png)

- rank_from_pickle !== NULL (646)
![](https://cdn.jsdelivr.net/gh/Miles-Zhu/bucket@main/imgs/20251212020527708.png)

## understanding data

> 评分为0，但是却有多条评论记录。

![](https://cdn.jsdelivr.net/gh/Miles-Zhu/bucket@main/imgs/20251214002959766.png)