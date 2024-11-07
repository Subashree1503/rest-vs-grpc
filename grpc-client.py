import grpc
import lab6_pb2
import lab6_pb2_grpc
import time
import sys
import base64

def do_add(stub, reps):
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.add(lab6_pb2.addMsg(a=5, b=10))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"Add method: Took {delta} ms per operation")

def do_rawimage(stub, reps):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.rawimage(lab6_pb2.rawImageMsg(img=img))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"RawImage method: Took {delta} ms per operation")

def do_dotproduct(stub, reps):
    a = [1.0, 2.0, 3.0]
    b = [4.0, 5.0, 6.0]
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.dotproduct(lab6_pb2.dotProductMsg(a=a, b=b))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"DotProduct method: Took {delta} ms per operation")

def do_jsonimage(stub, reps):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img_b64 = base64.b64encode(img).decode('utf-8')
    start = time.perf_counter()
    for _ in range(reps):
        response = stub.jsonimage(lab6_pb2.jsonImageMsg(img=img_b64))
    delta = ((time.perf_counter() - start) / reps) * 1000
    print(f"JsonImage method: Took {delta} ms per operation")

if __name__ == '__main__':
    server_address = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])
    
    with grpc.insecure_channel(f'{server_address}:50051') as channel:
        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

        if cmd == 'add':
            do_add(stub, reps)
        elif cmd == 'rawimage':
            do_rawimage(stub, reps)
        elif cmd == 'dotproduct':
            do_dotproduct(stub, reps)
        elif cmd == 'jsonimage':
            do_jsonimage(stub, reps)
        else:
            print("Unknown command")
