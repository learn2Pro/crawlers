from kafka import KafkaConsumer
from kafka import SimpleClient
import json
import redis
import datetime


# To consume latest messages and auto-commit offsets
# client = SimpleClient(hosts="master:9092,slave:9092")
# topic = client.topics[0]
# consumer = topic.get_simple_consumer(
#     consumer_group='my-group',
# #    auto_offset_reset=OffsetType.EARLIEST,
#     reset_offset_on_start=True
# )
def con():
    pool = redis.Redis(host='23.106.148.101', port=6379, password=r'banwagong-redis')
    pool.ttl(1000)
    pool.set('foo', 'bar')
    print(pool.get('foo'))
    return pool


cli = con()
consumer = KafkaConsumer('test-logs',
                         group_id='my-group',
                         bootstrap_servers=['master:9092', 'slave:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')
    last = cli.get('logs')
    if last is None:
        # value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "   %s:%d:%d: key=%s value=%s" % (
        #     message.topic, message.partition,
        #     message.offset, message.key,
        #     message.value.decode('utf-8'))
        value = "%s:%d:%d: key=%s value=%s" % (
            message.topic, message.partition,
            message.offset, message.key,
            message.value.decode('utf-8'))
    else:
        # value = last.decode('utf-8') + "<br \>" + datetime.datetime.now().strftime(
        #     "%Y-%m-%d %H:%M:%S") + "   %s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
        #                                                              message.offset, message.key,
        #                                                              message.value.decode('utf-8'))
        value = last.decode('utf-8') + "<br \>" + "%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                                     message.offset, message.key,
                                                                     message.value.decode('utf-8'))
    cli.set('logs', value, ex=36000);
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value.decode('utf-8')))
