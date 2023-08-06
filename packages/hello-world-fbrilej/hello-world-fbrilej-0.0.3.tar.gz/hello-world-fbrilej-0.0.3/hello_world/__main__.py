import os
import sys
from bottle import route, run, template, BottleException
import argparse

@route('/')
def index():
    return template(os.path.dirname(sys.modules[__name__].__file__) + '/data/index.html')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="the port to run the webserver on", default=80)
    args = parser.parse_args()

    try:
        run(host='0.0.0.0', port=args.port)
    except PermissionError:
        print(f"Error: Couldn't start webserver due to lack of permissions. Try the --port option to pick a higher port.")
