#!/usr/bin/python

import pymongo

class mongo():
    def __init__(self, db_name, mongo_addr = 'localhost', mongo_port = 27017):
        self.con = pymongo.Connection(mongo_addr, mongo_port)
        self.db = self.con[db_name]
    
    def insert(self, table, data):
        user = self.db[table]
        user.insert(data)

if __name__ == '__main__':
    db = mongo('test')
    db.insert('t', {'20140902': [{'id': 1, 'name': 'test'}, {'id': 2, 'name': 't'}]})
