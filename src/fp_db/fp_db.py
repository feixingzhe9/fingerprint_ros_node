#!/usr/bin/env python
# coding=utf-8

import sys
import sqlite3
import rospkg

connect = None
cursor = None

rospack = rospkg.RosPack()

TABLE_FP = "fp_feature"
DB_PATH = rospack.get_path("fingerprint")
DB_PATH = DB_PATH + "/fp_feature_id.db"

def open_db():
    global connect
    global cursor
    connect = sqlite3.connect(DB_PATH)
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
        #print "table", TABLE_FP, " is NULL"
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
    #print '\n', exe_str, '\n'
    cursor.execute(exe_str)
    commit_db()
    close_db()


def get_all_db():
    #print sys._getframe().f_code.co_name, " start"
    global connect
    global cursor

    open_db()

    exe_str = "SELECT * FROM " + TABLE_FP
    #print '\n', exe_str, '\n'
    cursor.execute(exe_str)
    values = cursor.fetchall()

    close_db()
    #print "return values: ", values
    #print sys._getframe().f_code.co_name ," end"
    return values

def get_feature_rfid_name():
    #print sys._getframe().f_code.co_name
    global connect
    global cursor

    open_db()

    #features = ([])
    #values = get_all_db()
#    for i in range(0, len(values)):
#        print i
#        features.append([values[i][1], values[i][2], values[i][7]])

    exe_str = "SELECT UID, NAME, RFID, FP_FEATURE FROM " + TABLE_FP
    #print exe_str
    cursor.execute(exe_str)
    features = cursor.fetchall()

    close_db()

    #print features
    return features

def del_feature_by_uid(uid):
    global connect
    global cursor

    open_db()
    exe_str = "SELECT UID FROM " + TABLE_FP
    cursor.execute(exe_str)
    uid_db = cursor.fetchall()
    has_this_uid_flag = False
    for i in uid_db:
        #print "uid in database :", i
        if i[0] == uid:
            has_this_uid_flag = True
            break
    if has_this_uid_flag is not True:
        #print "No  uid ", uid, " in table ! !"
        return -1

    exe_str = "DELETE  FROM " + TABLE_FP + " WHERE UID = " + str(uid)
    print '\n', exe_str, '\n'
    cursor.execute(exe_str)

    commit_db()
    close_db()
    #print "return values: ", values
    #print sys._getframe().f_code.co_name ," end"
    return 0

def del_all_data():
    global connect
    global cursor

    open_db()

    exe_str = "DELETE  FROM " + TABLE_FP
    print '\n', exe_str, '\n'
    cursor.execute(exe_str)

    commit_db()
    close_db()
    return 0

if __name__ == '__main__':
    #insert_fp_feature("kaka", "1055", "1055", 1055, 1, 1, "abcdefg")
    get_feature_rfid_name()
    print 'pass'
