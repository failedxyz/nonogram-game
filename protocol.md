Client-to-Server Packets:

 - 001 (connect): Sent from the client when it connects. Server assigns it a unique client ID, and adds the client to some list. The user does not need to be signed in at this point.
 - 002 (request channel info): Request channel info.
 - 003 (create/join channel): User joins a channel. Create this channel if doesn't exist.

Server-to-Client Packets:

 - 001 (connect-response): Response to client's connect packet
 - 002 (available channel info): Info about current rooms, channels, etc.