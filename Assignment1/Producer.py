import socket


activeProd = True
while activeProd == True:
    # Input the message to be sent to the broker
    msgFromProd = input("Enter the message to send to the broker: ")
    bytesToSend = str.encode(msgFromProd)

    brokerAddressPort = ("broker", 50000)
    bufferSize = 1024

    UDPProdSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send the message to the broker
    UDPProdSocket.sendto(bytesToSend, brokerAddressPort)

# Close the socket
UDPProdSocket.close()