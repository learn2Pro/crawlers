from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import log
import msgpack


producer = KafkaProducer(bootstrap_servers=['master:9092', 'slave:9092'])

# Asynchronous by default
future = producer.send('test-logs', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=1000)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)

# produce keyed messages to enable hashed partitioning
for _ in range(105):
    producer.send('test-logs', key=b'foo1', value=b'bar1')

# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('msgpack-topic', {'key': 'value'})
#
# # produce json messages
# producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
# producer.send('json-topic', {'key': 'value'})
#
# # produce asynchronously
# for _ in range(100):
#     producer.send('test-logs', b'msg')

# block until all async messages are sent
producer.flush()

# configure multiple retries
producer = KafkaProducer(retries=5)
