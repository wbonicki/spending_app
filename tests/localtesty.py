import datetime

date_string = '28-02-1931'

date_format = '%d-%m-%Y'

try:
   # dateObject = datetime.datetime.strptime(date_string, date_format)
   date_ = datetime.datetime.strptime(date_string, date_format)
   formatted_date = date_.strftime("%d-%m-%Y")
except ValueError:
   print("Incorrect data format, should be YYYY-MM-DD")
