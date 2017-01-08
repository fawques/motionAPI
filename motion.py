import cherrypy
import os
import signal
import os.path
from subprocess import call

class Motion(object):
    pid_file = '/tmp/motion.pid'

    @cherrypy.expose
    def index(self):
        index = "Motion is:"
        if self.is_running():
            index = index + "RUNNING"
        else:
            index = index + "STOPPED"
        index = index + "\nAvailable commands: start | stop"
        return index
    
    @cherrypy.expose
    def start(self):
        if self.is_running():
            return 'Motion already started'
        ret = call('motion')
        if ret:
            return 'OK'
        return 'ERROR'

    @cherrypy.expose
    def stop(self):
        if not self.is_running():
            return 'Motion not started'
        with open(self.pid_file, 'r') as f:
            pid = int(f.readline ())
        if pid:
            os.kill(pid, signal.SIGTERM)
            return 'OK'
        return 'ERROR'

    def is_running(self):
        return os.path.isfile(self.pid_file)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0','server.socket_port': 8000})
    cherrypy.quickstart(Motion(), '/')

