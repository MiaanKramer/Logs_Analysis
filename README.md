# Logs Analysis Project

## About
I have been hired onto a team working on a newspaper site. I have been tasked to create a **internal reporting tool** that will be used to gather information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, my code will answer questions about the site's user activity.

The program i have written in the project runs from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answer to some questions.

### Questions:

- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

## How to run the program

First thing you need to do is download [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html) to create and manage in order to run this project. Next thing you need to do is download the [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) that Udacity has provided. Now unpack the virtual machine and git bash in the folder of the machine.

Then run ```vagrant up```, Vagrant wil now download the Linux operating system and install it (may take a few minutes). After the install/download of the necessary files have been completed you have to run the ```vagrant ssh``` in your git bash terminal.

You are now inside the virtual machine. ```cd``` into the cagrant directory. Now you must hookup the database and create the views. To do to this you will need to run ```psql -d news -f newsdata.sql```. Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

Now you need to create the views. Run the command ```psql -d news``` to connect with the database. Now you can run sql queries. Run the Views queries below and exit by typing ```\q```. You can now run the python code by typing ```python logs_analysis.py```. The results should now be printed out in the terminal.

## Views

### Article Views
```
CREATE VIEW
    article_views AS
SELECT
    articles.title, articles.author, count(*) AS views
FROM
    articles
JOIN
    log
ON
    log.path = concat('/article/', articles.slug)
GROUP BY
    articles.title, articles.author
ORDER BY
    views DESC;
```

### Requests Per Day
```
CREATE VIEW
    day_logs AS
SELECT
    count(*) AS requests,
    count(1) FILTER (WHERE log.status = '200 OK') AS successful,
    count(1) FILTER (WHERE log.status != '200 OK') AS unsuccessful,
    TO_CHAR(log.time, 'fmMonth DD, YYYY') as date
FROM
    log
GROUP BY
    date;
```
