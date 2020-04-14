import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):

    # set an address for our destination server
    server_address = ('localhost', 10000)

    # log that we are creating a connection
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # create a client socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # connect to server
    sock.connect(server_address)

    # variable to hold received message as string
    received_message = ''

    try:

        # log command line message sent to server
        print('sending "{0}"'.format(msg), file=log_buffer)

        # send message to server
        sock.sendall(msg.encode('utf-8'))

        # variable to hold chunks of the received byte stream
        chunk = ''

        # loop to get chunks of stream from server
        while True:

            # get partial bytes from stream
            chunk = sock.recv(16)

            # decode and to cumulative string variable
            received_message += chunk.decode('utf8')

            # log received chunk
            print('received chunk: "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            # check for end of stream
            if len(chunk) < 16:
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # log entire message
        print(f'Entire message received (all chunks): {received_message}')

        # log and close socket
        print('closing socket', file=log_buffer)
        sock.close()

        # for testing
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
