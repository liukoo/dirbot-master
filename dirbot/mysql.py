# -*- coding: utf-8 -*-
import MySQLdb
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('python')
    #写入
    val= 'liukoo'
    sql = "insert into test(value) values(%s)"
    #n = cur.execute(sql,val)
    #更新
    sql ="update test set value=%s where id=4"
    param =("inserting")
    #n = cur.execute(sql,param)
    #查询
    sql ="select * from test1"
    n= cur.execute(sql)
    num = 0
    money = 0
    if n:
        for row in cur.fetchall():
            num+=int(row[2])
            money+=float(row[3])*int(row[2])

        print num
        print money
    #删除
    sql ="delete from test1 where id>=10"
    #cur.execute(sql)
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
conn.commit()
cur.close()
conn.close()
