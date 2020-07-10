import datetime
import pymysql


def img_read_store(img_dir, type):
    # img_dir 为图片路径
    # img_name 为图片文件名
    conn = pymysql.connect(host='123.57.246.9', user='root',
                           passwd='199918', port=3306, db='oldcare', charset='utf8')
    # 数据库的连接操作，db指定所要操作数据库名称，user指定用户，passwd 指定数据库登陆密码，charset 指定数据库编码方式，本例中使用 utf-8 的编码方 式
    cur = conn.cursor()  # 设置游标
    try:
        myimg = open(img_dir, 'rb')
        # 由于数据库对图片的存储使用的是二进制的方式，那么在进行图片文件的读 #取中，则采用文本文件二进制的方式进行读取， #这样做的目的是在进行数据库存入的时候不必要再进行数据类型的强制转换
        data = myimg.read()
        cur.execute("INSERT INTO event_image (type, image)VALUES( % s, % s)", (type, data))
        # 执行数据库 SQL 语句
        cur.connection.commit()
    # 数据库语句提交
    except IOError as e:
        print("Encountered amistake")
        print("Error %d %s" % (e.args[0], e.args[1]))
        exit(1)
    cur.close()
    conn.close()


#img_read_store("plots/accuracy.png", 1)


def getbyname(fileID, savepath):


    # fileID,savepath 分别指定要提取的图片 ID 和要保存的图片路径
    """get img from mysql by NameImg """
    try:
        conn = pymysql.connect(host='123.57.246.9', user='root',
                           passwd='199918', port=3306, db='oldcare', charset='utf8')
        cur = conn.cursor()
        # 以上两行代码作用同上
        cur.execute("select image from event_image where id=%d" % fileID)
        # 执行图片提取的 SQL 语句
        print("img read successfully......")
        data = cur.fetchone()[0]
        imgout = open(savepath + "mysql-" + str(fileID)+".jpg", 'wb')
        # 以写的方式打开一个二进制文件，如果该文件不存在则创建
        imgout.write(data)
        # 将从数据库提取到的文件写入到刚刚建立的二进制文件中
        print("img save successfully......")
        cur.close()
        conn.close()  # 关闭数据库连接
        print("mysql close successfully......")
    except pymysql.Error as e:
        print("Error %d %s" % (e.args[0], e.args[1]))
        exit(1)

getbyname(3,"plots/")
