from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the "static" directory
    static_dir = os.path.join(script_dir, 'static')

    # Check if the "static" directory exists
    if not os.path.isdir(static_dir):
        print(f"Error: The 'static' directory was not found at '{static_dir}'.")
        return

    # Change the current working directory to the "static" directory
    os.chdir(static_dir)

    # Configure the server
    server_address = ('', 8000)
    handler = handler_class

    # Start the HTTP server
    httpd = server_class(server_address, handler)
    print(f"Starting web server on port 8000, serving files from '{static_dir}'...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()

if __name__ == '__main__':
    run()