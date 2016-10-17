#!/usr/bin/python2.7

import os
import sys, getopt
import psycopg2
import urllib2
import json
import time
from datetime import date, timedelta, datetime

def execute_sql(sql,data=[]):
  global cursor
  try:
    return cursor.execute(sql,data)
  except psycopg2.Error as e:
    print "ERROR CODE: %s" % e.pgcode
    print e.pgerror
    sys.exit(1)

def verbose_print(string):
  if verbose:
    print string

def usage():
  print '''./mind_the_gap.py -h -v -d -s <start_date> -e <end_date>
  -v --verbose    show extended output
  -d --dry_run    only check and return the number of missing hours
  -s --start_date set start date (eg. 01-10-2016)
  -e --end_date   set_end date   (eg. 13-10-2016)
  -h              too late, you are here :D
  '''

def set_date(date):
  try:
    return datetime.strptime(date, '%d-%m-%Y').date()
  except:
    print "Error: Invalid date %s (dd-mm-yy)" % date
    sys.exit(1)

def is_date_range_valid(date1, date2):
  if date1 > date2:
    print "Error: start date (%s) is greater than end date (%s)" % (pretty_day(date1), pretty_day(date2))
    sys.exit(1)

def pretty_day(day):
  return day.strftime('%d-%m-%Y')

def find_missing_days(days):
  date_set = set(days[0] + timedelta(x) for x in range((days[-1] - days[0]).days))
  return sorted(date_set - set(days))

def find_missing_hours(hours):
  original_hours = set([int(hour[0]) for hour in hours])
  return sorted(list(set(range(0,24)) - original_hours))

def update_content(day, hour, range, text):
  execute_sql("INSERT INTO content (date, hour, range, text) VALUES (%s, %s, %s, %s)", (day, hour , range , text))
  execute_sql("INSERT INTO status (date, hour) VALUES (%s, %s)", (day, hour))

def missing_tables(days):
  global row_count
  missing = find_missing_days(days)
  if missing:
    for day in missing:
      if dry_run:
        verbose_print("%s is missing" % (pretty_day(day)))
      else:
        try:
          response = urllib2.urlopen(url24)
          data = json.load(response)
          for hour in range(24):
            update_content(day, hour, data["range"], data["text"])
          verbose_print("%s was updated" % (pretty_day(day)))
          row_count+=24
        except:
          print "Error: request error"

  for day in days:
    execute_sql("SELECT hour from status WHERE date=%s ORDER BY date, hour", [day])
    hours = cursor.fetchall()
    missing_hours = find_missing_hours(hours)
    if missing_hours:
      for hour in missing_hours:
        if dry_run:
          verbose_print("%s:%s:00 is missing" % (pretty_day(day), hour))
        else:
          try:
            response = urllib2.urlopen(url1)
            data = json.load(response)
            update_content(day, hour, data["range"], data["text"])
            verbose_print("%s:%s:00 was updated" % (pretty_day(day), hour))
            row_count+=1
          except:
            print "Error: request error"

def main(argv):
  global dry_run
  global row_count
  global url1
  global url24
  global verbose
  dry_run = False
  end_date=''
  row_count=0
  start_date=''
  url1  ="http://mockbin.org/bin/1f070f39-3781-4213-8fe1-71e072fb9128"
  url24 ="http://mockbin.org/bin/d21a0e91-05aa-491b-a4a0-d795aeadb24d"
  verbose = False

  db_host = os.getenv("DB_HOST", "psql_host")
  db_user = os.getenv("DB_USER", "postgres")
  db_password = os.getenv("DB_PASSWORD", "pass")
  try:
    opts, args = getopt.getopt(argv,"hvds:e:",["verbose","dry_run","start_date=","end_date="])
  except getopt.GetoptError:
    usage()
    sys.exit(1)
  for opt, arg in opts:
    if opt in ('-h'):
      usage()
      sys.exit(1)
    elif opt in ('-v', "--verbose"):
      verbose = True
    elif opt in ('-d', "--dry_run"):
      dry_run = True
    elif opt in ('-s', "--start_date"):
      start_date = set_date(arg)
    elif opt in ('-e', "--end_date"):
      end_date = set_date(arg)


  verbose_print("************************")
  verbose_print("MIND THE GAP")
  verbose_print("************************")
  if start_date and end_date:
    is_date_range_valid(start_date,end_date)

  c=0
  p=False
  while p == False:
    try:
      params="dbname='data' user=%s host=%s password=%s" % (db_user, db_host, db_password)
      conn = psycopg2.connect(params)
      p=True
    except:
      print "Error: Establishing database connection (%s/5)" % c
      if c == 5:
        print "Aborting..."
        sys.exit(1)
      c=c+1
      time.sleep(5)

  global cursor
  cursor = conn.cursor()
  sql = "SELECT DISTINCT date from status "
  if start_date:
    sql+="WHERE date >= '%s'" % start_date
  if end_date:
    if start_date:
      sql+=" AND "
    else:
      sql+=" WHERE "
    sql+="date <= '%s' " % end_date

  sql+="ORDER BY date"
  execute_sql(sql)
  rows = cursor.fetchall()
  days=[]
  for row in rows:
    days.append(row[0])

  missing_tables(days)
  conn.commit()
  conn.close()
  if verbose:
    print "------------------------"
    if dry_run:
      print "Total hours missing: %s" % row_count
    else:
      print "Total hours updated: %s" % row_count
  else:
    print row_count

if __name__ == "__main__":
   main(sys.argv[1:])
