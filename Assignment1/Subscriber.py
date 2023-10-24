import socket
import threading

# Define the subscriber address and port
brokerAddressPort = ("broker", 50009)  # Make sure this is the correct broker address and port
bufferSize = 1024

# Create a socket for managing subscriptions
UDPSubSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Function to receive and print messages from the broker
def receive_messages():
    # Receive and print messages from the broker
    try:
        msgFromBroker, _ = UDPSubSocket.recvfrom(bufferSize)
        messageReceived = msgFromBroker[3:]
        print(f"\nMessage from Broker: {messageReceived}\n")
    except socket.error:
        pass  # Continue if no message is available

# Start the message receiving thread
message_receiver_thread = threading.Thread(target=receive_messages)
message_receiver_thread.start()

# Input the subscriber number
subscriberNumberAcquired = False
while not subscriberNumberAcquired:
    subscriberNumber = input("Enter Subscriber Number (3 digits) or type 'exit' to quit: ")

    if subscriberNumber.lower() == 'exit': 
        break

    if not subscriberNumber.isdigit() or len(subscriberNumber) != 3:
        print("Subscriber Number must be 3 digits long.")
        continue

    subscriptionMessage = f"NewSub {subscriberNumber} has been initialized"
    try:
        UDPSubSocket.sendto(subscriptionMessage.encode(), brokerAddressPort)
    except Exception as e:
        print(f"Error sending subscription message: {e}")
        break

    subscriberNumberAcquired = True
    activeSub = True

subscriptions = set()  # A set to store active subscriptions

while activeSub:
    command = input("Enter 'sub (ProducerID)', 'unsub (ProducerID)', or 'exit': ").lower()
    
    if command == 'exit':
        break

    if command.startswith('sub '):
        parts = command.split()
        if len(parts) == 2:
            producerID = parts[-1]

            if len(producerID) != 3:
                print("Producer ID must be 3 characters long.")
                continue

            if producerID in subscriptions:
                print(f"Already subscribed to {producerID}")
            else:
                subscriptions.add(producerID)
                print(f"Subscriber has subscribed to producer {producerID}")
                subscriptionMessage = f"Sub {subscriberNumber} has subscribed to {producerID}"
                try:
                    UDPSubSocket.sendto(subscriptionMessage.encode(), brokerAddressPort)
                except Exception as e:
                    print(f"Error sending subscription message: {e}")
        else:
            print("Invalid 'sub' command. Please use 'sub (ProducerID)'.")

    elif command.startswith('unsub '):
        parts = command.split()
        if len(parts) == 2:
            producerID = parts[-1]

            if producerID in subscriptions:
                subscriptions.remove(producerID)
                print(f"Subscriber has unsubscribed from producer {producerID}")
                unsubscriptionMessage = f"Unsub {subscriberNumber} from {producerID}"
                try:
                    UDPSubSocket.sendto(unsubscriptionMessage.encode(), brokerAddressPort)
                except Exception as e:
                    print(f"Error sending unsubscription message: {e}")
            else:
                print(f"You are not subscribed to producer {producerID}")
        else:
            print("Invalid 'unsub' command. Please use 'unsub (ProducerID)'.")

    elif command == 'ls subs':
        currentSubs = len(subscriptions)
        if currentSubs == 0:
            print("No active subscriptions.")
        elif currentSubs == 1:
            print("1 Current Subscription:")
            for producerID in subscriptions:
                print(f"- {producerID}")
        else:
            print(f"{currentSubs} Current Subscriptions:")
            for producerID in subscriptions:
                print(f"- {producerID}")
    else:
        print("Unknown command. Please use 'sub (ProducerID)', 'unsub (ProducerID)', or 'exit'.")

# Close the socket
UDPSubSocket.close()
