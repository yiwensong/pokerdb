"""dbconn.py
This file is a python api to connect to the database.
"""
import psycopg2
import pandas as pd

DB_CONFIG = {
  'user': 'postgres',
  'database': 'pltracker',
  'password': 'ZU&%,Wk9~<xt`,7M',
  'host': '35.199.157.96',
  'port': 5432,
};

def get_connection():
    """Returns a connection to the research database."""
    con = psycopg2.connect(**DB_CONFIG)
    return con

def query(statement, con=None, params=None):
    """Returns a dataframe that contains the results of the statement."""
    if con is None:
        con = get_connection()
    table = pd.io.sql.read_sql(statement, con, params=params)
    return table

def run_sql_file(sql_fname, con=None):
    """Runs a sql config file."""
    if con is None:
        con = get_connection()
    with open(sql_fname, 'r') as f:
        sql = f.read()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def insert(tablename, value_dict, con=None):
    """Does an insert into tablename on cols with value_dict
    as the map for column to values.
    """
    if con is None:
        con = get_connection()
    cur = con.cursor()
    sql = 'INSERT INTO ' + tablename + '('
    for k in value_dict:
        sql += k + ', '
    sql = sql[:-2] + ') VALUES ('
    for k in value_dict:
        sql += '%(' + k + ')s, '
    sql = sql[:-2] + ')'
    print(sql)
    try:
        cur.execute(sql, value_dict)
    except psycopg2.IntegrityError as e:
        print('Insertion failed. Error:', e)
    con.commit()

