# Blackboard

## Interface

#### Constructor
`Blackboard(addr=MCAST_GRP, port=MCAST_PORT, read_size=READ_SIZE, TTL=MULTICAST_TTL)`

- `addr`: This is the network address to connect to. It must be an unreserved, available network block that supports the Multicasting protocol. It will default to `244.1.1.1`.
- `port`: This is the port on the network address the Blackboard will connect to. It will default to `5007`.
- `read_size`: This will specify the standard read size when getting data from the network address. It will default to `256` bytes.
- `TTL`: This is the number of times the signal will propagate through the network before being cut off. It will default to `32`.

#### Methods
- `write_json(channel, data)`: This will write the specified data to the specified channel. The channel can be any arbitrary string.
- `get(channel)`: This will return the most recent piece of data received on a specified channel.
- `register_callback(channel, f)`: This will add a callback function that will be called when a specific channel gets data. The callback must be a function that gets a single argument of the data from the channel.
- `is_open()`: This function will return `True` if the Blackboard is connected to the network, and `False` otherwise.
