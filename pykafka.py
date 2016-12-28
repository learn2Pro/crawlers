from pykafka import KafkaClient
import logging

client = KafkaClient(hosts="master:9092,slave:9092")

topic = client.topics['test-logs']

balanced_consumer = topic.get_balanced_consumer(
    consumer_group='group1',
    auto_commit_enable=True,
    #    reset_offset_on_start=True,
    zookeeper_connect='master:2181'
)

for message in balanced_consumer:
    if message is not None:
        print(message.offset, message.value)
