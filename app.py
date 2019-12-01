from flask import (
    Flask,
    Blueprint,
    session,
    request,
    redirect,
    url_for,
)
from routes.index import bp_user as user_routes
from routes.topic import bp_topic as topic_routes
from routes.reply import bp_reply as reply_routes
import config

app = Flask(__name__)
app.secret_key = config.secret_key

app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')

if __name__ == '__main__':
    config = dict(
        debug=True,
        port=2000,
        host='127.0.0.1'
    )
    app.run(**config)


"""
1.切分页面
    1.1 用户相关信息页--用户登录与注册页,个人详细信息展示页
    1.2 topic列表页--将所有topic条目展示,有添加topic的按钮,展示topic详细信息
    1.3 回复信息--添加回复框,展示所有回复信息
2.组织数据
    2.1 User类
        数据--id,name,password,
        方法--对密码进行加密, 验证注册信息, 验证登录
    2.2 Topic类
        数据--id, title, content, user_id, views, ct, ut
        方法--计算浏览数, 显示所有回复
    2.3 Reply类
        数据--id, content, topic_id, ct, ut
        方法--添加reply
3.实现逻辑
    3.1 
"""