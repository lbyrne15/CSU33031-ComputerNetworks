import socket

# Define the broker address and port
brokerAddressPort = ("broker", 50009)
bufferSize = 1024

# Create a socket for managing subscriptions
UDPBrokerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind the broker to its address and port
UDPBrokerSocket.bind(brokerAddressPort)

# Dictionary to store subscribers (subscriber IP -> subscriber port)
subscribers = {}

# Dictionary to store producer information and subscribers
producers = {}

# Dictionary to store subscribers and their subscriptions
subscriberSubscriptions = {}  # {subscriber_address: [producer_code1, producer_code2, ...]}

# Dictionary to store producers and their subscribers
producerSubscriptions = {}  # {producer_code: [subscriber_address1, subscriber_address2, ...]}

print("Broker up and listening. Waiting for messages...")

while True:
    bytesAddressPair = UDPBrokerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    if message.startswith(b"NewSub"): # New subscriber
        # Message from a subscriber registering with the broker
        parts = message.split()
        subscriberNumber = parts[1].decode("utf-8")

        print(f"Subscriber {subscriberNumber} has registered")
    elif message.startswith(b"Sub"):
        # Message from a subscriber requesting to subscribe
        parts = message.split()
        subscriberNumber = parts[1].decode("utf-8")
        producerCode = parts[5].decode("utf-8")

        # Store the subscriber
        subscriberAddress, subscriberPort = address
        subscribers[subscriberAddress] = subscriberPort

        # Update subscriptions
        if subscriberAddress not in subscriberSubscriptions:
            subscriberSubscriptions[subscriberAddress] = []
        subscriberSubscriptions[subscriberAddress].append(producerCode)

        if producerCode not in producerSubscriptions:
            producerSubscriptions[producerCode] = []
        producerSubscriptions[producerCode].append(subscriberAddress)

        print(f"Subscriber {subscriberAddress}:{subscriberPort} has subscribed to producer {producerCode}")

    elif message.startswith(b"Unsub"):
        # Message from a subscriber requesting to unsubscribe
        parts = message.split()
        subscriberNumber = parts[1].decode("utf-8")
        producerCode = parts[3].decode("utf-8")

        # Remove the subscriber
        if address in subscribers:
            del subscribers[address]
        print(f"Subscriber {subscriberNumber} has unsubscribed from producer {producerCode}")

        # Remove the subscriber from the producer's subscribers
        if producerCode in producerSubscriptions and address in producerSubscriptions[producerCode]:
            producerSubscriptions[producerCode].remove(address)
    elif message.startswith(b"NewProd"):
        # Message from a producer registering with the broker
        parts = message.split()
        producerCode = parts[1].decode("utf-8")

        producers[producerCode] = address
        print(f"Producer {producerCode} has registered")
    else:
        # Message from a producer
        producerCode = message[:3].decode("utf-8")
        producerFrame = message[3:]
        print(f"Message from Producer {producerCode}: {producerFrame.hex()}")

        # Forward the message to subscribed subscribers.
        if producerCode in producerSubscriptions:
            for subscriberAddress in producerSubscriptions[producerCode]:
                if subscriberAddress in subscribers:
                    UDPBrokerSocket.sendto(message, (subscriberAddress, subscribers[subscriberAddress]))
                    print(f"Forwarded message to {subscriberAddress}")

# Close the socket (this part may not be reached in an infinite loop)
UDPBrokerSocket.close()
UDPSubSocket.close()