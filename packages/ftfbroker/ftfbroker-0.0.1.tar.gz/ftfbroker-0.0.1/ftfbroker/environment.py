import os
import ssl

# Kafka connection settings
KAFKA_SERVER = os.getenv('FTF_KAFKA_SERVER', '')
KAFKA_USER = os.getenv('FTF_KAFKA_USER', '')
KAFKA_PASSWORD = os.getenv('FTF_KAFKA_PASSWORD', '')

DEFAULT_CONTEXT = ssl.create_default_context()
DEFAULT_CONTEXT.options &= ssl.OP_NO_TLSv1
DEFAULT_CONTEXT.options &= ssl.OP_NO_TLSv1_1

# Kafka producer meta info
KAFKA_SENDING_SERVICE = os.getenv('FTF_KAFKA_SENDING_SERVICE', "NOTSET")
KAFKA_ENVIRONMENT = os.getenv("FTF_KAFKA_ENVIRONMENT", "DEVELOPMENT")
