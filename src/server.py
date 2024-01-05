import argparse
import os
import socket

import server_utils

def main():
    utils = server_utils.ServerUtils()

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
            server_root = os.path.abspath('../content')
            file_name = os.path.split(full_path)[1]
            file_path = os.path.join(server_root, file_name)
            file_path = os.path.abspath(file_path)
            file_extension = os.path.splitext(file_path)[1]
            
            print(f"file_name: {file_name}, file_path: {file_path}, file_extension: {file_extension}")
            # Open file and get length, file data to send to client
            try:
                # Check if the file_path doesn't start with the server root as its directory
                if not file_path.startswith(server_root):
                    raise NotADirectoryError("Directory does not start at the server root.")
                               
                # Check if the path is a directory
                if os.path.isdir(file_path):
                    # List directory contents
                    html_content = utils.generate_directory_listing(file_path)
                    # Send the directory listing as an HTTP Response
                    http_response = utils.generate_200_response(len(html_content), '.html')
                    new_socket.sendall(http_response)
                    new_socket.sendall(html_content.encode(utils.encoding_type))
                else:
                    with open(file_path, 'rb') as file:
                        file_data = file.read()
                    file_length = len(file_data)
                    http_response = utils.generate_200_response(file_length, file_extension)
                    new_socket.sendall(http_response)
                    new_socket.sendall(file_data) # Sends binary data of requested file
            except FileNotFoundError:
                # Send 404 error to client when file can't be open or sent
                new_socket.sendall(utils.generate_404_response())
            except NotADirectoryError:
                new_socket.sendall(utils.generate_404_response())
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

if __name__ == '__main__':
    main()
