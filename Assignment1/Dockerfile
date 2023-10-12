FROM ubuntu

# Create a directory in the container to hold the files
WORKDIR /compnets

# Copy server.py and client.py from the local directory to the container
COPY Subscriber.py Broker.py Producer.py /compnets/

RUN apt-get update && \
    apt-get install -y net-tools netcat tcpdump inetutils-ping python3

CMD ["/bin/bash"]