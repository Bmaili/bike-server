from pymysql import connect
from config import *


class DB(object):

    def __init__(self):
        """初始化数据库连接"""

        # 创建数据库连接
        self.conn = connect(host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASS,
                            database=DB_NAME,
                            port=DB_PORT)

        # 获得游标
        self.cursor = self.conn.cursor()

        self.commit = self.conn.commit

    def get_one(self, sql):
        """执行SQL查询"""

        # 执行SQL查询
        self.cursor.execute(sql)
        # 查询结果
        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        # 获得字段列表
        fields = [field[0] for field in self.cursor.description]

        # 保存返回结果
        return_data = dict()
        for field, value in zip(fields, query_result):
            return_data[field] = value

        return return_data

    def select_db(self, USERorBIKE_ID):
        '''执行数据库查询操作，查询用户或车'''

        if 'u' in USERorBIKE_ID:  # 用户
            sql = "select * from tb_user where user_ID='{}'".format(USERorBIKE_ID)
            return self.get_one(sql)

        elif 'b' in USERorBIKE_ID:  # 车辆
            sql = "select * from tb_bike where bike_ID='{}'".format(USERorBIKE_ID)
            return self.get_one(sql)

        else:  # 二手信息序号,序号是数字，故不用单引号
            sql = "select * from tb_resell where num= {}".format(USERorBIKE_ID)
            return self.get_one(sql)

    def update_db(self, set, results, USERorBIKE_ID):
        '''执行数据库修改操作'''

        if 'u' in USERorBIKE_ID:  # 用户
            sql = "update tb_user set {} = '{}' where user_ID = '{}'".format(set, results, USERorBIKE_ID)
            self.cursor.execute(sql)

        elif 'b' in USERorBIKE_ID:  # 车辆
            sql = "update tb_bike set {} = '{}' where bike_ID = '{}'".format(set, results, USERorBIKE_ID)
            self.cursor.execute(sql)

        else:
            return None

    def insert_db(self, host_ID, time, title, info):
        '''将二手出售信息插入数据库'''

        sql = "insert into tb_resell(host_ID,time,title,info) VALUES('{}','{}','{}','{}')".format(host_ID, time, title,
                                                                                                  info)
        self.cursor.execute(sql)

    def delete_db(self, num):
        '''将二手出售信息从数据库删除'''

        sql = "delete from tb_resell where num = {}".format(num)
        self.cursor.execute(sql)

    def close(self):
        '''关闭数据库连接'''

        self.cursor.close()
        self.conn.close()
