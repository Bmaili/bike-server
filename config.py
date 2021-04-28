# ----服务器相关配置----
SERVER_IP = ''  # 服务器IP地址
SERVER_PORT = 8  # 服务器端口

# ----数据协议相关配置----

# 具体数据协议网址
# https://www.processon.com/view/link/6067ffe3f346fb0aa9839aa3

USER_REQUEST_LOGIN = 'us001'  # 登录请求
USER_REQUEST_FLUSH = 'us002'  # 刷新请求
USER_REQUEST_THEBIKE = 'us003'  # 某辆车详情请求
USER_REQUEST_THEFRIEND = 'us004'  # 某个用户详情请求
USER_REQUEST_ADDFRIEND = 'us005'  # 添加好友请求
USER_REQUEST_SHAREBIKE = 'us006'  # 分享车辆使用权请求
USER_REQUEST_DELETEFRIEND = 'us007'  # 删除好友
USER_REQUEST_SHAREBACK = 'us008'  # 撤销好友的车辆使用权
USER_REQUEST_REPLYFRIEND = 'us009'  # 对他人好友请求的回应
USER_REQUEST_USERRENAMED = 'us010'  # 修改本人昵称
USER_REQUEST_BIKERENAMED = 'us011'  # 修改车辆昵称

USER_REQUEST_OPEN = ''  # 开锁请求

USER_RESULT_LOGIN = 'su001'  # 登陆结果响应
USER_RESULT_FLUSH = 'su002'  # 刷新响应
USER_RESULT_THEBIKE = 'su003'  # 某辆车详情结果响应
USER_RESULT_THEFRIEND = 'su004'  # 某个用户详情结果响应
USER_RESULT_ADDFRIEND = 'su005'  # 添加好友结果响应
USER_RESULT_SHAREBIKE = 'su006'  # 分享车辆使用权结果响应
USER_RESULT_DELETEFRIEND = 'su007'  # 删除好友结果响应
USER_RESULT_SHAREBACK = 'su008'  # 撤销使用权结果响应
USER_RESULT_USERRENAMED = 'su010'  # 修改本人昵称结果响应
USER_RESULT_BIKERENAMED = 'su011'  # 修改车辆昵称结果相应

USER_MESSAGE_ADDFRIEND = '01'

REQUEST_ERROR = 'xxx'
DELIMITER_0 = ''  # 正则表达式里用来删特定字符串
DELIMITER = '|'  # 自定义协议数据分隔符
DELIMITER_2 = ','  # 自定义协议数据分隔符2号
DELIMITER_3 = '&'

# ----数据库相关配置----
DB_HOST = ''  # 数据库连接地址
DB_USER = ''  # 数据库登录用户名
DB_PASS = ''  # 数据库登录密码
DB_PORT = 3  # 数据库端口
DB_NAME = ''  # 数据库名
