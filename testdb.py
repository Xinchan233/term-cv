import pymysql
conn = pymysql.connect(host='123.57.246.9', user = "root", passwd="199918", db="oldcare", port=3306, charset="utf8")
cur = conn.cursor()
#sql语句
sql = "insert into event_info(id, event_type,oldperson_id) value(%s, %s, %s)"
#数据
test = [[1, 1, 1], [2, 2, 1]]

for i in range(len(test)):
    param = tuple(test[i])
    #执行sql语句
    count = cur.execute(sql, param)
    #判断是否成功
    if count > 0:
        print("添加数据成功！\n")
#提交事务
conn.commit()

#查询数据
cur.execute("select * from event_info")
#获取数据
users = cur.fetchall();

for i in range(len(users)):
    print(users[i]);

#关闭资源连接
cur.close()
conn.close()
print("数据库断开连接！");