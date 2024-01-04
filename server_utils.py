import os
import socket

class Server_Utils:
    # Properties
    DEFAULT = "default"
    END_OF_HEADER_LINE = "\r\n"
    END_OF_HEADER = "\r\n\r\n"
    FIRST_LINE = 0

    EXTENSIONS = {
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "default": "appliation/octet-stream",
    ".gif": "image/gif",
    ".html": "text/html",
    "jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".numbers": "application/vnd.apple.numbers",
    ".pages": "application/vnd.apple.pages",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    # Constructors
    def __init__(self, encoding_type='ISO-8859-1', transfer_size=4096):
        self.encoding_type = encoding_type
        if transfer_size <= 0:
            self.transfer_size = 512
        else:
            self.transfer_size = transfer_size

    # Methods
    def generate_200_response(self, file_length, file_extension):
        http_response = f"HTTP/1.1 200 OK\r\n"
        http_response += f"Content-Type: {self.EXTENSIONS.get(file_extension, self.EXTENSIONS[self.DEFAULT])}\r\n"
        http_response += f"Content-Length: {file_length}\r\n"
        http_response += f"Connection: close\r\n\r\n"
        return http_response.encode(self.encoding_type)

    def generate_404_response(self):
        http_response = f"HTTP/1.1 404 Not Found\r\n"
        http_response += f"Content-Type: text/plain\r\n"
        http_response += f"Content-Length: 13\r\n"
        http_response += f"Connection: close\r\n\r\n404 not found\r\n"
        return http_response.encode(self.encoding_type)

    def get_clientRequest_contentLength(self, new_socket):
        client_request = ""
        while True:
            data = new_socket.recv(self.transfer_size)
            client_request += data.decode(self.encoding_type)

            # Determine the end of header and break out of the loop
            header_end_index = client_request.find(self.END_OF_HEADER)
            if header_end_index != -1:
                header = client_request[:header_end_index]
                header_lines = header.split(self.END_OF_HEADER_LINE)

                # Check for the Content-Length
                content_length = 0
                for line in header_lines:
                    if line.lower().startswith('content-length'):
                        content_length = int(line.split(':')[1].strip())
                        break
                
                # Check if the entire request (header + content) has been received
                if len(client_request) >= header_end_index + len(self.END_OF_HEADER) + content_length:
                    break
        return (client_request, content_length)

    def get_request_line(self, client_request):
        header_end_index = client_request.find(self.END_OF_HEADER)
        if header_end_index != -1:
            header = client_request[:header_end_index]
            header_lines = header.split(self.END_OF_HEADER_LINE)
            header_first_line = header_lines[self.FIRST_LINE]
            return header_first_line.split()
    
    # Special Methods
    def __repr__(self):
        return f"Server_Utils(self, {self.encoding_type}, {self.send_recv_size})"
    
    def __str__(self):
        return f"Encoding Type: {self.encoding_type} Send/Recv Size: {self.send_recv_size}"

