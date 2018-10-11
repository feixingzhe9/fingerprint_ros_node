#!/usr/bin/env python
# coding=utf-8

import sqlite3

connect = None
cursor = None

TABLE_FP = "fp_feature"

def open_db():
    global connect
    global cursor
    connect = sqlite3.connect("test.db")
    cursor = connect.cursor()

def close_db():
    global connect
    global cursor
    connect.close()

def commit_db():
    global connect
    connect.commit()
    
def create_table():
    global connect
    global cursor

    open_db()

    exe_str = "CREATE TABLE IF NOT EXISTS " + TABLE_FP + \
                " (UID INTEGER PRIMARY KEY NOT NULL, \
                NAME TEXT, \
                RFID TEXT NOT NULL, \
                PASSWORD TEXT NOT NULL,  \
                WORKER_ID INT NOT NULL, \
                DOOR_ID INT NOT NULL, \
                ID_TYPE INT NOT NULL, \
                FP_FEATURE TEXT NOT NULL)"

    cursor.execute(exe_str)
    connect.commit()
    close_db()

def get_max_uid():
    global connect
    global cursor

    open_db()
    exe_str = "SELECT max(UID) FROM " + TABLE_FP
    cursor.execute(exe_str)
    values = cursor.fetchall()
    print values

    if values[0][0] == None  :
        print "table", TABLE_FP, " is NULL"
        return 1
    else:
        return int(values[0][0]) + 1


def insert_fp_feature(name, rfid, password, worker_id, door_id, id_type, feature):
    global connect
    global cursor
    
    open_db()

    uid = get_max_uid()

    exe_str = "INSERT INTO " + TABLE_FP + " VALUES( " + str(uid) + ", "\
                                                 "\'" + name        + "\'" + ", " + \
                                                 "\'" + rfid        + "\'" + ", " + \
                                                 "\'" + password    + "\'" + ", " + \
                                                 str(worker_id)  +  ", " + \
                                                 str(door_id)    +  ", " + \
                                                 str(id_type)    + ", " + \
                                                 "\'" + feature     + "\'" + ")"
    print '\n', exe_str, '\n'
    cursor.execute(exe_str)
    commit_db()
    close_db()

if __name__ == '__main__':
    #insert_fp_feature("kaka", "1055", "1055", 1055, 1, 1, "abcdefg")
    print 'pass'
