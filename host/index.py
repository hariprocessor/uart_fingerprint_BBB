import tornado.ioloop
import tornado.web
import torndb as database
import json
import requests
import sys


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class UserRegister(tornado.web.RequestHandler):
    def get(self):
        phone = self.get_argument('phone', None)
        name = self.get_argument('name', None)
        stamp = self.get_argument('stamp')
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        try:
            fp = open('uid.txt', 'r')
            print 'read'
            uid = fp.readline()
            print 'read'
            fp.close()
        except:
            uid = '1'
            fp.close()
        print '*'*30
        print uid
        f = requests.get("http://192.168.7.2:8888/userRegister?uid="+uid)
        # New register
        if f.text.encode('utf-8') == 'register':
            db.execute("insert into user (uid, name, phone, stamp) values (%s, %s, %s, %s)", uid, name, phone, int(stamp))
            user = db.query("select * from user where uid=%s", uid)
            result = dict()
            for item in user[0]:
                result[item] = user[0][item]
            result['type'] = ['register']
            self.write(json.dumps(result))
            fp2 = open('uid.txt', 'w')
            fp2.write(str(int(uid)+1))
            fp2.close()
            uuid = str(int(uid)+1)
            return
        # Old user
        else:
            uid = f.text.encode('utf-8')
            user = db.query("select * from user where uid=%s", uid)
            result = dict()
            for item in user[0]:
                result[item] = user[0][item]
            result['type'] = ['login']
            self.write(json.dumps(result))
            return

class UserDelete(tornado.web.RequestHandler):
    def get(self):
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        f = requests.get("http://192.168.7.2:8888/userDelete")
        if str.isdigit(f.text.encode('utf-8')):
            uid = int(f.text.encode('utf-8'))
            db.execute("delete from user where uid=%s", uid)
            self.write('success')
            return
        self.write('fail')
        return

class UserDeleteAll(tornado.web.RequestHandler):
    def get(self):
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        db.execute('delete from user')
        f = requests.get("http://192.168.7.2:8888/userDeleteAll")

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
            self.write(str(stamp))
            return
        except:
            self.write('fail')
            return

class Database(tornado.web.RequestHandler):
    def get(self):
        db = database.Connection("localhost", "fingerprint", user="root", password="1")
        data = db.execute("select * from user")
        result=list()
        for row in data:
            dic = dict()
            for r in row:
                dic[r] = row[r]
            result.append(dic)
        self.write(json.dumps(result))
        return
                
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/userRegister", UserRegister),
    (r"/userDelete", UserDelete),
    (r"/useStamp", UseStamp),
    (r"/modifyStamp", ModifyStamp),
    (r"/userDeleteAll", UserDeleteAll),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
