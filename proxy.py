from socket import *
import sys
import string


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)

    #Create a server socket, bind it to a port and start listening

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
        messageRaw = tcpCliSock.recv(1024)
        message = messageRaw.decode()
        print(message)


        # Extract the filename from the given message
        print(message.split()[1])
        filename = message.split()[1].partition("/")[2].replace("www.", "", 1)
        if (filename[-1] == '/'):
            filename = filename[:-1]

        print("Filename:", filename)
        fileExist = "false"
        filetouse = "/" + filename
        print("Filetouse:", filetouse)
        hostn = filename.replace("www.", "", 1).partition("/")[0]
        print("hostn: ", hostn)

        part = filename[len(hostn):]

        if(len(part)>0):
            if(part[-1] == '/'):
                part = part[:-1]
        else:
            part = "/"

        print("part: ", part)

        try:
            # Check wether the file exist in the cache
            print('Open file')
            f = open(filetouse[1:], "r")
            buffer = f.readline()
            print('Cache file opened')
            fileExist = "true"


            # ProxyServer finds a cache hit and generates a response message
            statusMessage = "HTTP/1.0 200 OK\r\n" + "Content-Type:text/html\r\n"
            tcpCliSock.send(statusMessage.encode())

            outputdata = ""
            #send the output data from file
            while buffer:
                outputdata = outputdata + buffer
                buffer = f.readline()

            print('Read from cache')
            print("Sending cache content:")
            print(outputdata)
            tcpCliSock.send(outputdata.encode())


        # Error handling for file not found in cache
        except IOError:
            print('Fail to read from cache')

            if fileExist == "false":
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                
                try:
                    # Connect to the socket to port 80
                    print('Connect to hostn')
                    c.connect((hostn, 80))

                    # Create a new message to send to new server
                    newMessage = "GET " + part + " HTTP/1.1\r\n" + "Host: " + hostn + "\r\n\r\n"
                    print("Sending message to host: ")
                    print(newMessage)
                    c.send(newMessage.encode())

                    # Read the response into buffer
                    print('Reading into buffer')
                    buffer = b''
                    recv = c.recv(8192)

                    while recv:

                        buffer = buffer + recv
                        recv = c.recv(8192)

                    print('Response saved, sending: \n', buffer.decode())
                    tcpCliSock.send(buffer)

                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket
                    # and the corresponding file in the cache

                    print("Creating cache file")
                    tmpFile = open("./" + filename, "wb")
                    print("Writing to cache")
                    tmpFile.write(buffer)
                    tmpFile.close()
                    print("Closing socket")
                    tcpCliSock.close()


                except:
                    print("Error: ", sys.exc_info()[0], sys.exc_info()[1])

            else:
                # HTTP response message for file not found
                pass


    # Close the server sockets
    tcpSerSock.close()

