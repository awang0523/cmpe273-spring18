# Install grpc tools

```sh
pip install grpcio-tools
```

# Compile the proto file

```sh
python3 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. drone.proto 
```

# Run
To start the server with a x-axis distance between each drone:

> python3 server.py {start_cooridnate} {peer_distance}

```sh
python3 server.py 0,0,0 10,0,0
```

When a drone joins to the server, the server will response an unique client/drone id and a coordinate to be moved.

> python3 client.py {server_port}

```sh
python3 client.py 3000 
```
Client log:

__First Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [0, 0, 0]
```

__Second Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [10, 0, 0]
```
