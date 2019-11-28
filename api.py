from flask import Flask
from flask import request

from IPython import embed

def parse_codes(query_string):
    codes = {}
    query = query_string.split("&")
    for x in query:
        params = x.split("=")
        codes[params[0]] = params[1]

    return codes

def update_config(codes):
    import toml
    config = toml.load("config.toml")
    config['codes'] = codes
    with open("config.toml", 'w') as f:
        f.write(toml.dumps(config))

app = Flask(__name__)
query_string = None

@app.route("/app/callback")
def hello():
    query_string = request.__dict__['environ']['QUERY_STRING']
    print(query_string)
    if query_string:
        codes = parse_codes(query_string)
        update_config(codes)
        return "thank you"
    else:
        return "no query string passed, thanks!"

if __name__ == "__main__":
    app.run()

# {'environ':
#   {'wsgi.version': (1, 0),
#     'wsgi.url_scheme': 'http',
#     'wsgi.input': <_io.BufferedReader name=5>,
#     'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>,
#     'wsgi.multithread': True,
#     'wsgi.multiprocess': False,
#     'wsgi.run_once': False,
#     'werkzeug.server.shutdown': <function WSGIRequestHandler.make_environ.<locals>.shutdown_server at 0x7fcf0dea4f28>,
#     'SERVER_SOFTWARE': 'Werkzeug/0.16.0',
#     'REQUEST_METHOD': 'GET',
#     'SCRIPT_NAME': '',
#     'PATH_INFO': '/',
#     'QUERY_STRING': '',
#     'REQUEST_URI': '/',
#     'RAW_URI': '/',
#     'REMOTE_ADDR': '127.0.0.1',
#     'REMOTE_PORT': 45752,
#     'SERVER_NAME': '127.0.0.1',
#     'SERVER_PORT': '5000',
#     'SERVER_PROTOCOL': 'HTTP/1.1',
#     'HTTP_HOST': '127.0.0.1:5000',
#     'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
#     'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5',
#     'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
#     'HTTP_CONNECTION': 'keep-alive',
#     'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
#     'werkzeug.request': <Request 'http://127.0.0.1:5000/' [GET]>
#   },
#   'shallow': False,
#   'url_rule': <Rule '/' (HEAD, OPTIONS, GET) -> hello>,
#   'view_args': {},
#   'url': 'http://127.0.0.1:5000/'
# }
