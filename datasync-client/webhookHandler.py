import json
from http.server import BaseHTTPRequestHandler, HTTPServer

port = 80


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Exemplo de como lidar com uma requisição POST
        if self.path == "/webhook":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            post_data_dict = json.loads(post_data.decode("utf-8"))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(post_data_dict).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=port):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
