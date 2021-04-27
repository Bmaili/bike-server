from threading import Thread
from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from db import DB
from config import *


class Server(object):
    """服务器"""

    def __init__(self):

        # 初始化套接字
        self.server_socket = ServerSocket()
        # 保存客户端连接套接字
        self.clients = dict()
        # 请求处理函数
        self.request_handle_functions = dict()
        # 注册请求处理函数

        self.register(USER_REQUEST_FLUSH, lambda sf, uID, data: self.request_Flush_handle(sf, uID, data))
        self.register(USER_REQUEST_THEBIKE, lambda sf, uID, data: self.request_TheBike_handle(sf, uID, data))
        self.register(USER_REQUEST_THEFRIEND, lambda sf, uID, data: self.request_TheFriend_handle(sf, uID, data))
        self.register(USER_REQUEST_ADDFRIEND, lambda sf, uID, data: self.request_addFriend_handle(sf, uID, data))
        self.register(USER_REQUEST_SHAREBIKE, lambda sf, uID, data: self.request_shareBike_handle(sf, uID, data))
        self.register(USER_REQUEST_OPEN, lambda sf, uID, data: self.request_openBike_handle(sf, uID, data))

    def register(self, request_id, handle_function):
        """注册请求处理函数"""
        self.request_handle_functions[request_id] = handle_function

    def startup(self):
        """启动服务器"""

        while True:
            print("等待用户接入...")
            # 等待客户端连接
            sock, addr = self.server_socket.accept()
            # 给客户端sock增加额外功能
            client_sock = SocketWrapper(sock)
            # 启动线程处理该用户请求
            print("有个客户端接入... 详情：", addr)
            user_ID = self.mylogin(client_sock, client_sock.recv_data())
            if user_ID:
                Thread(target=lambda: self.request_handle(client_sock, user_ID)).start()
            else:
                client_sock.close()

    def mylogin(self, client_sock, request_text):
        # 解析请求数据
        request_data = request_text.split(DELIMITER)
        if request_data[0] != USER_REQUEST_LOGIN or not request_data[1] or not request_data[2]:
            return False
        user_ID = request_data[1]
        user_password = request_data[2]
        print(user_password)
        """用户名和密码验证"""
        # 查询SQL
        sql = "select * from tb_user where user_ID='" + user_ID + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        # 未查询到数据
        if not results:
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '3']))
            print("没这个用户")
            return False
        # 用户名和密码不相等
        if results['user_password'] != user_password:
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '2']))
            print("密码不对")
            return False
        client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '1']))
        print(user_ID + '登陆成功')
        return user_ID

    @staticmethod
    def parse_request_text(request_text):
        """解析请求数据"""

        request_text_list = request_text.split(DELIMITER)
        print(request_text_list)
        # 保存请求数据
        request_data = dict()

        request_data['request_id'] = request_text_list[0]
        if request_text_list[0] == USER_REQUEST_FLUSH:  # 刷新请求
            pass
        elif request_text_list[0] == USER_REQUEST_THEBIKE:  # 具体某辆车
            request_data['bike_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_THEFRIEND:  # 具体某个好友
            request_data['friend_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_ADDFRIEND:  # 添加好友
            request_data['friend_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_SHAREBIKE:  # 分享车辆使用权
            request_data['bike_ID'] = request_text_list[1]
            request_data['friend_ID'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_OPEN:  # 开锁请求
            request_data['bike_ID'] = request_text_list[1]

        print("a号标记点")
        return request_data

    def request_handle(self, client_sock, user_ID):
        """响应处理函数"""

        while True:
            # 读取客户端数据
            request_text = client_sock.recv_data()
            if not request_text:
                print("客户端下线!")
                # self.remove_offline_user(client_sock)
                break
            # 解析请求数据
            request_data = self.parse_request_text(request_text)
            # 获取响应处理函数
            handle_function = self.request_handle_functions[request_data["request_id"]]
            if handle_function:
                handle_function(client_sock, user_ID, request_data)

        client_sock.close()

    def request_Flush_handle(self, client_sock, user_ID, request_data):
        '''处理刷新请求'''
        # 查询SQL
        sql = "select * from tb_user where user_ID='" + user_ID + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        user_nickname = results['user_nickname']

    def request_TheBike_handle(self, client_sock, user_ID, request_data):
        '''查看某辆车的具体信息'''
        bike_ID = request_data['bike_ID']
        # 查询SQL
        sql = "select * from tb_bike where bike_ID='" + bike_ID + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        if not results:
            return

        print(results)
        client_sock.send_data(DELIMITER.join([results['bike_ID'],
                                              results['bike_nickname'],
                                              results['bike_status'],
                                              results['bike_host'],
                                              results['bike_users'],
                                              results['bike_gps'],
                                              results['bike_power']]))

    def request_TheFriend_handle(self, client_sock, user_ID, request_data):
        '''查看某个好友的具体信息'''
        friend_ID = request_data['friend_ID']
        # 查询SQL
        sql = "select * from tb_user where user_ID='" + friend_ID + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        if not results:
            return
        print(results)
        client_sock.send_data(DELIMITER.join([results['user_ID'],
                                              results['user_nickname'],
                                              results['user_status']]))

    def request_addFriend_handle(self, client_sock, user_ID, request_data):
        '''添加好友'''
        makefriend_ID = request_data['friend_ID']
        if user_ID == makefriend_ID:
            client_sock.send_data(DELIMITER.join(USER_RESULT_ADDFRIEND, '4'))
            print("不能加自己为好友")
            return

        sql = "select * from tb_user where user_ID='" + makefriend_ID + "'"
        db_conn = DB()
        results = db_conn.get_one(sql)
        if not results:  # 不存在这个用户
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '3']))
            print("不存在这个用户")
            return

        sql_2 = "select * from tb_user where user_ID='" + user_ID + "'"
        results_2 = db_conn.get_one(sql_2)
        user_friends = []
        if results_2['user_friend']:
            user_friends = results_2['user_friend'].split(DELIMITER_2)

        if makefriend_ID in user_friends:  # 这个用户已经是你的好友了
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '2']))
            print("这个用户已经是你的好友了")
            return

        else:  # 请求发送成功
            sql_3 = "select * from tb_user where user_ID='" + makefriend_ID + "'"
            results_3 = db_conn.get_one(sql_3)
            results_3['user_message'] += DELIMITER_2 + USER_MESSAGE_ADDFRIEND + DELIMITER_3 + user_ID
            sql_2 = "update tb_user set user_message = '" + results_3[
                'user_message'].strip(DELIMITER_2) + "' where user_ID = '" + makefriend_ID + "'"
            db_conn.cursor.execute(sql_2)
            db_conn.commit()  # 提交数据
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '1']))
        print("请求添加好友函数执行完毕")

    def request_shareBike_handle(self, client_sock, user_ID, request_data):
        '''分享自行车骑行权限'''
        bike_ID = request_data['bike_ID']
        friend_ID = request_data['friend_ID']
        db_conn = DB()
        sql = "select * from tb_user where user_ID='" + user_ID + "'"
        results = db_conn.get_one(sql)
        user_friend = results['user_friend'].split(DELIMITER)
        if friend_ID not in user_friend:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_REQUEST_SHAREBIKE, '3']))
            return

        sql = "select * from tb_user where user_ID='" + friend_ID + "'"
        results = db_conn.get_one(sql)
        friend_apply = results['user_apply'].split(DELIMITER)
        if bike_ID in friend_apply:
            print('人家已经有这辆车了！')
            client_sock.send_data(DELIMITER.join([USER_REQUEST_SHAREBIKE, '2']))
            return
        else:
            results['user_apply'] += DELIMITER_2 + bike_ID
            sql = "update tb_user set user_apply = '" + results['user_apply'].strip(
                DELIMITER_2) + "' where user_ID = '" + friend_ID + "'"
            db_conn.cursor.execute(sql)
            sql = "select * from tb_bike where bike_ID='" + bike_ID + "'"
            results = db_conn.get_one(sql)
            results['bike_users'] += DELIMITER_2 + friend_ID
            sql = "update tb_bike set bike_users = '" + results['bike_users'].strip(
                DELIMITER_2) + "' where bike_ID = '" + bike_ID + "'"
            db_conn.cursor.execute(sql)
            db_conn.commit()  # 提交数据
        print('分享自行车骑行权限函数执行完毕')

    def request_openBike_handle(self, client_sock, user_ID, request_data):
        pass


if __name__ == "__main__":
    server = Server()
    server.startup()
