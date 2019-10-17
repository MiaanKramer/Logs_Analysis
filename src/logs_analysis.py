#! /usr/bin/env python3

# Postgresql Library Import
import psycopg2

DBNAME = "news"

# Articles query to return top 3 most viewed articles
article_query = """
SELECT
    *
FROM
    article_views
LIMIT
    3;
"""

# Authors query to return authors sorted
# by most popular determined by sum of article views

author_query = """
SELECT
    authors.name,
    sum(article_views.views) as views
FROM
    article_views
JOIN
    authors
ON
    article_views.author = authors.id
GROUP BY
    authors.name
ORDER BY
    views DESC;
"""

# Errors query which returns days
# when more than 1% of requests resulted in errors

log_query = """
SELECT
    date,
    (cast(unsuccessful as decimal) / requests) * 100 AS percentage
FROM
    day_logs
WHERE
    (cast(unsuccessful as decimal) / requests) * 100 > 1
ORDER BY
    percentage;
"""


# Connects to the database(Re - usable)
def db_connect(sql_query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_query)
    query_results = c.fetchall()
    return query_results


# Retrieves the top three articles
# by using the article_query combined with the db_connect
def most_viewed_articles():
    articles = db_connect(article_query)
    print('\nMost popular three articles of all time:\n')
    for art in articles:
        print(str(art[0]) + ' - ' + str(art[2]) + ' views')


# Returns the authors with their total views across all
#  of their articles and sorts them by total views descending
def most_popular_authors():
    authors = db_connect(author_query)
    print('\nMost popular article authors of all time:\n')
    for auth in authors:
        print(auth[0] + ' - ' + str(auth[1]) + ' views')


# Returns all the days where more than 1 %
#  of requests resulted in an error
def error_percentages():
    errors = db_connect(log_query)
    print('\nDays that more than 1% of requests lead to errors:\n')
    for error in errors:
        print(error[0] + ' - ' + '%.2f' % error[1] + '% errors')


# Calls all of the functions to be printed out for the user to see
most_viewed_articles()
most_popular_authors()
error_percentages()
