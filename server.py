import base64
import http.server
import socketserver

from jinja2 import Environment, FileSystemLoader, select_autoescape

PORT = 8080
TEMPLATE_DIR = "."

# Create a Jinja2 environment for rendering templates
jinja2_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html'])
)


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
            with open('image.svg', 'r') as file:
                image_svg = file.read()
            with open('5cm.svg', 'r') as file:
                image_5cm_svg = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            context = {
                'inline_svg': image_svg.replace('<svg', '<svg id="inline"', 1),
                'base64_svg': base64.b64encode(image_svg.encode('utf-8')).decode('utf-8'),
                'inline_5cm_svg': image_5cm_svg,
            }
            html = self.render_template("template.html", context)
            self.wfile.write(html.encode('utf-8'))


# Avoid "OSError: [Errno 48] Address already in use" when restarting the server
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("localhost", PORT), TemplateHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
