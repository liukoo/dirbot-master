# -*- coding: utf-8 -*-
import MySQLdb
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('python')
    #写入
    val= 'liukoo'
    sql = "insert into test(value) values(%s)"
    n = cur.execute(sql,val)
    #更新
    sql ="update test set value=%s where id=4"
    param =("inserting")
    #n = cur.execute(sql,param)
    #查询
    sql ="select id from test where id=1"
    n= cur.execute(sql)
    if n:
        for row in cur.fetchall():
            print int(row[0])
    #删除
    sql ="delete from test where id>=10"
    #cur.execute(sql)
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
conn.commit()
cur.close()
conn.close()
