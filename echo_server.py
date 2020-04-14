import socket
import sys
import traceback


def server(log_buffer=sys.stderr):

    # set an address for our server
    address = ('127.0.0.1', 10000)

    print("Making a server on {0}:{1}\n".format(*address), file=log_buffer)

    # create a server socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # bind the socket
    sock.bind(address)

    # tell the socket to listen, queue length = 1
    sock.listen(1)

    # outer loop creates new connection sockets
    try:
        while True:

            # log that server is listening and able to accept connections
            print('Waiting for next connection...', file=log_buffer)

            # create new incoming connection socket
            conn, addr = sock.accept()

            try:

                # log connetion socket information
                print('Connection - {0}:{1} active:'.format(*addr), file=log_buffer)

                # inner loop receives and sends partial stream chunks
                while True:

                    # pull partial bytes off stream
                    data = conn.recv(16)

                    print('  Received: "{0}"'.format(data.decode('utf8')))

                    # send partial bytes to client
                    conn.sendall(data)
                    print('  Sent: "{0}"'.format(data.decode('utf8')))

                    # check for end of stream
                    if len(data) < 16:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

            finally:

                # log finish processing connection socket stream
                conn.close()

                print("Echo complete. Client connection closed.\n", file=log_buffer)

    except KeyboardInterrupt as e:

        # close server socket
        sock.close()

        # log interrupt and quit
        print("\nKeyboard interrupt detected.")
        print("Quitting echo server.", file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
