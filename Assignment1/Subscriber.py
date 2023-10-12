import socket

activeSub = True
while activeSub == True:
    # Input the message to be sent to the broker
    subbed = False
    while subbed == False:
        msgFromSub = input("Enter Sub to subscribe to producer: ")
        if msgFromSub == "Sub":
            print("Subscriber has subscribed to producer")
            subbed = True
        else: 
            print("Unknown message received")

    serverAddressPort = ("broker", 50000)
    bufferSize = 1024

    UDPSubSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send the custom message to the broker
    UDPSubSocket.sendto(str.encode(msgFromSub), serverAddressPort)

    # Receive a message from the broker
    msgFromBroker, _ = UDPSubSocket.recvfrom(bufferSize)

    print(f"Message from Broker: {msgFromBroker.decode('utf-8')}")

# Close the socket
UDPSubSocket.close()
