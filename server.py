import re
import time
from db import DB
from config import *
from threading import Thread
from socket_wrapper import SocketWrapper
from socket import socket, AF_INET, SOCK_STREAM


class Server(object):
    """服务器"""

    def __init__(self):

        self.server_socket = socket(AF_INET, SOCK_STREAM)

        # 绑定本地IP和PORT
        self.server_socket.bind((SERVER_IP, SERVER_PORT))

        # 设置最大被动监听数
        self.server_socket.listen(128)

        # 保存客户端在线连接套接字，键为客户端ID，值为套接字
        self.online_clients = dict()

        # 请求处理函数
        self.request_handle_functions = dict()

        # 服务器初始化操作，包括：把所有客户端状态初始化为离线
        self.server_init()

        # 注册请求处理函数
        self.register(USER_REQUEST_FLUSH, lambda cli, uid, data: self.request_Flush_handle(cli, uid, data))
        self.register(USER_REQUEST_THEBIKE, lambda cli, uid, data: self.request_TheBike_handle(cli, uid, data))
        self.register(USER_REQUEST_THEFRIEND, lambda cli, uid, data: self.request_TheFriend_handle(cli, uid, data))
        self.register(USER_REQUEST_ADDFRIEND, lambda cli, uid, data: self.request_addFriend_handle(cli, uid, data))
        self.register(USER_REQUEST_SHAREBIKE, lambda cli, uid, data: self.request_shareBike_handle(cli, uid, data))
        self.register(USER_REQUEST_DELFRIEND, lambda cli, uid, data: self.request_deleteFriend_handle(cli, uid, data))
        self.register(USER_REQUEST_SHAREBACK, lambda cli, uid, data: self.request_shareBack_handle(cli, uid, data))
        self.register(USER_REQUEST_REPLYFRIEND, lambda cli, uid, data: self.request_replyFriend_handle(cli, uid, data))
        self.register(USER_REQUEST_USERRENAMED, lambda cli, uid, data: self.request_userRenamed_handle(cli, uid, data))
        self.register(USER_REQUEST_BIKERENAMED, lambda cli, uid, data: self.request_bikeRenamed_handle(cli, uid, data))
        self.register(USER_REQUEST_OPEN, lambda cli, uid, data: self.request_openBike_handle(cli, uid, data))
        self.register(USER_REQUEST_CHAT, lambda cli, uid, data: self.request_requestChat_handle(cli, uid, data))
        self.register(USER_REQUEST_SELLBIKE, lambda cli, uid, data: self.request_sellBike_handle(cli, uid, data))
        self.register(USER_REQUEST_ONESELL, lambda cli, uid, data: self.request_oneSell_handle(cli, uid, data))
        self.register(USER_REQUEST_MYSELL, lambda cli, uid, data: self.request_mySell_handle(cli, uid, data))
        self.register(USER_REQUEST_DELSELL, lambda cli, uid, data: self.request_delSell_handle(cli, uid, data))
        self.register(USER_REQUEST_STARSELL, lambda cli, uid, data: self.request_starSell_handle(cli, uid, data))
        self.register(USER_REQUEST_CLOSEONLINE, lambda cli, uid, data: self.request_closeOnline_handle(cli, uid, data))

        self.register(BIKE_PUSH_INFO, lambda cli, uid, data: self.request_pushInfo_handle(cli, uid, data))
        self.register(BIKE_RESULT_OPEN, lambda cli, uid, data: self.result_replyOpen_handle(cli, uid, data))
        self.register(BIKE_CLOSE, lambda cli, uid, data: self.request_closeBike_handle(cli, uid, data))
        self.register(BIKE_OPENBYNFC, lambda cli, uid, data: self.request_openByNFC_handle(cli, uid, data))
        self.register(BIKE_STOLEN, lambda cli, uid, data: self.request_bikeStolen_handle(cli, uid, data))
        self.register(BIKE_SPEEDING, lambda cli, uid, data: self.request_Speeding_handle(cli, uid, data))
        self.register(BIKE_RESULT_CLOSE, lambda cli, uid, data: self.result_closedOnline_handle(cli, uid, data))
        self.register(BIKE_PUSH_GPS, lambda cli, uid, data: self.result_pushGPS_handle(cli, uid, data))

    def register(self, request_id, handle_function):
        """注册请求处理函数"""
        self.request_handle_functions[request_id] = handle_function

    def server_init(self):
        '''服务器初始化操作，包括：把所有客户端状态初始化为离线'''
        db_conn = DB()
        sql = "UPDATE tb_user SET STATUS='{}'".format(STATUS[3])
        db_conn.cursor.execute(sql)
        sql = "UPDATE tb_bike SET STATUS='{}'".format(STATUS[3])
        db_conn.cursor.execute(sql)
        db_conn.commit()
        db_conn.close()

    @staticmethod
    def parse_request_text(request_text):
        """解析请求数据"""

        # 解析并保存数据
        request_text_list = request_text.split(DELIMITER)
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
        elif request_text_list[0] == USER_REQUEST_DELFRIEND:  # 删除好友
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
        elif request_text_list[0] == USER_REQUEST_CHAT:  # 请求聊天
            request_data['friend_ID'] = request_text_list[1]
            request_data['info'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_SELLBIKE:  # 发一条卖车信息
            request_data['title'] = request_text_list[1]
            request_data['info'] = request_text_list[2]
        elif request_text_list[0] == USER_REQUEST_ONESELL:  # 查看一条卖车信息
            request_data['sell_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_MYSELL:  # 查看我的转卖信息(大致的）
            pass
        elif request_text_list[0] == USER_REQUEST_DELSELL:  # 删除某条转卖信息
            request_data['sell_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_STARSELL:  # 想买某辆转卖车辆
            request_data['sell_ID'] = request_text_list[1]
        elif request_text_list[0] == USER_REQUEST_CLOSEONLINE:  # 用户远程关锁
            request_data['bike_ID'] = request_text_list[1]


        elif request_text_list[0] == BIKE_PUSH_INFO:  # 车辆向云端发送自己的数据
            request_data['status'] = request_text_list[1]
            request_data['power'] = request_text_list[2]
            request_data['lsat_ID'] = request_text_list[3]
        elif request_text_list[0] == BIKE_RESULT_OPEN:  # 车辆回应开锁结果
            request_data['reply_num'] = request_text_list[1]
            request_data['user_ID'] = request_text_list[2]
        elif request_text_list[0] == BIKE_CLOSE:  # 车辆手动关锁
            request_data['user_ID'] = request_text_list[1]
        elif request_text_list[0] == BIKE_OPENBYNFC:  # 因为NFC被开锁
            pass
        elif request_text_list[0] == BIKE_STOLEN:  # 车被偷了
            pass
        elif request_text_list[0] == BIKE_SPEEDING:  # 车辆超速了
            request_data['user_ID'] = request_text_list[1]
            request_data['speed'] = request_text_list[2]
            request_data['gps'] = request_text_list[3]
        elif request_text_list[0] == BIKE_RESULT_CLOSE:  # 车辆回应云端关锁指令
            request_data['reply_num'] = request_text_list[1]
            request_data['close_user_ID'] = request_text_list[2]
        elif request_text_list[0] == BIKE_PUSH_GPS:  # 发送自己的GPS
            request_data['gps'] = request_text_list[1]

        print("解析数据函数执行完毕！")
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
            Thread(target=lambda: self.request_login(client_sock, addr)).start()

    def request_login(self, client_sock, addr):
        # 验证登陆函数

        bool_login = False
        print(addr, '接入服务器', 'hello')
        request_text = client_sock.recv_data()
        request_data = request_text.split(DELIMITER)
        # request_data = client_sock.recv_data().split(DELIMITER)
        print(request_text)

        # 判断接收到的数据是否是登陆请求
        if (request_data[0] == USER_REQUEST_LOGIN or request_data[0] == BIKE_REQUEST_LOGIN) \
                and request_data[1] and request_data[2]:

            USERorBIKE_ID = request_data[1]
            userorBIKE_password = request_data[2]

            # 读取数据库中的信息
            db_conn = DB()
            results = db_conn.select_db(USERorBIKE_ID)

            # 判断接入的是车辆还是用户
            RESULT_LOGIN = USER_RESULT_LOGIN if 'u' in USERorBIKE_ID else BIKE_REQUEST_LOGIN

            if results:

                # 查看这个用户是否已经在线
                if (USERorBIKE_ID not in self.online_clients) or results['status'] == 3:

                    if results['password'] == userorBIKE_password:
                        print(USERorBIKE_ID + '登陆成功')

                        # 将那个人或车的状态改为"在线"，注意:车辆NFC开锁时主人状态为骑行２
                        if results['status'] == 3:
                            db_conn.update_db('status', STATUS[1], USERorBIKE_ID)
                            db_conn.commit()

                        # 保存用户或车辆连接套接字
                        self.online_clients[USERorBIKE_ID] = client_sock

                        client_sock.send_data(DELIMITER.join([RESULT_LOGIN, '1']))

                        Thread(target=lambda: self.request_handle(client_sock, USERorBIKE_ID)).start()

                        # 查看用户是否有留言，有就发给他
                        if 'u' in USERorBIKE_ID:
                            results = db_conn.select_db(USERorBIKE_ID)
                            message = results['message']
                            message_num = message.count(DELIMITER_2) - 1
                            if message_num >= 1:
                                message = message.replace(DELIMITER_3, DELIMITER).strip(DELIMITER_2)
                                message_list = message.split(DELIMITER_2)
                                for m in message_list:
                                    client_sock.send_data(m)

                                db_conn.update_db('message', DELIMITER_2, USERorBIKE_ID)
                                db_conn.commit()

                        db_conn.close()

                        bool_login = True

                    else:
                        print("密码不对")
                        client_sock.send_data(DELIMITER.join([RESULT_LOGIN, '2']))

                else:
                    print("此账号已经登陆了！")
                    client_sock.send_data(DELIMITER.join([RESULT_LOGIN, '4']))

            else:
                print("此账户未注册！")
                client_sock.send_data(DELIMITER.join([RESULT_LOGIN, '3']))

        if not bool_login:
            client_sock.close()

    def request_handle(self, client_sock, USERorBIKE_ID):
        """响应处理函数"""
        try:
            while True:
                # 持续等待接收客户端数据
                request_text = client_sock.recv_data()

                # 解析请求数据
                request_data = self.parse_request_text(request_text)
                print(request_data)

                # 获取响应处理函数
                handle_function = self.request_handle_functions[request_data["request_id"]]

                if handle_function:
                    handle_function(client_sock, USERorBIKE_ID, request_data)
        except:
            print("客户端下线!")
            client_sock.close()
            # 将那个客户端在线套接字删掉
            del self.online_clients[USERorBIKE_ID]
            # 将那个人或车的状态改为"离线"
            db_conn = DB()
            db_conn.update_db('status', STATUS[3], USERorBIKE_ID)
            db_conn.commit()
            db_conn.close()


    def request_Flush_handle(self, client_sock, user_ID, request_data):
        '''处理刷新请求'''

        pass


    def request_TheBike_handle(self, client_sock, user_ID, request_data):
        '''查看某辆车的具体信息'''

        db_conn = DB()
        bike_ID = request_data['bike_ID']
        results_bike = db_conn.select_db(bike_ID)

        if not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print("非法请求，这车不存在")
            return

        if results_bike['host'] != user_ID and len(
                re.findall(user_ID + DELIMITER_2, results_bike['bike_users'], re.S)) == 0:
            uesr_number = len(re.findall(DELIMITER_2, results_bike['bike_users'], re.S)) - 1
            client_sock.send_data(DELIMITER.join([USER_RESULT_THEBIKE, '2',
                                                  results_bike['bike_ID'],
                                                  results_bike['nickname'],
                                                  results_bike['host'],
                                                  str(uesr_number)]))
            print("你只能看部分数据！")
            return

        client_sock.send_data(DELIMITER.join([USER_RESULT_THEBIKE, '1',
                                              results_bike['bike_ID'],
                                              results_bike['nickname'],
                                              results_bike['status'],
                                              results_bike['host'],
                                              results_bike['bike_users'],
                                              results_bike['gps'],
                                              results_bike['power']]))

        print("查看某辆车具体信息函数执行完毕")


    def request_TheFriend_handle(self, client_sock, user_ID, request_data):
        '''查看某个人的具体信息'''

        db_conn = DB()
        results = db_conn.select_db(request_data['friend_ID'])

        if not results:
            client_sock.send_data(DELIMITER.join([USER_RESULT_THEFRIEND, '2']))
            print("此人不存在")
            return

        client_sock.send_data(DELIMITER.join([USER_RESULT_THEFRIEND, '1',
                                              results['user_ID'],
                                              results['nickname'],
                                              results['status'],
                                              results['ownership']]))
        print('查看某个人的具体信息函数执行完毕')


    def request_addFriend_handle(self, client_sock, user_ID, request_data):
        '''添加好友'''

        makefriend_ID = request_data['friend_ID']
        if user_ID == makefriend_ID:
            client_sock.send_data(DELIMITER.join(USER_RESULT_ADDFRIEND, '4'))
            print("不能加自己为好友")
            return

        db_conn = DB()
        results = db_conn.select_db(makefriend_ID)
        if not results:  # 不存在这个用户
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '3']))
            print("不存在这个用户")
            return

        if len(re.findall(USER_MESSAGE_ADDFRIEND + DELIMITER_3 + user_ID + DELIMITER_3, results['message'],
                          re.S)) != 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '5']))
            print("你已经向他发送过好友请求了")
            return

        results = db_conn.select_db(user_ID)

        if len(re.findall(makefriend_ID + DELIMITER_2, results['friend'], re.S)) != 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '2']))
            print("这个用户已经是你的好友了")
            return

        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        # 看对方是否在线，在线就直接发给他
        friend_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == makefriend_ID:
                friend_sock = sock
                break

        if not friend_sock:
            # 对方不在线，将信息存到数据库
            results = db_conn.select_db(makefriend_ID)
            results['message'] += USER_MESSAGE_ADDFRIEND + DELIMITER_3 + user_ID + DELIMITER_3 + time_now + DELIMITER_2

            db_conn.update_db('message', results['message'], makefriend_ID)
            db_conn.commit()  # 提交数据
            client_sock.send_data(DELIMITER.join([USER_RESULT_ADDFRIEND, '1']))
            print("对方不在线，留言成功！")
            return

        message = USER_MESSAGE_ADDFRIEND + DELIMITER + user_ID + DELIMITER + time_now
        friend_sock.send_data(message)
        print('对方在线，信息发送成功！')


    def request_shareBike_handle(self, client_sock, user_ID, request_data):
        '''分享自行车骑行权限'''

        bike_ID = request_data['bike_ID']
        friend_ID = request_data['friend_ID']
        db_conn = DB()
        results_bike = db_conn.select_db(bike_ID)
        results_friend = db_conn.select_db(friend_ID)

        if not results_friend or not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if user_ID == friend_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '6']))
            print("不必把自己的车的使用权赋予自己！")
            return

        if results_bike['host'] != user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '5']))
            print("这辆车的主人不是你！")
            return

        if not results_friend:  # 不存在这个用户
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '4']))
            print("不存在这个用户")
            return

        if len(re.findall(user_ID + DELIMITER_2, results_friend['friend'], re.S)) == 0:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '3']))
            return

        if len(re.findall(bike_ID + DELIMITER_2, results_friend['use_power'], re.S)) != 0:
            print('人家已经有这辆车了！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '2']))
            return

        results_friend['use_power'] += bike_ID + DELIMITER_2
        db_conn.update_db('use_power', results_friend['use_power'], friend_ID)
        results_bike['bike_users'] += friend_ID + DELIMITER_2
        db_conn.update_db('bike_users', results_bike['bike_users'], bike_ID)
        db_conn.commit()

        client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBIKE, '1']))
        print('分享自行车骑行权限函数执行完毕')


    def request_deleteFriend_handle(self, client_sock, user_ID, request_data):
        '''删除好友'''

        friend_ID = request_data['friend_ID']
        db_conn = DB()
        results_me = db_conn.select_db(user_ID)
        results_him = db_conn.select_db(friend_ID)

        if not results_me or not results_him:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if len(re.findall(friend_ID + DELIMITER_2, results_me['friend'], re.S)) == 0:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_DELFRIEND, '2']))
            return

        # 正则表达式，将目标ID删掉
        myfriends = re.sub(friend_ID + DELIMITER_2, KONGBAI, results_me['friend'], re.S)

        db_conn.update_db('friend', myfriends, user_ID)
        hisfriends = re.sub(user_ID + DELIMITER_2, KONGBAI, results_him['friend'], re.S)

        db_conn.update_db('friend', hisfriends, friend_ID)
        db_conn.commit()  # 提交数据
        print('删除好友成功')

        # 还得删除车辆里的使用者
        del_bike = results_me['ownership'].split(DELIMITER_2)
        for bike in del_bike:
            results_bike = db_conn.select_db(bike)
            if results_bike:
                if len(re.findall(friend_ID + DELIMITER_2, results_bike['bike_users'], re.S)) != 0:
                    new_users = re.sub(friend_ID + DELIMITER_2, KONGBAI, results_bike['bike_users'], re.S)
                    db_conn.update_db('bike_users', new_users, bike)
                    new_apply = re.sub(bike + DELIMITER_2, KONGBAI, results_him['use_power'], re.S)
                    db_conn.update_db('use_power', new_apply, friend_ID)

        del_bike = results_him['ownership'].split(DELIMITER_2)
        for bike in del_bike:
            results_bike = db_conn.select_db(bike)
            if results_bike:
                if len(re.findall(user_ID + DELIMITER_2, results_bike['bike_users'], re.S)) != 0:
                    new_users = re.sub(user_ID + DELIMITER_2, KONGBAI, results_bike['bike_users'], re.S)
                    db_conn.update_db('bike_users', new_users, bike)
                    new_apply = re.sub(bike + DELIMITER_2, KONGBAI, results_me['use_power'], re.S)
                    db_conn.update_db('use_power', new_apply, user_ID)

        db_conn.commit()  # 提交数据
        client_sock.send_data(DELIMITER.join([USER_RESULT_DELFRIEND, '1']))
        print('删除对方车辆的使用权，删除好友函数执行完毕')


    def request_shareBack_handle(self, client_sock, user_ID, request_data):
        '''撤销好友的车辆使用权'''

        bike_ID = request_data['bike_ID']
        friend_ID = request_data['friend_ID']

        db_conn = DB()
        results_friend = db_conn.select_db(friend_ID)
        results_bike = db_conn.select_db(bike_ID)

        if not results_bike or not results_friend:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if results_bike['host'] != user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '3']))
            print("这辆车的主人不是你！")
            return

        if len(re.findall(bike_ID + DELIMITER_2, results_friend['use_power'], re.S)) == 0:
            print('人家没有这辆车了！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '2']))
            return

        hisbikes = re.sub(bike_ID + DELIMITER_2, KONGBAI, results_friend['use_power'], re.S)
        db_conn.update_db('use_power', hisbikes, friend_ID)
        bike_users = re.sub(friend_ID + DELIMITER_2, KONGBAI, results_bike['bike_users'], re.S)

        db_conn.update_db('bike_users', bike_users, bike_ID)
        db_conn.commit()  # 提交数据
        client_sock.send_data(DELIMITER.join([USER_RESULT_SHAREBACK, '1']))
        print('撤销好友的车辆使用权函数执行完毕')


    def request_replyFriend_handle(self, client_sock, user_ID, request_data):
        '''用户对他人好友请求的回应的响应'''

        friend_ID = request_data['friend_ID']
        reply_num = request_data['reply_num']

        db_conn = DB()

        results_me = db_conn.select_db(user_ID)

        # 不同意对方的好友请求
        if reply_num == '2' or user_ID == friend_ID or len(
                re.findall(friend_ID + DELIMITER_2, results_me['friend'], re.S)) != 0:
            return

        # 同意对方的好友请求
        db_conn = DB()
        results_me['friend'] += friend_ID + DELIMITER_2
        db_conn.update_db('friend', results_me['friend'], user_ID)
        results_me = db_conn.select_db(user_ID)
        results_me['friend'] += friend_ID + DELIMITER_2
        db_conn.update_db('friend', results_me['friend'], user_ID)

        results_him = db_conn.select_db(friend_ID)
        results_him['friend'] += user_ID + DELIMITER_2

        db_conn.update_db('friend', results_him['friend'], friend_ID)
        db_conn.commit()
        print('用户对他人好友请求的回应的响应函数执行完毕')


    def request_userRenamed_handle(self, client_sock, user_ID, request_data):
        '''修改本人昵称'''

        new_nickname = request_data['new_nickname']

        if len(re.findall(REGULAR_NICKNAME, new_nickname, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_USERRENAMED, '2']))
            print('修改昵称失败！昵称只能有1至8位汉字、字母、数字、下划线')
            return

        db_conn = DB()
        db_conn.update_db('nickname', new_nickname, user_ID)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_USERRENAMED, '1']))
        print('修改用户昵称函数执行完毕！')


    def request_bikeRenamed_handle(self, client_sock, user_ID, request_data):
        '''修改车辆昵称'''

        new_nickname = request_data['new_nickname']
        bike_ID = request_data['bike_ID']

        if len(re.findall(REGULAR_NICKNAME, new_nickname, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '2']))
            print('修改昵称失败！昵称只能有1至8位汉字、字母、数字、下划线')
            return

        db_conn = DB()
        results_bike = db_conn.select_db(bike_ID)

        if not results_bike:
            client_sock.send_data(REQUEST_ERROR)
            print("非法请求")
            return

        if user_ID != results_bike['host']:
            client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '3']))
            print('修改昵称失败！你不是该车主人')
            return

        db_conn.update_db('nickname', new_nickname, bike_ID)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_BIKERENAMED, '1']))
        print('修改车辆昵称函数执行完毕！')


    def request_openBike_handle(self, client_sock, user_ID, request_data):
        '''请求开锁'''

        bike_ID = request_data['bike_ID']
        db_conn = DB()
        results_bike = db_conn.select_db(bike_ID)

        if not results_bike:
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '3']))
            print('这车不存在')
            return

        if user_ID != results_bike['host'] and len(
                re.findall(user_ID + DELIMITER_2, results_bike['bike_users'], re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '2']))
            print('你没有权限使用这辆车')
            return

        if bike_ID not in self.online_clients:
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '5']))
            print('这车不在线')
            return

        if results_bike['status'] == '2':
            client_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '4']))
            print('这车正在被骑行中')
            return

        bike_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == bike_ID:
                bike_sock = sock
                break

        if not bike_sock:
            client_sock.send_data(REQUEST_ERROR)
            return

        bike_sock.send_data(DELIMITER.join([BIKE_REQUEST_OPEN, user_ID]))
        print('请求开锁函数执行完毕')


    def result_replyOpen_handle(self, client_sock, bike_ID, request_data):
        '''自行车的开锁回应'''

        reply_num = request_data['reply_num']
        user_ID = request_data['user_ID']

        user_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == user_ID:
                user_sock = sock
                break

        if reply_num == '2':
            print('开锁失败')
            if user_sock:
                user_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '2']))
            return

        # 向用户端发送开锁成功的信息
        if user_sock:
            user_sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '1']))

        # 数据库将用户与车辆状态改为骑行
        db_conn = DB()
        db_conn.update_db('status', STATUS[2], user_ID)
        db_conn.update_db('status', STATUS[2], bike_ID)
        db_conn.commit()
        db_conn.close()


    def request_closeBike_handle(self, client_sock, bike_ID, request_data):
        '''手动关锁'''

        db_conn = DB()
        db_conn.update_db('status', STATUS[1], bike_ID)
        db_conn.commit()

        user_ID = request_data['user_ID']

        user_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == user_ID:
                user_sock = sock
                break

        if user_sock:
            db_conn.update_db('status', STATUS[1], user_ID)
            user_sock.send_data(USER_PUSH_CLOSE)
        else:
            db_conn.update_db('status', STATUS[3], user_ID)

        db_conn.commit()
        db_conn.close()
        print('手动关锁函数执行完毕')


    def request_openByNFC_handle(self, client_sock, bike_ID, request_data):
        '''车辆因NFC被开锁'''

        # 将车的状态标记为骑行
        db_conn = DB()
        results = db_conn.select_db(bike_ID)
        host_ID = results['host']

        db_conn.update_db('status', STATUS[2], bike_ID)
        db_conn.update_db('status', STATUS[2], host_ID)
        db_conn.commit()

        # 看主人是否客户端在线,向他发送开锁成功的消息
        for online_id, sock in self.online_clients.items():
            if online_id == host_ID:
                sock.send_data(DELIMITER.join([USER_RESULT_OPEN, '1']))
                break

        db_conn.close()
        print('车辆因NFC开锁函数执行完毕')


    def request_requestChat_handle(self, client_sock, user_ID, request_data):
        '''聊天请求'''

        text_info = request_data['info']
        if len(re.findall(REGULAR_INFO, text_info, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_CHAT, '3']))
            print('发送内容失败，只能匹配1至150位汉字、字母、数字、下划线、还有部分中文标点  。 ； ， ： “ ”（ ） 、 ？ 《 》 这些符号')
            return

        friend_ID = request_data['friend_ID']
        db_conn = DB()
        results_friend = db_conn.select_db(friend_ID)

        if not results_friend:
            client_sock.send_data(REQUEST_ERROR)
            print('非法请求')
            return

        if len(re.findall(user_ID + DELIMITER_2, results_friend['friend'], re.S)) == 0:
            print('这个人不是你的好友哦！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_CHAT, '2']))
            return

        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        # 看对方是否在线，在线就直接发给他
        friend_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == friend_ID:
                friend_sock = sock
                break

        if not friend_sock:
            results_friend[
                'message'] += USER_MESSAGE_CHAT + DELIMITER_3 + user_ID + DELIMITER_3 + time_now + DELIMITER_3 + text_info + DELIMITER_2

            print('对方不在线，留言成功！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_CHAT, '1']))
            db_conn.update_db('message', results_friend['message'], friend_ID)
            db_conn.commit()
            db_conn.close()
            return

        message = USER_MESSAGE_CHAT + DELIMITER + user_ID + DELIMITER + time_now + DELIMITER + text_info
        friend_sock.send_data(message)
        print('对方在线，信息发送成功！')


    def request_sellBike_handle(self, client_sock, user_ID, request_data):
        '''把车子挂到聊天室'''

        text_title = request_data['title']
        text_info = request_data['info']

        if len(re.findall(REGULAR_TITLE, text_title, re.S)) == 0 or \
                len(re.findall(REGULAR_INFO, text_info, re.S)) == 0:
            client_sock.send_data(DELIMITER.join([USER_RESULT_SELLBIKE, '2']))
            print('发送内容失败，只能匹配限定数量的汉字、字母、数字、下划线、还有部分中文标点  。 ； ， ： “ ”（ ） 、 ？ 《 》 这些符号')
            return

        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        db_conn = DB()
        db_conn.insert_db(user_ID, time_now, text_title, text_info)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_SELLBIKE, '1']))
        print('成功把信息挂上去了！')
        db_conn.close()


    def request_oneSell_handle(self, client_sock, user_ID, request_data):
        '''查看转卖墙上的具体的某一条信息'''

        sell_ID = request_data['sell_ID']
        db_conn = DB()
        results = db_conn.select_db(sell_ID)
        if not results:
            client_sock.send_data(REQUEST_ERROR)
            return

        text = USER_RESULT_ONESELL + DELIMITER + sell_ID + DELIMITER + results['host_ID'] + DELIMITER + results[
            'time'] + DELIMITER + results['title'] + DELIMITER + results['info']
        client_sock.send_data(text)
        print('查看转卖墙上的具体的某一条信息执行成功')
        db_conn.close()


    def request_mySell_handle(self, client_sock, user_ID, request_data):
        '''查看我的转卖信息(大致的）'''

        db_conn = DB()
        sql = "SELECT * FROM tb_resell WHERE host_ID = '{}'".format(user_ID)
        db_conn.cursor.execute(sql)
        query_result = db_conn.cursor.fetchall()

        if not query_result:
            client_sock.send_data(REQUEST_ERROR)
            return

        for query in query_result:
            li = list(query)
            li[0] = str(li[0])
            li = USER_RESULT_MYSELL + DELIMITER + DELIMITER.join(li)
            client_sock.send_data(li)

        print('查看我的转卖信息(大致的）函数执行完毕')
        db_conn.close()


    def request_delSell_handle(self, client_sock, user_ID, request_data):
        '''删除某条转卖信息'''

        sell_ID = request_data['sell_ID']
        db_conn = DB()
        results = db_conn.select_db(sell_ID)

        # 不存在这信息或者你不是发布它的主人
        if not results or results['host_ID'] != user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_DELSELL, '2']))
            return

        db_conn.delete_db(sell_ID)
        db_conn.commit()
        client_sock.send_data(DELIMITER.join([USER_RESULT_DELSELL, '1']))
        print('成功把转卖信息删了！')
        db_conn.close()


    def request_starSell_handle(self, client_sock, user_ID, request_data):
        '''想买某辆转卖车辆'''

        sell_ID = request_data['sell_ID']
        db_conn = DB()
        results = db_conn.select_db(sell_ID)

        if not results:
            client_sock.send_data(REQUEST_ERROR)
            return

        host_ID = results['host_ID']
        results_host = db_conn.select_db(host_ID)

        # 不存在这信息或者你就是发布它的主人
        if not results_host or host_ID == user_ID:
            client_sock.send_data(DELIMITER.join([USER_RESULT_STARSELL, '2']))
            return
        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        # 看对方是否在线，在线就直接发给他
        host_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == host_ID:
                host_sock = sock
                break

        if not host_sock:
            results_host['message'] += DELIMITER_3.join([USER_MESSAGE_RESELL, sell_ID, user_ID, time_now]) + DELIMITER_2
            print('对方不在线，留言成功！')
            client_sock.send_data(DELIMITER.join([USER_MESSAGE_RESELL, '1']))
            db_conn.update_db('message', results_host['message'], host_ID)
            db_conn.commit()
            db_conn.close()
            return

        message = DELIMITER.join([USER_MESSAGE_RESELL, sell_ID, user_ID, time_now])
        host_sock.send_data(message)
        print('对方在线，信息发送成功！')


    def request_closeOnline_handle(self, client_sock, user_ID, request_data):
        '''用户远程关锁'''

        bike_ID = request_data['bike_ID']

        bike_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == bike_ID:
                bike_sock = sock
                break

        if not bike_sock:
            print('关锁失败！')
            client_sock.send_data(DELIMITER.join([USER_RESULT_CLOSEONLINE, '2']))
            return

        bike_sock.send_data(DELIMITER.join([BIKE_CLOSEONLINE, user_ID]))
        print('用户远程关锁函数执行完毕')


    def result_closedOnline_handle(self, client_sock, bike_ID, request_data):
        '''车辆回应云端关锁指令'''

        reply_num = request_data['reply_num']
        user_ID = request_data['close_user_ID']

        db_conn = DB()
        if reply_num == '1':
            print('关锁成功')
            db_conn.update_db('status', STATUS[1], bike_ID)
            db_conn.update_db('status', STATUS[1], user_ID)

        user_sock = None
        for online_id, sock in self.online_clients.items():
            if online_id == user_ID:
                user_sock = sock
                break

        if user_sock:
            if reply_num == '3':
                print('开锁的人不是你！')
                user_sock.send_data(DELIMITER.join([USER_RESULT_CLOSEONLINE, '3']))
            if reply_num == '2':
                print('关锁失败！')
                user_sock.send_data(DELIMITER.join([USER_RESULT_CLOSEONLINE, '2']))
        else:
            print('关锁成功！')
            db_conn.update_db('status', STATUS[3], user_ID)
            user_sock.send_data(DELIMITER.join([USER_RESULT_CLOSEONLINE, '1']))

        db_conn.commit()
        db_conn.close()


    def request_pushInfo_handle(self, client_sock, bike_ID, request_data):
        '''车辆向云端发送自己的数据'''

        status = request_data['status']
        power = request_data['power']
        # lsat_ID = request_data['lsat_ID'] #最近一次骑它的人

        db_conn = DB()
        db_conn.update_db('status', status, bike_ID)
        db_conn.update_db('power', power, bike_ID)
        db_conn.commit()
        db_conn.close()
        print('车辆向云端发送自己的数据函数执行完毕')


    def request_bikeStolen_handle(self, client_sock, bike_ID, request_data):
        '''车被偷警告'''

        db_conn = DB()
        results = db_conn.select_db(bike_ID)
        host_ID = results['host']

        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        # 看主人是否客户端在线,向他发送消息
        for online_id, sock in self.online_clients.items():
            if online_id == host_ID:
                sock.send_data(DELIMITER.join([USER_MESSAGE_ALARM, bike_ID, time_now]))
                return

        # 主人不在线，向他留言
        results_host = db_conn.select_db(host_ID)
        results_host['message'] += DELIMITER_3.join([USER_MESSAGE_ALARM, bike_ID, time_now]) + DELIMITER_2
        db_conn.update_db('message', results_host['message'], host_ID)
        db_conn.commit()
        db_conn.close()
        print('车被偷警告函数执行完毕')


    def request_Speeding_handle(self, client_sock, bike_ID, request_data):
        '''车辆超速警告'''

        user_ID = request_data['user_ID']
        speed = request_data['speed']
        gps = request_data['gps']

        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

        # 看使用者是否客户端在线,向他发送消息
        for online_id, sock in self.online_clients.items():
            if online_id == user_ID:
                sock.send_data(DELIMITER.join([USER_MESSAGE_SPEEDING, bike_ID, time_now, gps, speed]))
                return

        # 使用者不在线，向他留言
        db_conn = DB()
        results_user = db_conn.select_db(user_ID)
        results_user['message'] += DELIMITER_3.join(
            [USER_MESSAGE_SPEEDING, bike_ID, time_now, gps, speed]) + DELIMITER_2
        db_conn.update_db('message', results_user['message'], user_ID)
        db_conn.commit()
        db_conn.close()
        print('车超速警告函数执行完毕')


    def result_pushGPS_handle(self, client_sock, bike_ID, request_data):
        '''处理车辆发过来的GPS信息'''

        gps = request_data['gps']

        # 看看是否超出地理围栏外
        # 这段之后再写

        db_conn = DB()
        db_conn.update_db('gps', gps, bike_ID)
        db_conn.commit()
        db_conn.close()
        print('处理车辆发过来的GPS信息函数执行完毕')


if __name__ == "__main__":
    server = Server()
    server.startup()
