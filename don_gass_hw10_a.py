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


def get_datetimes(cursor, table_name, col_name):
    """
    :param cursor:  cursor from cat_connect()
    :param table_name:  name of table to select data from
    :param col_name:  column to return
    :return:  data from col_name as list of tuples
    """
    cursor.execute('SELECT {cn} FROM {tn} ORDER BY {cn} ASC' \
                   .format(cn=col_name, tn=table_name))
    return cursor.fetchall()


def get_focal_length(cursor, table_name, col_name):
    """
    :param cursor:  cursor from cat_connect()
    :param table_name:  name of table to select data from
    :param col_name:  column to return
    :return:  data from col_name as list of tuples
    """
    cursor.execute('SELECT {cn} FROM {tn} ORDER BY {cn} ASC' \
                   .format(cn=col_name, tn=table_name))
    return cursor.fetchall()


def convert_captured_data(captured_dates_times, captured_focal_lengths):
    """
    :param captured_dates_times: the raw capture time data
    :return: formatted yyyy-mm list of dates
    """
    converted_date = []
    converted_length = []
    for cap_time in captured_dates_times:
        cap_date, __ = cap_time[0].split('T')
        # get dates in yyyy-mm (2017-10) format for easier string sorting
        # because mmm-yyyy (OCT-2017) formats will not sort properly (as strings)
        converted_date.append(arrow.get(cap_date).format('YYYY-MM'))
    for length in captured_focal_lengths:
        if length[0] is None:
            continue
        else:
            converted_length.append(length[0])
    return converted_date, converted_length


def get_unique_values(date_list, length_list):
    """
    :param date_list:
    :param length_list:
    :return: a two sorted lists of unique values from union'ing itself
    """
    ret_dates = sorted(list(set(date_list) | set(date_list)))
    ret_lengths = sorted(list(set(length_list) | set(length_list)))
    return ret_dates, ret_lengths


def make_plot_list(value_list, captured_values):
    """
    :param value_list: list of unique values
    :param captured_values: the values to count based on value_list
    """
    return [captured_values.count(x) for x in value_list]


def plot_settings():
    """Basic plot settings: size and style"""
    plt.figure(1, figsize=(18, 9))
    plt.style.use('ggplot')


def plot_shot_frequency(dates_to_plot, counts_of_dates):
    """
    Plot all of the things...(shot frequency)
    :param dates_to_plot: unique date list
    :param count_of_dates: shot counts by month
    """
    plt.subplot(2, 1, 1)
    plt.plot(dates_to_plot, counts_of_dates, 'g-o', label="Frequency of shots")
    plt.xlabel("Capture year-month")
    plt.ylabel("Number of shots by month")
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.annotate('Intro Photo Class & New DSLR Camera', xy=('2015-08', 154),
                 xytext=('2013-12', 400),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('Semester markers', xy=('2015-08', 800),
                 xytext=('2013-12', 900),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.title("My Photography Frequency")
    plt.tight_layout()
    plt.legend(shadow=True, loc="upper left")
    # Create the vertical semester bars
    plt.axvspan('2015-08', '2015-12', facecolor='blue', alpha=0.35)
    plt.axvspan('2016-01', '2016-05', facecolor='red', alpha=0.35)
    plt.axvspan('2016-09', '2016-12', facecolor='magenta', alpha=0.35)
    plt.axvspan('2017-01', '2017-05', facecolor='yellow', alpha=0.35)


def plot_focal_lengths(list_of_lengths, lengths_to_plot):
    """
    Plot all of the things...(focal lengths)
    :param lengths_to_plot: unique focal length list
    :param count_of_lengths: focal length counts
    """
    plt.subplot(2, 1, 2)
    plt.style.use('ggplot')
    plt.plot(list_of_lengths, lengths_to_plot, 'b-', label="Focal length usage")
    plt.xlabel('Focal Lengths')
    plt.ylabel('Count of focal lengths')
    plt.annotate('35mm f1.8 fixed focal length lens', xy=(35, 900),
                 xytext=(10, 1000),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('50mm f1.8 fixed focal length lens', xy=(50, 2700),
                 xytext=(20, 2400),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.text(75, 1500, 'Green area, other than 35mm and 50mm lens points,\n' \
                       'represents an 18-140mm f3.5-f5.6 zoom lens.',
             color='green')
    plt.text(4, 1500, 'Blue area represents\nfocal lengths outside\n' \
                      'my three lenses: most\nlikely cell phone\nshots.',
             color='blue')
    plt.title('My Favorite Focal Lengths')
    plt.tight_layout()
    plt.legend(shadow=True, loc="upper right")
    plt.axvspan(3.97, 17.9, facecolor='blue', alpha=0.35)
    plt.axvspan(18, 140, facecolor='green', alpha=0.35)

# CONSTANTS
TABLE_NAME = 'Adobe_images'
TABLE_NAME2 = 'AgHarvestedExifMetadata'
COL_NAME = 'captureTime'
COL_NAME2 = 'focalLength'
SQL_FILE = 'LightroomCatalog-2.lrcat'

# Main program
CONN, CUR = cat_connect(SQL_FILE)
CAPTURED_DATES_TIMES = get_datetimes(CUR, TABLE_NAME, COL_NAME)
CAPTURED_FOCAL_LENGTHS = get_focal_length(CUR, TABLE_NAME2, COL_NAME2)
CONN.close()
CAPTURED_DATES, CAPTURED_LENGTHS = convert_captured_data(CAPTURED_DATES_TIMES,
                                                         CAPTURED_FOCAL_LENGTHS)
DATE_LIST, LENGTH_LIST = get_unique_values(CAPTURED_DATES, CAPTURED_LENGTHS)
COUNTS = make_plot_list(DATE_LIST, CAPTURED_DATES)
COUNTS2 = make_plot_list(LENGTH_LIST, CAPTURED_LENGTHS)
plot_settings()
plot_shot_frequency(DATE_LIST, COUNTS)
plot_focal_lengths(LENGTH_LIST, COUNTS2)
plt.show()
