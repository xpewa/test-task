import csv, sqlite3
import create_bd
import time
from datetime import timedelta
import logging
import sys
import re 

COUNT_BATCH = 50000


DB_PATH = "results/san_francisco.sqlite3"
DATE_PATH = "data/police-department-calls-for-service.csv"

logging.basicConfig(
    level=logging.INFO,
    filename = "results/log.log",
    format = "%(message)s"
    )

def progress(count):
    sys.stdout.write(f"Loaded {count} rows\r")
    sys.stdout.flush()

def check_datetime(date):
    is_fit = re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", date)
    return date if is_fit else "0000-00-00T00:00:00"

def check_crime_id(crime_id):
    is_fit = re.fullmatch(r"\d{9}", crime_id)
    return crime_id if is_fit else "000000000"

def check_time(time):
    is_fit = re.fullmatch(r"\d{2}:\d{2}", time)
    return time if is_fit else "00:00"

start_time = time.monotonic()
with open(DATE_PATH) as file:
    try:
        connection = sqlite3.connect(DB_PATH)
        logging.info("Successfull connection")
        cursor = connection.cursor()
        count_row = 0

        reader = csv.DictReader(file)
        sql_crime = "insert into Crime values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = []

        for row in reader:
            if count_row % COUNT_BATCH == 0:
                cursor.executemany(sql_crime, data)
                data = []
                progress(count_row)
                

            crime_id = check_crime_id(row["Crime Id"])
            report_date = check_datetime(row["Report Date"]).replace("T", " ")
            call_date = check_datetime(row["Call Date"]).replace("T", " ")
            offense_date = check_datetime(row["Offense Date"]).replace("T", " ")
            call_date_time = check_datetime(row["Call Date Time"]).replace("T", " ")
            call_time = check_time(row["Call Time"])

            data.append([count_row, crime_id, row["Original Crime Type Name"],
                        report_date, call_date, offense_date, call_time,
                        call_date_time, row["Disposition"], row["Address"],
                        row["City"], row["State"], row["Agency Id"],
                        row["Address Type"], row["Common Location"]])
            count_row +=1

        if data:
            cursor.executemany(sql_crime, data)
            progress(count_row)

        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("SQLite error", error)
        logging.error(f"SQLite error: {error}")

    finally:
        if (connection):
            connection.close()
            logging.info("Connection close")
        end_time = time.monotonic()
        logging.info(f"Number of records created: {count_row}")
        logging.info(f"Program execution time: {timedelta(seconds=end_time - start_time)}")
        

