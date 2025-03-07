from http.server import HTTPServer, SimpleHTTPRequestHandler
from celery import Celery

import os
if os.name == 'nt':
    import multiprocessing.popen_spawn_win32

os.makedirs("celery", exist_ok=True)

celery = Celery('agent',
                broker='filesystem://',
                backend='db+sqlite:///celery/results.sqlite')

celery.conf.update(
    broker_transport_options={'data_folder_in': './celery', 'data_folder_out': './celery', 'data_folder_processed': './celery'},
    result_expires=3600)

celery.conf.task_track_started = True
celery.conf.task_ignore_result = False


class SimpleHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, uri=None, data_to_return=None, user=None, **kwargs):
        self.uri = uri
        self.user = user
        self.data_to_return = data_to_return
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path != self.uri:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(self.data_to_return.encode() if self.data_to_return else b"No data provided")

@celery.task(bind=True)
def create_http_server(self, port, uri, data_to_return, user):
    self.update_state(meta={"port": port, "uri": uri})
    def handler(*args, **kwargs):
        data_response = f"{data_to_return}\nRequested by: {user}"
        SimpleHandler(*args, uri=uri, data_to_return=data_response, **kwargs)

    HTTPServer(("0.0.0.0", int(port)), handler).serve_forever()
