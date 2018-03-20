import sys
from concurrent import futures
import grpc
import threading

import drone_pb2
import drone_pb2_grpc

start_cooridnate = []
peer_distance = []
coordinates = []
threads = []

def numUsers():
    return len(coordinates)


class Directioner(drone_pb2_grpc.DirectionerServicer):
    def Register(self, request, context):
        userId = numUsers()
        if (userId == 0):
            coordinates.append(start_cooridnate)
        elif (userId == 1):
            x = coordinates[0][0] + peer_distance[0]
            y = coordinates[0][1] + peer_distance[1]
            z = coordinates[0][2] + peer_distance[2]
            coordinates.append([x, y, z])
        else:
            # already 2 drones
            return drone_pb2.IdResp(uid = -1)

        threads.append(threading.Condition())
        resp = drone_pb2.IdResp(uid = userId)
        return resp

    def GetCoordinate(self, request, context):
        userId = request.uid
        resp = drone_pb2.CoordinateResp(x=0, y=0, z=0)
        threads[userId].acquire()
        while True:
            resp.x = coordinates[userId][0]
            resp.y = coordinates[userId][1]
            resp.z = coordinates[userId][2]
            yield resp
            threads[userId].wait()
        threads[userId].release()


def coordinateParser(str):
    str = str.replace('[', '')
    str = str.replace(']', '')
    coordinates = str.split(',')
    if (len(coordinates) != 3):
        print ('Invalid coordinates! Set to default: [0, 0 ,0]')
        return [0,0,0]
    else:
        return [int(coordinates[0]), int(coordinates[1]), int(coordinates[2])]


def move(array):
    coordinates[0] = array

    for i in range(len(coordinates)):
        threads[i].acquire()
        if i == 1:
            coordinates[1][0] = array[0] + peer_distance[0]
            coordinates[1][1] = array[1] + peer_distance[1]
            coordinates[1][2] = array[2] + peer_distance[2]
        threads[i].notify()
        threads[i].release()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_DirectionerServicer_to_server(
        Directioner(), server)
    server.add_insecure_port('[::]:3000')
    server.start()
    print ('Server started at 3000')

    try:
        while True:
            line = input('Enter New Cooridnate[x, y, z]>')
            move(coordinateParser(line))
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    start_cooridnate = coordinateParser(sys.argv[1])
    peer_distance = coordinateParser(sys.argv[2])
    serve()
