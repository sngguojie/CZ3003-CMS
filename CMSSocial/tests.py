from django.test import TestCase
from twitter_api import TwitterApp
import env
import json
import datetime

class CMSTwitterTest(TestCase):
	"""
	To test that the TwitterApp functions as expected
	"""
	def test_setup(self):

		self.twitter_app = TwitterApp(env.TWIT_CONSUMER_KEY, env.TWIT_CONSUMER_SECRET, env.TWIT_ACCESS_TOKEN, env.TWIT_ACCESS_TOKEN_SECRET)

	def test_update_status(self):
		"""
		Test initial state at startup is correct
		"""
		self.test_setup()

		status = 'CMS Status Update! ' + str(datetime.datetime.now())
		data = json.dumps({'status': status})

		before = self.twitter_app.get_public_tweets()
		response = self.client.post('/CMSSocial/update/', data, content_type="application/json")
		after = self.twitter_app.get_public_tweets()
		
		self.assertEqual(response.status_code, 200)

		response_data = json.loads(response.content)

		self.assertEqual(response_data['success'], True)

		self.assertEqual(list(set(after)-set(before)), [status])