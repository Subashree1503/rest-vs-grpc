from concurrent import futures
import grpc
import lab6_pb2
import lab6_pb2_grpc
from PIL import Image
import io
import base64

class Lab6ServiceServicer(lab6_pb2_grpc.Lab6ServiceServicer):
    def add(self, request, context):
        result = request.a + request.b
        print(f"Received add request: a={request.a}, b={request.b}, sum={result}")
        return lab6_pb2.addReply(sum=result)

    def rawimage(self, request, context):
        try:
            img_data = io.BytesIO(request.img)
            img = Image.open(img_data)
            print(f"Received rawimage request: width={img.width}, height={img.height}")
            return lab6_pb2.imageReply(width=img.width, height=img.height)
        except Exception as e:
            print(f"Error processing rawimage: {e}")
            context.set_details(f"Error processing image: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return lab6_pb2.imageReply(width=0, height=0)

    def dotproduct(self, request, context):
        try:
            a = request.a
            b = request.b
            if len(a) != len(b):
                raise ValueError("Vectors must be the same length")
            dot_product = sum([x * y for x, y in zip(a, b)])
            print(f"Received dotproduct request: dot_product={dot_product}")
            return lab6_pb2.dotProductReply(dotproduct=dot_product)
        except Exception as e:
            print(f"Error in dotproduct: {e}")
            context.set_details(f"Error calculating dot product: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return lab6_pb2.dotProductReply(dotproduct=0.0)

    def jsonimage(self, request, context):
        try:
            img_data = base64.b64decode(request.img)  # Decode from base64
            img = Image.open(io.BytesIO(img_data))
            print(f"Received jsonimage request: width={img.width}, height={img.height}")
            return lab6_pb2.imageReply(width=img.width, height=img.height)
        except Exception as e:
            print(f"Error processing jsonimage: {e}")
            context.set_details(f"Error processing JSON image: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return lab6_pb2.imageReply(width=0, height=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6ServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
