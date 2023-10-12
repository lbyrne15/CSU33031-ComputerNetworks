import socket

localIP = "broker"
localPort = 50000
bufferSize = 1024

# Create a datagram socket
UDPBrokerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and IP
UDPBrokerSocket.bind((localIP, localPort))

print("UDP broker up and listening")

# Dictionary to store subscribers (subscriber IP -> subscriber port)
subscribers = {}
activeBroker = True
# Listen for incoming datagrams
while activeBroker == True:
    bytesAddressPair = UDPBrokerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # Check the content of the message to determine its source
    if message.startswith(b"Sub"):
        # Message from a subscriber requesting to subscribe
        subscriber_address, subscriber_port = address
        subscribers[subscriber_address] = subscriber_port
        print(f"Subscriber {subscriber_address}:{subscriber_port} has subscribed")
    else:
        # Message from a producer
        producerMsg = message[len(b"FromProducer:"):]
        print(f"Message from Producer: {producerMsg.decode('utf-8')}")
        
        # Forward the message to all subscribers
        for subscriber_address, subscriber_port in subscribers.items():
            UDPBrokerSocket.sendto(message, (subscriber_address, subscriber_port))

# Close the socket (this part may not be reached in an infinite loop)
UDPBrokerSocket.close()
