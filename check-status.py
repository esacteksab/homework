import time
from subprocess import call
import socket
import urllib

start_time = time.time()
HOSTNAME = socket.gethostname()


def getStatus():
    while 1 == 1:

        elapsed_time = time.time() - start_time
        r = urllib.urlopen('http://localhost:8000')
        if int(elapsed_time) > 20 and r.getcode() == 503:
            call(['salt-call', 'file.comment', '/tmp/haproxy.conf',
                 'server\ {0}\ '.format(HOSTNAME)])
            call(['salt-call', 'service.reload', 'haproxy'])
            print "Now you fix it!"
            break
        # elif int(elapsed_time) < 30 and r.status_code == 503:
        #     print 'fail'
        #     print elapsed_time
        else:
            print r.getcode()
        time.sleep(2)


if __name__ == '__main__':
    getStatus()
