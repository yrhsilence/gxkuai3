##
# crawler all the data from url web.
##

import urllib2
import datetime
import os
import time
import traceback
import ConfigParser

from BeautifulSoup import BeautifulSoup
from multiprocessing import Process

from mongo import mongo

cf = ConfigParser.ConfigParser()
cf.read("conf.ini")

URL = cf.get('crawler', 'URL') 
DATE_FORMAT = cf.get('crawler', 'DATE_FORMAT')
DATA_DIR = cf.get('crawler', 'DATA_DIR')
MAX_DUR = cf.getint('crawler', 'MAX_DUR')
START_DATE = cf.get('crawler', 'START_DATE')

db_name = cf.get('db', 'name') 
db_addr = cf.get('db', 'addr')
db_port = cf.get('db', 'port')

def get_date_format(date_time):
    return date_time.strftime(DATE_FORMAT) 

def get_date_list(dur):
    n, date = 0, datetime.datetime.now()
    while(n < dur):
        form_date = get_date_format(date)
        if(form_date < START_DATE): break
        yield form_date
        date = date + datetime.timedelta(-1)
        n += 1
        
def get_url(date):
    return URL + date

def get_page(url):
    page = None
    try:
        page = urllib2.urlopen(url).read()
    except Exception, e:
        open('log/log.txt', 'w+').write(e)
    return page

def comb_data(period, win_number):
    comb = {}
    if(period == None or win_number == None):
        return None
    
    comb['period'] = period 
    comb['win_number'] = win_number
    comb['win_sum'] = reduce(lambda x, y: int(x) + int(y), win_number.split()) 
    return comb

def parse_page(page):
    data = []
    try:
        soup = BeautifulSoup(page)
        result = soup.findAll('td', attrs = {'class': "start"})  
        for item in result:
            period = item.get('data-period', None)
            win_number = item.get('data-win-number', None)
            comb = comb_data(period, win_number)
            if comb is not None: 
                data.append(comb)
    except Exception, e:
        open('log/log.txt', 'w+').write(e)
    return data

def write_file(date, data):
    fp = open(os.path.join(DATA_DIR, date), 'w')
    data = sorted(data, key = lambda x: x['period'])
    def write_one_record(record):
        pri = record['period'] + ": " + record['win_number'] + " ; " + str(record['win_sum']) + '\n'
        fp.write(pri)

    map(write_one_record, data)
    fp.close()

def store_db(date, data):
    db = mongo(db_name)
    db.insert('win_number', {'date': date, 'data': data})

def store(date, data):
    write_file(date, data) 
    store_db(date, data)
  
def process_date(date):
    data = parse_page(
               get_page(
                   get_url(date)))
    #print date, data
    store(date, data)

def main():
    try:
        date_list = get_date_list(MAX_DUR)
        #map(process_date, date_list)
        for date in date_list:
            p = Process(target=process_date, args=(date,))
            p.start()
    except Exception, e:
        msg = traceback.format_exc()            
        open('log/log.txt', 'w+').write(msg)

if __name__ == '__main__':
    main()
