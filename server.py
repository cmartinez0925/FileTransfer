import argparse
import os
import socket

import server_utils

utils = server_utils.Server_Utils()

# Create the terminal command arguments for the script
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addr", action='store', dest="address", type=str, default="127.0.0.1",
                    help="Address of server")
parser.add_argument('-p', '--port', action='store', dest='port', type=int, default=33490, 
                    help="Port number to be used, use --help for more info")
args = parser.parse_args()

ADDR = args.address
PORT = args.port
socket_info = (ADDR, PORT)

# Create socket for server to listen on
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket_info)

try:
    s.listen()
    print(f"Listening on {ADDR} : {PORT}")

    while True:
        # Accept incoming connections to the server
        new_socket, new_addr = s.accept()
        print("\nNew incoming traffic")
        print(f"Connection from {new_addr}")

        # Receive the request from the client and parse content length
        client_request, content_length = utils.get_clientRequest_contentLength(new_socket)

        # Find the end of the header for the request and parse the request
        request_method, full_path, protocol = utils.get_request_line(client_request)

        # Remove entire path and get extension
        file_path = full_path.split('/')[-1]
        file_name, file_extension = os.path.splitext(file_path)
        
        # Open file and get length, file data to send to client
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            file_length = len(file_data)
            http_response = utils.generate_200_response(file_length, file_extension)
            new_socket.sendall(http_response)
            new_socket.sendall(file_data) # Sends binary data of requested file
        except FileNotFoundError:
            # Send 404 error to client when file can't be open or sent
            http_response = utils.generate_404_response()
            new_socket.sendall(http_response)
        finally:
            print(f"Closing connection on {new_addr}\n")
            new_socket.close()
except KeyboardInterrupt:
    print("\nServer is shutting down.")
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
    print("Socket is closed.")


