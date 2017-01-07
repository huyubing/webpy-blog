#coding=utf-8
import web, datetime
import os

db = web.database(dbn='sqlite', db='blog.db',  driver="sqlite3")

def get_posts():
    return db.select('entries', order='id DESC')

def get_post(id):
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow())

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text)

def list_dir(dir):
    '''找出目录下的所有文件夹'''
    list = os.listdir(dir)
    list_name = []
    for line in list:
        path_name = os.path.join(dir, line)
        if os.path.isdir(path_name):
            if path_name.find('.') < 0:
                list_name.append(line)
    return list_name

def get_svn_list():
    lists = list_dir("/Users/MacPro_huyubing");
    
    svn_list = {
        "test-svn1" : {
            "class": "1",
            "remarks": "note test-svn1"},
        "test-svn2" : {
            "class": "2",
            "remarks": "some remarks string"}}
    print svn_list
    return lists
