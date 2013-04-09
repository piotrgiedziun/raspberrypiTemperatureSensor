import os
import glob
import time
import tornado.ioloop
import tornado.web

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")

class TempHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('{"tmp": "%f"}' % read_temp())

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/temp", TempHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),"static")}),
])

if __name__ == "__main__":
    application.listen(80, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

