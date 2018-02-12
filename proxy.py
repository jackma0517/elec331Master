from socket import *
import sys
import string

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)

    #Create a server socket, bind it to a port and start listening
    # home 192.168.2.121

    serverIP = sys.argv[1]
    port = 8888
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind((serverIP, port))
    tcpSerSock.listen(5)
    # Fill in start.
    # Fill in end.

    while 1:
        # Strat receiving data from the client
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)
        message = tcpCliSock.recv(1024).decode()
        print(message)


        # Extract the filename from the given message
        print(message.split()[1])
        filename = message.split()[1].partition("/")[2]

        print("Filename:", filename)
        fileExist = "false"
        filetouse = "/" + filename
        print("Filetouse:", filetouse)

        
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.readlines()
            print('Cache file opened')
            fileExist = "true"
            print('Cache file opened')

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")

            #send the output data from file
            tcpCliSock.send(outputdata)

            print('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print("hostn: ", hostn)
                try:
                    # Connect to the socket to port 80
                    print('Connect to hostn')
                    c.connect((hostn, 80))

                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    print('Making temporary file')
                    fileobj = c.makefile('rb')
                    print('Writing to temporary file')
                    fileobj.write("GET " + "http://" + filename + "HTTP / 1.1\r\n")

                    # Read the response into buffer
                    print('Reading from buffer')
                    buffer = ""
                    resp = c.recv(4096).decode()

                    while resp:
                        buffer = buffer + resp
                        resp = c.recv(4096).decode()

                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket
                    # and the corresponding file in the cache
                    print('print buffer: ', buffer)
                    tmpFile = open("./" + filename, "wb")
                    tmpFile.write(buffer)
                    print('print buffer: ', buffer)
                    tcpCliSock.send(buffer)


                    # Fill in end.
                except:
                    print("Illegal request")
            else:
                # HTTP response message for file not found
                pass
                # Fill in start.
                # Fill in end.

    # Close the client and the server sockets
    tcpCliSock.close()
    tcpSerSock.close()