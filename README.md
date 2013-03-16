homework
========

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
        ##server salt-minion 127.0.0.1:8000 maxconn 32
