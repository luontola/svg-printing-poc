import http.server
import socketserver

from jinja2 import Environment, FileSystemLoader, select_autoescape

PORT = 8080
TEMPLATE_DIR = "templates"

# Create a Jinja2 environment for rendering templates
jinja2_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html'])
)


# Create a custom request handler to render HTML templates
class TemplateHandler(http.server.SimpleHTTPRequestHandler):
    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
        template = jinja2_env.get_template(template_name)
        return template.render(context)

    def do_GET(self):
        # Check if the request is for a static file (e.g., CSS, JS)
        if "." in self.path:
            super().do_GET()
        else:
            # Render the HTML template
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=UTF-8')
            self.end_headers()
            context = {
                'message': 'Hello from <u>Python</u>!',
            }
            html = self.render_template("index.html", context)
            self.wfile.write(html.encode('UTF-8'))


# Avoid "OSError: [Errno 48] Address already in use" when restarting the server
socketserver.TCPServer.allow_reuse_address = True

# Create and configure the server
with socketserver.TCPServer(("localhost", PORT), TemplateHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
