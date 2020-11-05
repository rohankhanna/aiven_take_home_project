# importing unittest module
import unittest
from unittest.mock import MagicMock

from producer import get_website_ids, producer
from consumer import consumer

# unittest will test all the methods whose name starts with 'test'
class EndToEndTest(unittest.TestCase):
   # return True or False
   def test(self):
   	website_ids = get_website_ids()
   	producer(1, website_ids, run_once=True)
   	consumer(run_once=True)
   	self.assertEqual(True, True)
   	# TODO mock and stub the postgres db connection
   	# TODO mock and stub the Kafka connection
   	# TODO patch each function call such that no external api calls are made. 
   	# ensure that KafkaProducer and KafkaConsumer are both patched in such a way that when producer.send()
   	# is called, the data is appended to a variable that is modifiable by objects of both KafkaProducer and KafkaConsumer
# running the test
unittest.main()