import tornado.ioloop
import tornado.web
import json
import fingerprint as f

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class UserRegister(tornado.web.RequestHandler):
    def get(self):
        uid = self.get_argument('uid', None)
        uid = uid.encode('utf-8')
        uid = int(uid)
        response = f.compare_n()
        print response
        if type(response) is int:
            print 'int'
            self.write(str(response))
            return
	else:
            print 'acknouser else'
            t = f.add(uid)
            print t
            if t == 'ACK_SUCCESS':
                print 'register'
                self.write('register')
                return
        self.write('fail')
        return

class UserDelete(tornado.web.RequestHandler):
    def get(self):
        response = f.compare_n()
        if type(response) is int:
            uid = response
            response = f.delete_user(uid)
            if response == 'ACK_SUCCESS':
                self.write(str(uid))
                return
        self.write('fail')
        return

class userDeleteAll(tornado.web.RequestHandler):
    def get(self):
        f.delete_all()

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/userRegister", UserRegister),
    (r"/userDelete", UserDelete),
    (r"/userDeleteAll", userDeleteAll)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
