import os
import sys
from bottle import route, run, template
from bottledaemon import daemon_run

@route('/')
def index():
    return template(os.path.dirname(sys.modules[__name__].__file__) + '/data/index.html')

if __name__ == "__main__":
    run(host='0.0.0.0', port=80)
