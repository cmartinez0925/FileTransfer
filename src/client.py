import argparse
import socket

def main():
    ENCODING_TYPE = "ISO-8859-1"
    TRANSFER_SIZE = 4096
    ZERO_DATA_REMAINING = 0

    # Create the command line arguments to be used
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--addr", action='store', dest="address", type=str, default="127.0.0.1",
                        help="Website to send request, defaults to localhost")
    parser.add_argument("-c", "--connection", action='store', dest="connection", type=str, default="close",
                        help="Desire connection type, defaults to close")
    parser.add_argument("-f", "--file", action='store', dest="file", type=str, default="",
                        help="File to be requested from server, defaults to blank string")
    parser.add_argument("-m", "--method", action='store', dest="method", type=str, default="GET",
                        help="Desire request method, defaults to GET")
    parser.add_argument("-p", "--port", action='store', dest="port", type=int, default=33490,
                        help="Port number to use, defaults to 33490")
    args = parser.parse_args()


    # Create tuple of addr info and HTTP Request
    addr = (args.address, args.port)
    http_request = f"{args.method} /{args.file} HTTP/1.1\r\n"
    http_request += f"Host: {args.address}\r\n"
    http_request += f"Connection: {args.connection}\r\n\r\n"

    # Create socket and send request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(http_request.encode(ENCODING_TYPE))

    # Loop to recieve all byte data from server. Once complete close socket and print data
    run = True
    msg = ""
    print("Waiting for data to be received...")
    while run:
        data = s.recv(TRANSFER_SIZE)
        msg += data.decode(ENCODING_TYPE)
        if len(data) == ZERO_DATA_REMAINING:
            run = False

    s.close()
    print(msg)

if __name__ == '__main__':
    main()