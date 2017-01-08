import cherrypy
import os
import signal
import os.path
from subprocess import call

class Motion(object):
    pid_file = '/tmp/motion.pid'

    @cherrypy.expose
    def index(self):
        return "Available commands: start | stop"
    
    @cherrypy.expose
    def start(self):
        if os.path.isfile(self.pid_file):
            return 'Motion already started'
        ret = call('motion')
        if ret:
            return 'OK'
        return 'ERROR'

    @cherrypy.expose
    def stop(self):
        if not os.path.isfile(self.pid_file):
            return 'Motion not started'
        with open(self.pid_file, 'r') as f:
            pid = int(f.readline ())
        if pid:
            os.kill(pid, signal.SIGTERM)
            return 'OK'
        return 'ERROR'

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 8000})
    cherrypy.quickstart(Motion(), '/')

