from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from entries import get_all_entries, get_single_entry, delete_single_entry, search_entries, create_journal_entry, update_entry


class HandleRequests(BaseHTTPRequestHandler):

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # This method supports requests with the OPTIONS verb.
    # Where you would set up CORS
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        # Set the response code to 'Ok'
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/entries` or `/entries/2`
        if len(parsed) == 2:
            (resource, id) = parsed
            print(f"resource: {resource}\nid: {id}")

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "q" and resource == "entries":
                response = search_entries(value)

        self.wfile.write(response.encode())

    def do_DELETE(self):
        # 204 - Successfully processed request
        # but no information to send back
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        delete_single_object = {
            "entries": delete_single_entry
        }
        func = delete_single_object[resource]
        func(id)

        self.wfile.write("".encode())

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        print(f"path: {path}")
        print(f"path_params: {path_params}")
        print(f"resource: {resource}")
        # Check if there is a query string parameter
        if "?" in resource:
            # E.G.: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new object
        new_object = None

        # Add a new object to the list.
        create_obj = {
            "entries": create_journal_entry
        }

        func = create_obj[resource]
        new_object = func(post_body)

        # Encode the new object and send in response
        self.wfile.write(f"{new_object}".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))

        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        # rest of the elif's

        if success:
            # 204 - Successful request but no content to return.
            self._set_headers(204)
        else:
            # Something went wrong.
            self._set_headers(404)

        # Encode the new entry and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
