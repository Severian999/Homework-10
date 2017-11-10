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
    return cur.fetchall()


def convert_capture_dates_times(captured_dates_times):
    converted_date = []
    for capTime in captured_dates_times:
        capDate, __ = capTime[0].split('T')
        # get dates in yyyy-mm (2017-10) format for easier string sorting
        # because mmm-yyyy (OCT-2017) formats will not sort properly (as strings)
        converted_date.append(arrow.get(capDate).format('YYYY-MM'))
    return converted_date


def get_unique_dates(date_list):
    # get sorted list of unique dates based on yyyy-mm format using set
    # operations
    unique_dates = sorted(list((set(date_list) | set(date_list))))
    # list comprehension to return sorted list in mmm-yyyy format...
    # eg. 2017-10 to OCT-2017
    # return [arrow.get(x).format('MMM-YYYY') for x in unique_dates]
    return unique_dates


def make_plot_list(date_list, captured_dates):
    return [captured_dates.count(x) for x in date_list]


def expand_dates(short_dates):
    return [arrow.get(x).format('MMM-YYYY') for x in short_dates]

table_name = 'Adobe_images'
col_name = 'captureTime'
sql_file = 'LightroomCatalog-2.lrcat'

conn, cur = cat_connect(sql_file)
captured_dates_times = get_data(cur, table_name,col_name)
captured_dates = convert_capture_dates_times(captured_dates_times)
print(captured_dates)
date_list = get_unique_dates(captured_dates)
counts = make_plot_list(date_list, captured_dates)
print(counts)
conn.close()

plt.plot(date_list,counts, label="Frequency of shots")
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
