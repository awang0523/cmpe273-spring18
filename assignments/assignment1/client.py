import sys

import grpc

import drone_pb2
import drone_pb2_grpc

def run():
    host = 'localhost:' + sys.argv[1]
    channel = grpc.insecure_channel(host)
    stub = drone_pb2_grpc.DirectionerStub(channel)
    resp = stub.Register(drone_pb2.IdReq())

    if resp.uid == -1:
        print('Already have 2 drones.')
    else:
        print('Client id [%d] connected to the server.' % resp.uid)
        coordinates = stub.GetCoordinate(drone_pb2.CoordinateReq(uid = resp.uid))
        for coordinate in coordinates:
            print('[received] moving to [%d, %d, %d]'
                  % (coordinate.x, coordinate.y, coordinate.z))

if __name__ == '__main__':
    run()

