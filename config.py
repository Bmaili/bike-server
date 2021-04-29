# ----服务器相关配置----
SERVER_IP = ''  # 服务器IP地址，不填默认本地
SERVER_PORT = 8  # 服务器端口

# ----数据库相关配置----
DB_HOST = ''  # 数据库连接地址
DB_USER = ''  # 数据库登录用户名
DB_PASS = ''  # 数据库登录密码
DB_PORT = 3  # 数据库端口
DB_NAME = ''  # 数据库名

# ----数据协议相关配置----
# ----用户-云端数据协议----
# 具体数据协议网址https://www.processon.com/view/link/6067ffe3f346fb0aa9839aa3

# user -> server
USER_REQUEST_LOGIN = 'us001'  # 登录请求
USER_REQUEST_FLUSH = 'us002'  # 刷新请求
USER_REQUEST_THEBIKE = 'us003'  # 某辆车详情请求
USER_REQUEST_THEFRIEND = 'us004'  # 某个用户详情请求
USER_REQUEST_ADDFRIEND = 'us005'  # 添加好友请求
USER_REQUEST_SHAREBIKE = 'us006'  # 分享车辆使用权请求
USER_REQUEST_DELFRIEND = 'us007'  # 删除好友
USER_REQUEST_SHAREBACK = 'us008'  # 撤销好友的车辆使用权
USER_REQUEST_REPLYFRIEND = 'us009'  # 对他人好友请求的回应
USER_REQUEST_USERRENAMED = 'us010'  # 修改本人昵称
USER_REQUEST_BIKERENAMED = 'us011'  # 修改车辆昵称
USER_REQUEST_OPEN = 'us012'  # 开锁请求
USER_REQUEST_CHAT = 'us013'  # 聊天请求
USER_REQUEST_SELLBIKE = 'us014'  # 把车子挂到聊天室
USER_REQUEST_ONESELL = 'us015'  # 查看转卖墙上的具体的某一条信息
USER_REQUEST_MYSELL = 'us017'  # 查看我的转卖信息(大致的）
USER_REQUEST_DELSELL = 'us018'  # 删除某条转卖信息
USER_REQUEST_STARSELL = 'us019'  # 想买某辆转卖车辆
USER_REQUEST_CLOSEONLINE = 'us020'  # 远程关锁

# server -> user
USER_RESULT_LOGIN = 'su001'  # 登陆结果响应
USER_RESULT_FLUSH = 'su002'  # 刷新响应
USER_RESULT_THEBIKE = 'su003'  # 某辆车详情结果响应
USER_RESULT_THEFRIEND = 'su004'  # 某个用户详情结果响应
USER_RESULT_ADDFRIEND = 'su005'  # 添加好友结果响应
USER_RESULT_SHAREBIKE = 'su006'  # 分享车辆使用权结果响应
USER_RESULT_DELFRIEND = 'su007'  # 删除好友结果响应
USER_RESULT_SHAREBACK = 'su008'  # 撤销使用权结果响应
USER_RESULT_USERRENAMED = 'su010'  # 修改本人昵称结果响应
USER_RESULT_BIKERENAMED = 'su011'  # 修改车辆昵称结果相应
USER_RESULT_OPEN = 'su012'  # 向用户发送开锁回应
USER_RESULT_CHAT = 'su013'  # 聊天请求响应结果
USER_RESULT_SELLBIKE = 'su014'  # 把车子挂到聊天室响应结果
USER_RESULT_ONESELL = 'su015'  # 查看转卖墙上的具体的某一条信息响应结果
USER_PUSH_CLOSE = 'su016'  # 告诉用户关锁信息，无需回应所以上面没us016
USER_RESULT_MYSELL = 'su017'  # 查看我的转卖信息(大致的）响应结果
USER_RESULT_DELSELL = 'su018'  # 删除某条转卖信息响应结果
USER_RESULT_STARSELL = 'su019'  # 想买某辆转卖车辆响应结果
USER_RESULT_CLOSEONLINE = 'su020'  # 远程关锁结果回应

# ----server -> user   message类----
USER_MESSAGE_ADDFRIEND = 'ms001'  # 别人请求添加你为好友
USER_MESSAGE_CHAT = 'ms002'  # 好友给你发的信息
USER_MESSAGE_RESELL = 'ms003'  # 别人想买你挂在转卖墙上的车
USER_MESSAGE_OUTBOUNDS = 'ms004'  # 你某车跑出地理围栏外了！
USER_MESSAGE_ALARM = 'ms005'  # 你车发了警报（也许被偷了）
USER_MESSAGE_SPEEDING = 'ms006'  # 你车超速了

# ----车辆-云端数据协议----
# 具体数据网址https://www.processon.com/view/link/6066f1fce0b34d282990f9b0
# bike -> server
BIKE_REQUEST_LOGIN = 'bs001'  # 登录请求
BIKE_PUSH_INFO = 'bs002'  # 车辆向云端发送自己的数据
BIKE_RESULT_OPEN = 'bs003'  # 车辆回应开锁请求
BIKE_CLOSE = 'bs004'  # 车辆手动关闭
BIKE_OPENBYNFC = 'bs005'  # 因为NFC被开锁
BIKE_STOLEN = 'bs006'  # 车被偷了
BIKE_SPEEDING = 'bs007'  # 超速
BIKE_RESULT_CLOSE = 'bs008'  # 车辆回应云端关锁指令
BIKE_PUSH_GPS = 'bs009'  # 发送自己的GPS，可用于地理围栏检测

# server -> bike
BIKE_RESULT_LOGIN = 'sb001'  # 回应自行车登陆结果
BIKE_GET_INFO = 'sb002'  # 向自行车询问状态
BIKE_REQUEST_OPEN = 'sb003'  # 向车辆发送开锁请求
BIKE_CLOSEONLINE = 'sb008'  # 用户远程关锁
BIKE_GET_GPS = 'sb009'  # 获取车辆GPS，可用于地理围栏检测

# ---------其他---------
STATUS = ['0', '1', '2', '3']  # 用户或车的状态 ，1在线，2骑行\被骑，3离线，0没啥用
REQUEST_ERROR = 'xxx'  # 回应用户的非法请求
KONGBAI = ''  # 空白符，正则表达式里用来删特定字符串
DELIMITER = '|'  # 自定义协议数据分隔符，下面俩主要是数据库里存储数据时的不同分隔符
DELIMITER_2 = ','  # 自定义协议数据分隔符2号
DELIMITER_3 = '&'  # 自定义协议数据分隔符3号

# 正则表达式定义
# 用于匹配用户或车辆昵称：昵称只能有1至8位汉字、字母、数字、下划线'
REGULAR_NICKNAME = r'^[a-zA-Z0-9_\u4e00-\u9fa5]{1,8}$'

# 用于匹配转卖车辆信息的标题：标题只能有1至15位汉字、字母、数字、下划线'
REGULAR_TITLE = r'^[a-zA-Z0-9_\u4e00-\u9fa5]{1,15}$'

# 用于匹配转卖车辆信息的正文内容、与好友的聊天内容，
# 只能匹配1至150位汉字、字母、数字、下划线、还有部分中文标点  。 ； ， ： “ ”（ ） 、 ？ 《 》 这些符号
REGULAR_INFO = r'^[a-zA-Z0-9_\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]{1,150}$'
