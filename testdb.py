import datetime
import pymysql

#sql语句
curr_time = datetime.datetime.now()
db = pymysql.connect(host='123.57.246.9', user='root', password='199918', port=3306, db='oldcare')

cursor = db.cursor()
# sql语句
sql = "insert into event_info(event_type,event_desc,event_location) value(3,'有人摔倒!!!','走廊')"
try:
    cursor.execute(sql)
    print('Successful')
    db.commit()
except:
    print('Failed')
    db.rollback()
cursor.close()
db.close()