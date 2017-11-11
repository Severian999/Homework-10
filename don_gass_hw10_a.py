#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Don Gass
"""

import sqlite3
import arrow
import matplotlib.pyplot as plt

def cat_connect(sql_file):
    """
    :param sql_file:  database file to open
    :return:  connection object, cursor object
    """
    conn = sqlite3.connect(sql_file)
    cur = conn.cursor()
    return conn, cur


def get_data(cursor, table_name, col_name):
    """
    :param cursor:  cursor from cat_connect()
    :param table_name:  name of table to select data from
    :param col_name:  column to return
    :return:  data from col_name as list of tuples
    """
    cursor.execute('SELECT {cn} FROM {tn} ORDER BY {cn} ASC' \
                   .format(cn=col_name, tn=table_name))
    return CUR.fetchall()


def convert_capture_dates_times(captured_dates_times):
    """
    :param captured_dates_times: the raw capture time data
    :return: formatted yyyy-mm list of dates
    """
    converted_date = []
    for cap_time in captured_dates_times:
        cap_date, __ = cap_time[0].split('T')
        # get dates in yyyy-mm (2017-10) format for easier string sorting
        # because mmm-yyyy (OCT-2017) formats will not sort properly (as strings)
        converted_date.append(arrow.get(cap_date).format('YYYY-MM'))
    return converted_date


def get_unique_dates(date_list):
    """
    :param date_list:
    :return: a sorted list of unique dates from union'ing itself
    """
    return sorted(list((set(date_list) | set(date_list))))


def make_plot_list(date_list, captured_dates):
    """
    :param date_list: list of unique dates
    :param captured_dates: the dates to count based on date_list
    """
    return [captured_dates.count(x) for x in date_list]


TABLE_NAME = 'Adobe_images'
COL_NAME = 'captureTime'
SQL_FILE = 'LightroomCatalog-2.lrcat'

CONN, CUR = cat_connect(SQL_FILE)
CAPTURED_DATES_TIMES = get_data(CUR, TABLE_NAME, COL_NAME)
CAPTURED_DATES = convert_capture_dates_times(CAPTURED_DATES_TIMES)
DATE_LIST = get_unique_dates(CAPTURED_DATES)
COUNTS = make_plot_list(DATE_LIST, CAPTURED_DATES)
CONN.close()

plt.plot(DATE_LIST, COUNTS, label="Frequency of shots")
plt.xlabel("Capture year-month")
plt.ylabel("Number of shots by month")
plt.xticks(rotation=45)
plt.annotate('Intro Photo Class & New Camera', xy=('2015-08', 154),
             xytext=('2013-12', 400),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.title("My Photography Frequency")
plt.tight_layout()
plt.legend(shadow=True, loc="upper left")

plt.show()
