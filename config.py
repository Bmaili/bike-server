# ----服务器相关配置----
SERVER_IP = ''  # 服务器IP地址
SERVER_PORT = 8  # 服务器端口

# ----数据协议相关配置----
USER_REQUEST_LOGIN = 'us001'  # 登录请求
USER_REQUEST_FLUSH = 'us002'  # 刷新请求
USER_REQUEST_THEBIKE = 'us003'  # 某辆车详情请求
USER_REQUEST_THEFRIEND = 'us004'  # 某个好友详情请求
USER_REQUEST_ADDFRIEND = 'us005'  # 添加好友请求
USER_REQUEST_SHAREBIKE = 'us006'  # 分享车辆使用权请求
USER_REQUEST_OPEN = 'us007'  # 开锁请求

USER_RESULT_OPEN = 'su001'  # 登陆结果响应
USER_RESULT_FLUSH = 'su002'  # 刷新响应
USER_RESULT_THEBIKE = 'su003'  # 某辆车详情结果响应
USER_RESULT_THEFRIEND = 'su004'  # 某辆车详情结果响应
USER_RESULT_ADDFRIEND = 'su005'  # 添加好友结果响应
USER_RESULT_SHAREBIKE = 'su006'  # 分享车辆使用权结果响应


USER_MESSAGE_ADDFRIEND = '01'

DELIMITER = '|'  # 自定义协议数据分隔符
DELIMITER_2 = ','  # 自定义协议数据分隔符2号
DELIMITER_3 = '&'

# ----数据库相关配置----
DB_HOST = ''  # 数据库连接地址
DB_USER = ''  # 数据库登录用户名
DB_PASS = ''  # 数据库登录密码
DB_PORT = 3  # 数据库端口
DB_NAME = ''  # 数据库名
