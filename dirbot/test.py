#coding:utf-8
import MySQLdb
conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
cur=conn.cursor()
conn.select_db('python')
sql ="select * from queue where stat='0' order by id asc limit 1"
sql_lock = "LOCK TABLES queue"
flag= cur.execute(sql)
if flag:
    line = cur.fetchone()
    cur.execute("LOCK TABLES queue READ")
    c_id = line[0]
    shop_url = line[1]
    cur.execute("UNLOCK TABLES")
    cur.execute("update queue set stat='1' where id=%d" % c_id)
    print shop_url