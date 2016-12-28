from kafka import KafkaConsumer
from kafka import SimpleClient
import json

# To consume latest messages and auto-commit offsets
# client = SimpleClient(hosts="master:9092,slave:9092")
# topic = client.topics[0]
# consumer = topic.get_simple_consumer(
#     consumer_group='my-group',
# #    auto_offset_reset=OffsetType.EARLIEST,
#     reset_offset_on_start=True
# )
consumer = KafkaConsumer('test-logs',
                         group_id='my-group',
                         bootstrap_servers=['master:9092', 'slave:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))


