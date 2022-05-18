import csv, sqlite3
import create_bd
from progress.bar import IncrementalBar
import time
from datetime import timedelta
import logging


DB_PATH = "results/san_francisco.sqlite3"
DATE_PATH = "data/police-department-calls-for-service.csv"

logging.basicConfig(
    level=logging.INFO,
    filename = "results/log.log",
    format = "%(message)s"
    )

def add_item(cursor, sql, *args):
    cursor.execute(sql, *args)

def len_csv(path):
    with open(path) as file:
        reader = csv.reader(file)
        count_row = sum(1 for row in reader)
        return count_row

start_time = time.monotonic()
count_records = len_csv(DATE_PATH)
bar = IncrementalBar("Loading BD", max = count_records)
with open(DATE_PATH) as file:
    try:
        connection = sqlite3.connect(DB_PATH)
        logging.info("Successfull connection")
        cursor = connection.cursor()
        count_row = 0

        reader = csv.reader(file)
        for row in reader:
            if count_row:
                crime_id = row[0]
                original_crime_type_name = row[1]
                report_date = row[2][:10] + " " + row[2][11:]
                call_date = row[3][:10] + " " + row[3][11:]
                offense_date = row[4][:10] + " " + row[4][11:]
                call_time = row[5]
                call_date_time = row[6][:10] + " " + row[6][11:]
                desposition = row[7]
                address = row[8]
                city = row[9]
                state = row[10]
                agency_id = row[11]
                address_type = row[12]
                common_location = row[13]

                sql_crime = "insert into Crime values (?, ?, ?)"
                add_item(cursor, sql_crime, (count_row, crime_id, original_crime_type_name))

                sql_crime = "insert into Date values (?, ?, ?, ?, ?, ?, ?)"
                add_item(cursor, sql_crime, (count_row, report_date, call_date, offense_date,
                                             call_time, call_date_time, count_row))

                sql_crime = "insert into Location values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                add_item(cursor, sql_crime, (count_row, desposition, address, city,
                                             state, agency_id, address_type, common_location, count_row))

            count_row +=1
            bar.next()

        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("SQLite error", error)
        logging.info(f"SQLite error: {error}")

    finally:
        if (connection):
            connection.close()
            logging.info("Connection close")
        if (bar):
            bar.finish()
        end_time = time.monotonic()
        logging.info(f"Number of records created: {count_row-1}")
        logging.info(f"Program execution time: {timedelta(seconds=end_time - start_time)}")
        

