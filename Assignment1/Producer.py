import socket
import struct
import os

def create_packet(producerCode, frameData):
    # Define the binary header structure
    headerFormat = "!3sB"  # 3 bytes for producer code, 1 byte for stream number
    header = struct.pack(headerFormat, producerCode.encode(), 1)  # Stream number is set to 1
    
    # Create the packet with the binary header and the frame data
    packet = header + frameData
    
    return packet

framesFolder = '/compnets/FrameSamples/'

brokerAddressPort = ("broker", 50009)
bufferSize = 1024

UDPProdSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

getCode = True

while True:
    producerCode = input("Enter Producer Code (3 characters) or type 'exit' to quit: ")
    
    # Check if the user wants to exit
    if producerCode.lower() == 'exit':
        break
    
    # Check if the input is valid
    if len(producerCode) != 3:
        print("Producer Code must be 3 characters long.")
        continue  # Continue the loop to re-prompt for input

    newProducerMessage = f"NewProd {producerCode} has been initialized"
    print(newProducerMessage)
    UDPProdSocket.sendto(str.encode(newProducerMessage), brokerAddressPort)

    while True:
        frameFilename = input("Enter frame filename (e.g., frame001.png) or type 'exit' to quit: ")
        
        if frameFilename.lower() == 'exit':
            getCode = False
            break

        framePath = os.path.join(framesFolder, frameFilename)
        
        if not os.path.isfile(framePath):
            print(f"Frame file '{frameFilename}' not found.")
            continue

        with open(framePath, 'rb') as frameFile:
            frameData = frameFile.read()

        packet = create_packet(producerCode, frameData)

        # Send the binary packet to the broker
        UDPProdSocket.sendto(packet, brokerAddressPort)

# Close the socket
UDPProdSocket.close()
