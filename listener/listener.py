import os
import time
import stomp
import logging
from lxml import etree
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageListener(stomp.ConnectionListener):
    def __init__(self, connection, response_queue):
        self.connection = connection
        self.response_queue = response_queue
        self.templates = self.load_templates()
        self.default_response = self.load_default_response()

    def load_templates(self):
        templates = {}
        requests_dir = Path('/app/templates/requests')
        responses_dir = Path('/app/templates/responses')

        if not requests_dir.exists():
            logger.warning("Directory with requests hasn't found")
            return templates

        for request_file in requests_dir.glob('*.xml'):
            response_file = responses_dir / request_file.name
            if response_file.exists():
                with open(request_file, 'r', encoding='utf-8') as rf:
                    request_xml = self.normalize_xml(rf.read())
                with open(response_file, 'r', encoding='utf-8') as rf:
                    response_xml = rf.read()
                templates[request_xml] = response_xml
                logger.info(f"Loaded template: {request_file.name}")
            else:
                logger.warning(f"Answer has not found for: {request_file.name}")

        logger.info(f"Total templates: {len(templates)}")
        return templates

    def load_default_response(self):
        default_file = Path('/app/templates/responses/default_error.xml')
        if default_file.exists():
            with open(default_file, 'r', encoding='utf-8') as f:
                return f.read()
        return """<?xml version="1.0" encoding="UTF-8"?>
<error>
    <code>404</code>
    <message>Template not found</message>
</error>"""

    def normalize_xml(self, xml_string):
        """delete \n, spaces"""
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.fromstring(xml_string.encode('utf-8'), parser)
            return etree.tostring(root, method='c14n').decode('utf-8')
        except Exception as e:
            logger.error(f"Parse error XML: {e}")
            return xml_string.strip()

    def on_message(self, frame):
        """incoming message handling"""
        try:
            body = frame.body
            logger.info(f"Received message from {frame.headers.get('destination', 'unknown')}")
            logger.debug(f"Body: {body[:200]}...")

            normalized_body = self.normalize_xml(body)
            response = self.templates.get(normalized_body)

            if response:
                logger.info("Matching template found")
            else:
                logger.warning("Template not found, sending default response")
                response = self.default_response

            self.connection.send(
                destination=f'/queue/{self.response_queue}',
                body=response,
                headers={
                    'content-type': 'application/xml',
                    'persistent': 'true',
                    'destination-type': 'ANYCAST'
                }
            )

            file_answers_dir = Path('/app/answers')
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = file_answers_dir / f"response_{timestamp}.xml"

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response)
                logger.info(f"Response saved to file: {filename}")
            except Exception as file_error:
                logger.error(f"Error saving response to file: {file_error}")

            logger.info(f"Answer sent to {self.response_queue}")

        except Exception as e:
            logger.error(f"Message processing error: {e}")

    def on_error(self, frame):
        logger.error(f"Error STOMP: {frame.body}")

    def on_disconnected(self):
        logger.warning("Disconnected from Artemis")

def ensure_queue_exists(conn, queue_name):
    try:
        conn.send(
            destination=f'/queue/{queue_name}',
            body='',
            headers={
                'content-type': 'text/plain',
                'destination-type': 'ANYCAST',
                'persistent': 'false',
                'expires': '1000'
            }
        )
        logger.info(f"Queue {queue_name} created/verified")
    except Exception as e:
        logger.warning(f"Queue creation warning: {e}")

def main():
    host = os.getenv('ARTEMIS_HOST', 'artemis')
    port = int(os.getenv('ARTEMIS_PORT', '61616'))
    user = os.getenv('ARTEMIS_USER', 'admin')
    password = os.getenv('ARTEMIS_PASSWORD', 'admin')
    request_queue = os.getenv('REQUEST_QUEUE', 'request.queue')
    response_queue = os.getenv('RESPONSE_QUEUE', 'response.queue')

    logger.info(f"Connecting to Artemis {host}:{port}")

    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = stomp.Connection([(host, port)])
            listener = MessageListener(conn, response_queue)
            conn.set_listener('', listener)
            conn.connect(user, password, wait=True)

            logger.info("Connected to Artemis")

            ensure_queue_exists(conn, request_queue)
            ensure_queue_exists(conn, response_queue)
            time.sleep(1)
            logger.info(f"Listening to the queue: {request_queue}")

            conn.subscribe(destination=f'/queue/{request_queue}', id=1, ack='auto')

            logger.info("Service started successfully. Waiting for messages...")

            while conn.is_connected():
                time.sleep(1)

        except Exception as e:
            retry_count += 1
            logger.warning(f"Attempt {retry_count}/{max_retries}: {e}")
            time.sleep(2)

    logger.error("Unable to connect to Artemis")

if __name__ == '__main__':
    main()