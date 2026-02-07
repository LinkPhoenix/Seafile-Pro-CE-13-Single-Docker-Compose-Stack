import os

daemon = True
workers = 5

bind = "127.0.0.1:8000"

pids_dir = '/opt/seafile/pids'
pidfile = os.path.join(pids_dir, 'seahub.pid')

timeout = 1200
limit_request_line = 8190
forwarder_headers = 'SCRIPT_NAME,PATH_INFO,REMOTE_USER'
