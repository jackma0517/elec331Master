from socket import *

if __name__ == "__main__":
    msg = "\r\n Name: Jack Ma, Student Number: 29930147. ELEC331 is FUN! "
    endmsg = "\r\n.\r\n"
    # Choose a mail server (e.g. Google mail server) and call it mailserver
    gmailServer = 'smtp.gmail.com'
    eceServer = 'esva.mail-relay.ubc.ca'
    eceEmail = 'p3n0b@ece.ubc.ca'
    gmail = 'jackma0517@gmail.com'
    mailPort = 25
    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    mailServer = eceServer
    clientSocket.connect((mailServer, mailPort))

    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    print("HELO command")
    heloCommand = 'HELO Jack\r\n'
    clientSocket.send(heloCommand.encode())
    recv = clientSocket.recv(1024).decode()

    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    print("FROM command")
    if(mailServer == gmailServer):
        fromAddress = gmail
    else:
        fromAddress = eceEmail
    fromCommand = 'MAIL FROM:' + fromAddress + "\r\n"
    clientSocket.send(fromCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')

    # Send RCPT TO command and print server response.
    print("RCPT command")
    if (mailServer == gmailServer):
        rcptAddress = gmail
    else:
        rcptAddress = eceEmail
    rcptCommand = 'RCPT TO:' + rcptAddress + "\r\n"
    clientSocket.send(rcptCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')


    # Send DATA command and print server response.
    print("DATA command")
    dataCommand = "DATA\r\n"
    clientSocket.send(dataCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '354':
        print('354 reply not received from server.')

    # Send message data.
    # Message ends with a single period.
    print("Sending DATA")
    clientSocket.send(msg.encode())
    clientSocket.send(endmsg.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '250':
        print('250 reply not received from server.')


    # Send QUIT command and get server response.
    print("QUIT command")
    quitCommand = "QUIT\r\n"
    clientSocket.send(quitCommand.encode())
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '221':
        print('221 reply not received from server.')

    print("\n\nFinish, check the mailbox")