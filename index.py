import tornado.ioloop
import tornado.web
import torndb as database
import json
import fingerprint as f

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class UserRegister(tornado.web.RequestHandler):
    def get(self):
        phone = self.get_argument('phone', None)
        name = self.get_argument('name', None)
        stamp = self.get_argument('stamp')
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        response = f.compare_n()
        if phone != None and name != None:
            user = db.query("select uid from user where name=%s and phone=%s", name, phone)
            if response == 'ACK_NOUSER' and len(user) == 0:
                db.execute("insert into user (name, phone, stamp) values (%s, %s, %s)", name, phone, int(stamp))
                user = db.query("select * from user where name=%s and phone=%s", name, phone)
                if f.add(user['uid']) == 'ACK_SUCCESS':
                    result = dict()
                    for item in user[0]:
                        result[item] = user[0][item]
                    result['type'] = ['register']
                    return json.dumps(result)
        else:
            if type(response) is int:
                user = db.query("select * from user where uid=%s", response)
                result = dict()
                for item in user[0]:
                    result[item] = user[0][item]
                result['type'] = ['login']
                return json.dumps(result)
        return 'fail'

class UserDelete(tornado.web.RequestHandler):
    def get(self):
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        response = f.compare_n()
        if type(response) is int:
            uid = response
            response = f.delete_user(uid)
            if response == 'ACK_SUCCESS':
                db.execute("delete from user where uid=%s", uid)
                return 'success'
        return 'fail'

class UseStamp(tornado.web.RequestHandler):
    def get(self):
        try:
            db = database.Connection("localhost", "fingerprint", user="root", password="1")
            uid = self.get_argument('uid', None)
            number = self.get_argument('number', None)
            user = db.query("select * from user where uid=%s", uid)
            stamp = user[0]['stamp']+int(number)
            db.execute("update user set stamp=%s where uid = %s", stamp, int(uid))
            return 'success'
        except:
            return 'fail'

class ModifyStamp(tornado.web.RequestHandler):
    def get(self):
        try:
            db = database.Connection("localhost", "fingerprint", user="root", password="1")
            uid = self.get_argument('uid', None)
            add = self.get_argument('add', None)
            sub = self.get_argument('sub', None)
            user = db.query("select * from user where uid=%s", uid)
            if add != None:
                stamp = user[0]['stamp']+int(number)
                db.execute("update user set stamp=%s where uid = %s", stamp, int(uid))
            elif sub != None:
                stamp = user[0]['stamp']-int(number)
                db.execute("update user set stamp=%s where uid = %s", stamp, int(uid))
            else:
                return 'fail'
            return str(stamp)
        except:
            return 'fail'

application = tornado.web.Application([
    (r"/", MainnHandler),
    (r"/userRegister", UserRegister),
    (r"/userDelete", UserDelete),
    (r"/useStamp", UseStamp),
    (r"/modifyStamp", ModifyStamp),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
