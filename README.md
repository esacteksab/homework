homework
========


Checks for HTTP 503.  If HTTP 503 exists for > 30 seconds, it runs 

    salt-call file.comment /tmp/haproxy.conf server\ $HOSTNAME\ 

and then runs

    salt-call service.reload haproxy
    
What the above does is comments out the hostname behind haproxy and reloads (not restarts) haproxy to ensure that $HOSTNAME
is no longer behind HAProxy. 

running webserver.py:

    Serving http://127.0.0.1:8000/
    localhost - - [16/Mar/2013 15:31:56] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:31:56] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:31:58] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:31:58] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:00] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:00] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:02] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:02] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:04] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:04] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:06] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:06] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:08] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:08] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:10] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:10] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:12] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:12] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:14] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:14] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:16] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:16] "GET / HTTP/1.1" 503 -
    localhost - - [16/Mar/2013 15:32:18] code 503, message Service Unavailable
    localhost - - [16/Mar/2013 15:32:18] "GET / HTTP/1.1" 503 -


running check-status.py:

    root@salt-minion:~# python check-status 
    503
    503
    503
    503
    503
    503
    503
    503
    503
    503
    503
    [INFO    ] Loaded configuration file: /etc/salt/minion
    [WARNING ] Package debconf-utils is not installed.
    [INFO    ] Executing command "sed -i.bak -r -e 's/(server\\ salt-minion\\ )/#\\1/g' /tmp/haproxy.conf" in directory '/root'
    local:
        
    [INFO    ] Loaded configuration file: /etc/salt/minion
    [WARNING ] Package debconf-utils is not installed.
    [INFO    ] Executing command 'service haproxy reload' in directory '/root'
    local:
        True
    Now you fix it!


before:

    root@salt-minion:~# cat /tmp/haproxy.conf
    # Simpl configuration for an HTTP proxy listening on port 80 on all
    # interfaces and forwarding requests to a single backend "servers" with a
    # single server "server1" listening on 127.0.0.1:8000
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    frontend http-in
        bind *:80
        default_backend servers

    backend servers
        server salt-minion 127.0.0.1:8000 maxconn 32


after:

    root@salt-minion:~# cat /tmp/haproxy.conf
    # Simpl configuration for an HTTP proxy listening on port 80 on all
    # interfaces and forwarding requests to a single backend "servers" with a
    # single server "server1" listening on 127.0.0.1:8000
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    frontend http-in
        bind *:80
        default_backend servers

    backend servers
        #server salt-minion 127.0.0.1:8000 maxconn 32
        
        
watcher.py would likely be managed by supervisord (or uWSGI) for process management. 

It uses pyinotify https://github.com/seb-m/pyinotify

it checks on 

    IN_CLOSE_WRITE
    Writtable file was closed. 
    
http://seb-m.github.com/pyinotify/pyinotify.EventsCodes-class.html
    
My belief, rather than IN_CREATE, this ensures the file is done writing (not locked). 
Based on the file that we're using/managing, you can do whatever you want (based on where it is ran). 
Like `check-status.py` above, you could do a subprocess.call on a salt or salt-call (maybe even agaist Salt-API)

running watcher.py

    (venv)➜  foo  python loop2.py
    Wrote: /tmp/foo3
    you touched my file! I'm going to Salt you!
    Wrote: /tmp/foo-new



touching a file (this is comparable to uploading a file). Moving this to .backup or .tar'ing this for backup (prior to
deployment would not cause `pyinotify` to flag this and initiate anything. 

    ➜  foo  touch /tmp/foo3
    

Deploying & Restoring
---------------------

I feel I don't know enough about the environment. I could tar a directory like so:

    def backup_web():
        """ Backup a specified directory/project """
        tar = tarfile.open("/tmp/%s-%s-web-bkup.tar.bz2" % (date, project), "w:bz2")
        tar.add("/usr/share/nginx/%s" % (project))
        tar.close()
        
    def backup_db():
        """ backup a specified database """
        local("su postgres -c '/usr/bin/pg_dump -Fc %sdb > /opt/pg/bkup/%sdb-%s.dump'" % (project, project, date))


Then on failure, rm -rf /usr/share/nginx/$PROJECT, DROP DB, then extract previously made tar in it's place 
and `pg_restore` the `pg_dump`. 

If the deployment was in a `.deb` or `.rpm` you could leveage Salt and remove newest package and reinstall the old pkg
version. If you're just dropping a `.war` file, drop the old `.war` file. 



