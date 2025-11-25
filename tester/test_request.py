#!/usr/bin/env python3
import stomp
import time
import sys
import os

def send_test_requests():
    host = os.getenv('ARTEMIS_HOST', 'artemis')
    port = int(os.getenv('ARTEMIS_PORT', '61616'))
    conn = stomp.Connection([(host, port)])

    try:
        conn.connect('admin', 'admin', wait=True)

        # Request 1: getUserInfo
        request1 = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <operation>getUserInfo</operation>
    <userId>12345</userId>
</request>"""

        conn.send(destination='/queue/request.queue',
                  body=request1,
                  headers={'content-type': 'application/xml'})
        print("Request 1 (getUserInfo) has been sent!")

        time.sleep(1)

        # Request 2: getBalance
        request2 = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <operation>getBalance</operation>
    <accountId>67890</accountId>
</request>"""

        conn.send(destination='/queue/request.queue',
                  body=request2,
                  headers={'content-type': 'application/xml'})
        print("Request 2 (getBalance) has been sent!")

        time.sleep(1)

        # Request 3: unknown (return default_error)
        request3 = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <operation>unknownOperation</operation>
</request>"""

        conn.send(destination='/queue/request.queue',
                  body=request3,
                  headers={'content-type': 'application/xml'})
        print("Request 3 (unknownOperation) has been sent!")

        print("\nCheck answers at Web Console: http://localhost:8161")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        conn.disconnect()
        print("\nDisconnected")

if __name__ == '__main__':
    send_test_requests()