import SocketServer
import datetime

class EchoRequestHandler(SocketServer.BaseRequestHandler ):
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('hi ' + str(self.client_address) + '\n')

    def handle(self):
        data = 'dummy'
        while data:
            data = self.request.recv(1024)
            t = datetime .datetime .now()
            s = '%s-%s-%s %s:%s:%s.%s' % (t.year,t.month,t.day, t.hour,t.minute,t.second,t.microsecond)
            self.request.send ("%s %s:" % (s,data))
            if data.strip() == 'bye':
                return

    def finish(self):
        print self.client_address, 'disconnected!'
        self.request.send('bye ' + str(self.client_address) + '\n')

#server host is a tuple ('host', port)
server = SocketServer.ThreadingTCPServer(('', 50008), EchoRequestHandler)
server.serve_forever()
