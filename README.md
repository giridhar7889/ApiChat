APICHAT protocol - Client-server-client

Most HTTP-based client-server-client chat protocols work like this:

A client requests for the server to find a chat partner;
The server waits until it gets a request from another client;
The server relays messages between between the two, until either one of the clients disconnects.

How does the server do its job as a middleman?
Once two clients are connected to one another, they can start exchanging messages. To interact with their partner, a client simply sends a request to the server, including the action they want to perform and their ID. The server remembers the partner the ID is tied to, and is able to effectively be a middleman:
