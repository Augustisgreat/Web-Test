import http.server
import socketserver
import urllib.parse

PORT = 8080

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse the query from the original request
            parsed_url = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed_url.query).get('q', [''])[0]

            # If the query exists, construct the Google search URL
            if query:
                search_url = f'https://www.google.com/search?q={query}'
            else:
                # If no query, use a default URL
                search_url = 'https://www.google.com'

            # Forward the search results to the browser
            self.send_response(302)
            self.send_header('Location', search_url)
            self.end_headers()

        except Exception as e:
            print(f"An error occurred in do_GET: {e}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Starting proxy server at http://localhost:{PORT}")
        httpd.serve_forever()
