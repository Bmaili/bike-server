from threading import Thread
from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from db import DB
from config import *
import re


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
        self.register(USER_REQUEST_DELETEFRIEND, lambda sf, uID, data: self.request_deleteFriend_handle(sf, uID, data))
        self.register(USER_REQUEST_SHAREBACK, lambda sf, uID, data: self.request_shareBack_handle(sf, uID, data))
        self.register(USER_REQUEST_REPLYFRIEND, lambda sf, uID, data: self.request_replyFriend_handle(sf, uID, data))
        self.register(USER_REQUEST_USERRENAMED, lambda sf, uID, data: self.request_userRenamed_handle(sf, uID, data))
        self.register(USER_REQUEST_BIKERENAMED, lambda sf, uID, data: self.request_bikeRenamed_handle(sf, uID, data))
        self.register(USER_REQUEST_OPEN, lambda sf, uID, data: self.request_openBike_handle(sf, uID, data))

    def register(self, request_id, handle_function):
        """注册请求处理函数"""

        self.request_handle_functions[request_id] = handle_function

    @staticmethod
    def parse_request_text(request_text):
        """解析请求数据"""

        request_text_list = request_text.split(DELIMITER)
        # 保存请求数据
        request_data = dict()

        request_data['request_id'] = request_text_list[0]
        if request_text_list[0] == USER_REQUEST_FLUSH:  # 刷新请求
            pass
        elif request_text_list[0] == USER_REQUEST_THEBIKE:  # 具体某辆车
            request_data['bike_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_THEFRIEND:  # 具体某个好友
            request_data['friend_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_ADDFRIEND:  # 请求添加好友
            request_data['friend_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_SHAREBIKE:  # 分享车辆使用权
            request_data['bike_ID'] = request_text_list[1]
            request_data['friend_ID'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_DELETEFRIEND:  # 删除好友
            request_data['friend_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_SHAREBACK:  # 撤销好友车辆使用权
            request_data['bike_ID'] = request_text_list[1]
            request_data['friend_ID'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_REPLYFRIEND:  # 对他人好友请求的回应
            request_data['friend_ID'] = request_text_list[1]
            request_data['reply_num'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_USERRENAMED:  # 修改本人昵称
            request_data['new_nickname'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_BIKERENAMED:  # 修改车辆昵称
            request_data['bike_ID'] = request_text_list[1]
            request_data['new_nickname'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_OPEN:  # 开锁请求
            request_data['bike_ID'] = request_text_list[1]

        print("解析数据函数执行完毕！")
        print(request_data)
        return request_data

    def startup(self):
        """启动服务器"""

        while True:
            print("等待用户接入...")
            # 等待客户端连接
            sock, addr = self.server_socket.accept()
            # 给客户端sock增加额外功能
            client_sock = SocketWrapper(sock)

            # 启动线程处理该用户请求
            Thread(target=lambda: self.mylogin(client_sock, addr)).start()

    def mylogin(self, client_sock, addr):
        # 解析请求数据
        bool_login = False
        print(addr, '接入服务器', 'hello')
        request_data = client_sock.recv_data().split(DELIMITER)
        if request_data[0] == USER_REQUEST_LOGIN and request_data[1] and request_data[2] and len(request_data) == 3:
            user_ID = request_data[1]
            user_password = request_data[2]
            print(user_password)

            # 用户名和密码验证
            sql = "select * from tb_user where user_ID='" + user_ID + "'"
            db_conn = DB()
            results = db_conn.get_one(sql)

            if results:
                if results['user_password'] == user_password:
                    print(user_ID + '登陆成功')
                    client_sock.send_data(DELIMITER.join([USER_RESULT_LOGIN, '1']))
                    Thread(target=lambda: self.request_handle(client_sock, user_ID)).start()
                    bool_login = True
                else:
                    print("密码不对")
                    client_sock.send_data(DELIMITER.join([USER_RESULT_LOGIN, '2']))
            else:
                print("没这个用户")
                client_sock.send_data(DELIMITER.join([USER_RESULT_LOGIN, '3']))
        if not bool_login:
            client_sock.close()

    def request_handle(self, client_sock, user_ID):
        """响应处理函数"""
        try:
            while True:
                # 读取客户端数据
                request_text = client_sock.recv_data()
                if not request_text:
                    print("客户端下线!")
                    break
                # 解析请求数据
                request_data = self.parse_request_text(request_text)
                # 获取响应处理函数
                handle_function = self.request_handle_functions[request_data["request_id"]]
                if handle_function:
                    handle_function(client_sock, user_ID, request_data)
        except:
            client_sock.send_data(REQUEST_ERROR)
        finally:
            client_sock.close()

    def request_Flush_handle(self, client_sock, user_ID, request_data):
        '''处理刷新请求'''

        # 查询SQL
        sql = "select * from tb_user where user_ID='" + user_ID + "'"
        # 创建数据库连接对象
        db_conn = DB()
        results = db_conn.get_one(sql)
        user_nickname = results['user_nickname']
        pass

    def request_TheBike_handle(self, client_sock, user_ID, request_data):
        '''查看某辆车的具体信息'''

        bike_ID = request_data['bike_ID']
        sql_bike = "select * from tb_bike where bike_ID='" + bike_ID + "'"
        db_conn = DB()
        results_bike = db_conn.get_one(sql_bike)

        if not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print("非法请求，这车不存在")
            return

        if results_bike['bike_host'] != user_ID and len(
                re.findall(user_ID + DELIMITER_2, results_bike['bike_users'], re.S)) == 0:
            uesr_number = len(re.findall(DELIMITER_2, results_bike['bike_users'], re.S)) - 1
            client_sock.send_data(DELIMITER.join([USER_RESULT_THEBIKE, '2',
                                                  results_bike['bike_ID'],
                                                  results_bike['bike_nickname'],
                                                  results_bike['bike_host'],
                                                  str(uesr_number)]))
            print("你只能看部分数据！")
            return

        client_sock.send_data(DELIMITER.join([USER_RESULT_THEBIKE, '1',
                                              results_bike['bike_ID'],
                                              results_bike['bike_nickname'],
                                              results_bike['bike_status'],
                                              results_bike['bike_host'],
                                              results_bike['bike_users'],
                                              results_bike['bike_gps'],
                                              results_bike['bike_power']]))
        print("查看某辆车具体信息函数执行完毕")

    def request_TheFriend_handle(self, client_sock, user_ID, request_data):
        '''查看某个人的具体信息'''

        friend_ID = request_data['friend_ID']
        sql = "select * from tb_user where user_ID='" + friend_ID + "'"
        db_conn = DB()
        results = db_conn.get_one(sql)
        if not results:
            client_sock.send_data(DELIMITER.join([USER_RESULT_THEFRIEND, '2']))
            print("此人不存在")
            return

        client_sock.send_data(DELIMITER.join([USER_RESULT_THEFRIEND, '1',
                                              results['user_ID'],
                                              results['user_nickname'],
                                              results['user_status'],
                                              results['user_ownership']]))
        print('查看某个人的具体信息函数执行完毕')

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

        if len(re.findall(USER_MESSAGE_ADDFRIEND + DELIMITER_3 + user_ID + DELIMITER_2, results['user_message'],
                          re.S)) != 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '5']))
            print("你已经向他发送过好友请求了")
            return

        sql = "select * from tb_user where user_ID='" + user_ID + "'"
        results = db_conn.get_one(sql)

        if len(re.findall(makefriend_ID + DELIMITER_2, results['user_friend'], re.S)) != 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '2']))
            print("这个用户已经是你的好友了")
            return

        # 请求发送成功
        sql = "select * from tb_user where user_ID='" + makefriend_ID + "'"
        results = db_conn.get_one(sql)
        results['user_message'] += USER_MESSAGE_ADDFRIEND + DELIMITER_3 + user_ID + DELIMITER_2
        sql_2 = "update tb_user set user_message = '" + results[
            'user_message'] + "' where user_ID = '" + makefriend_ID + "'"
        db_conn.cursor.execute(sql_2)
        db_conn.commit()  # 提交数据
        client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '1']))
        print("请求添加好友函数执行完毕")

    def request_shareBike_handle(self, client_sock, user_ID, request_data):
        '''分享自行车骑行权限'''

        bike_ID = request_data['bike_ID']
        friend_ID = request_data['friend_ID']
        db_conn = DB()
        sql_friend = "select * from tb_user where user_ID='" + friend_ID + "'"
        results_friend = db_conn.get_one(sql_friend)
        sql_bike = "select * from tb_bike where bike_ID='" + bike_ID + "'"
        results_bike = db_conn.get_one(sql_bike)

        if not results_friend or not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if user_ID == friend_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '6']))
            print("不必把自己的车的使用权赋予自己！")
            return

        if results_bike['bike_host'] != user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '5']))
            print("这辆车的主人不是你！")
            return

        if not results_friend:  # 不存在这个用户
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '4']))
            print("不存在这个用户")
            return

        if len(re.findall(user_ID + DELIMITER_2, results_friend['user_friend'], re.S)) == 0:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '3']))
            return

        if len(re.findall(bike_ID + DELIMITER_2, results_friend['user_apply'], re.S)) != 0:
            print('人家已经有这辆车了！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '2']))
            return

        results_friend['user_apply'] += bike_ID + DELIMITER_2
        sql_fiend = "update tb_user set user_apply = '" + results_friend[
            'user_apply'] + "' where user_ID = '" + friend_ID + "'"
        db_conn.cursor.execute(sql_fiend)
        results_bike['bike_users'] += friend_ID + DELIMITER_2
        sql_bike = "update tb_bike set bike_users = '" + results_bike[
            'bike_users'] + "' where bike_ID = '" + bike_ID + "'"
        db_conn.cursor.execute(sql_bike)
        db_conn.commit()  # 提交数据
        client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '1']))
        print('分享自行车骑行权限函数执行完毕')

    def request_deleteFriend_handle(self, client_sock, user_ID, request_data):
        '''删除好友'''

        friend_ID = request_data['friend_ID']
        db_conn = DB()
        sql_me = "select * from tb_user where user_ID='" + user_ID + "'"
        results_me = db_conn.get_one(sql_me)

        if not results_me:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if len(re.findall(friend_ID + DELIMITER_2, results_me['user_friend'], re.S)) == 0:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_DELETEFRIEND, '2']))
            return

        # 正则表达式，将目标ID删掉
        myfriends = re.sub(friend_ID + DELIMITER_2, DELIMITER_0, results_me['user_friend'], re.S)
        sql_me = "update tb_user set user_friend = '" + myfriends + "' where user_ID = '" + user_ID + "'"
        db_conn.cursor.execute(sql_me)
        sql_him = "select * from tb_user where user_ID='" + friend_ID + "'"
        results_him = db_conn.get_one(sql_him)
        hisfriends = re.sub(user_ID + DELIMITER_2, DELIMITER_0, results_him['user_friend'], re.S)
        sql_him = "update tb_user set user_friend = '" + hisfriends + "' where user_ID = '" + friend_ID + "'"
        db_conn.cursor.execute(sql_him)
        db_conn.commit()  # 提交数据
        pass  # 还得删除车辆里的使用者

    def request_shareBack_handle(self, client_sock, user_ID, request_data):
        '''撤销好友的车辆使用权'''

        bike_ID = request_data['bike_ID']
        friend_ID = request_data['friend_ID']
        db_conn = DB()
        sql_friend = "select * from tb_user where user_ID='" + friend_ID + "'"
        results_friend = db_conn.get_one(sql_friend)
        sql_bike = "select * from tb_bike where bike_ID='" + bike_ID + "'"
        results_bike = db_conn.get_one(sql_bike)

        if not results_bike or not results_friend:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if results_bike['bike_host'] != user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '3']))
            print("这辆车的主人不是你！")
            return

        if len(re.findall(bike_ID + DELIMITER_2, results_friend['user_apply'], re.S)) == 0:
            print('人家没有这辆车了！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '2']))
            return

        hisbikes = re.sub(bike_ID + DELIMITER_2, DELIMITER_0, results_friend['user_apply'], re.S)
        sql_friend = "update tb_user set user_apply = '" + hisbikes + "' where user_ID = '" + friend_ID + "'"
        db_conn.cursor.execute(sql_friend)
        bike_users = re.sub(friend_ID + DELIMITER_2, DELIMITER_0, results_bike['bike_users'], re.S)
        sql_bike = "update tb_bike set bike_users = '" + bike_users + "' where bike_ID = '" + bike_ID + "'"
        db_conn.cursor.execute(sql_bike)
        db_conn.commit()  # 提交数据
        client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '1']))
        print('撤销好友的车辆使用权函数执行完毕')

    def request_replyFriend_handle(self, client_sock, user_ID, request_data):
        '''用户对他人好友请求的回应的响应'''

        friend_ID = request_data['friend_ID']
        reply_num = request_data['reply_num']

        # 不同意对方的好友请求
        if reply_num == '2' or user_ID == friend_ID:
            return

        # 同意对方的好友请求
        db_conn = DB()
        sql_me = "select * from tb_user where user_ID='" + user_ID + "'"
        results_me = db_conn.get_one(sql_me)
        results_me['user_friend'] += friend_ID + DELIMITER_2
        sql_me = "update tb_user set user_friend = '" + results_me[
            'user_friend'] + "' where user_ID = '" + user_ID + "'"
        db_conn.cursor.execute(sql_me)

        sql_him = "select * from tb_user where user_ID='" + friend_ID + "'"
        results_him = db_conn.get_one(sql_him)
        results_him['user_friend'] += user_ID + DELIMITER_2
        sql_him = "update tb_user set user_friend = '" + results_him[
            'user_friend'] + "' where user_ID = '" + friend_ID + "'"
        db_conn.cursor.execute(sql_him)
        db_conn.commit()
        print('用户对他人好友请求的回应的响应函数执行完毕')

    def request_userRenamed_handle(self, client_sock, user_ID, request_data):
        '''修改本人昵称'''

        new_nickname = request_data['new_nickname']

        if len(re.findall(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', new_nickname, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_USERRENAMED, '2']))
            print('修改昵称失败！昵称只能有汉字、字母、下划线')
            return

        db_conn = DB()
        sql = "update tb_user set user_nickname = '" + new_nickname + "' where user_ID = '" + user_ID + "'"
        db_conn.cursor.execute(sql)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_USERRENAMED, '1']))
        print('修改用户昵称函数执行完毕！')

    def request_bikeRenamed_handle(self, client_sock, user_ID, request_data):
        '''修改车辆昵称'''

        new_nickname = request_data['new_nickname']
        bike_ID = request_data['bike_ID']

        if len(re.findall(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', new_nickname, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '2']))
            print('修改昵称失败！昵称只能有汉字、字母、下划线')
            return

        db_conn = DB()
        sql_bike = "select * from tb_bike where bike_ID='" + bike_ID + "'"
        results_bike = db_conn.get_one(sql_bike)

        if not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print("非法请求")
            return

        if user_ID != results_bike['bike_host']:
            client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '3']))
            print('修改昵称失败！你不是该车主人')
            return

        sql_bike = "update tb_bike set bike_nickname = '" + new_nickname + "' where bike_ID = '" + bike_ID + "'"
        db_conn.cursor.execute(sql_bike)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '1']))
        print('修改车辆昵称函数执行完毕！')

    def request_openBike_handle(self, client_sock, user_ID, request_data):
        pass


if __name__ == "__main__":
    server = Server()
    server.startup()
