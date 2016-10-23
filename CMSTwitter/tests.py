from django.test import TestCase
from twitter_api import TwitterApp
import secret
import json
import datetime

class CMSTwitterTest(TestCase):
	"""
	To test that the TwitterApp functions as expected
	"""
	def test_setup(self):

		self.twitter_app = TwitterApp(secret.CONSUMER_KEY, secret.CONSUMER_SECRET, secret.ACCESS_TOKEN, secret.ACCESS_TOKEN_SECRET)

	def test_update_status(self):
		"""
		Test initial state at startup is correct
		"""
		self.test_setup()

		status = 'CMS Status Update! ' + str(datetime.datetime.now())
		data = json.dumps({'status': status})

		before = self.twitter_app.get_public_tweets()
		response = self.client.post('/CMSTwitter/update/', data, content_type="application/json")
		after = self.twitter_app.get_public_tweets()
		
		self.assertEqual(response.status_code, 200)

		response_data = json.loads(response.content)

		self.assertEqual(response_data['success'], True)

		self.assertEqual(list(set(after)-set(before)), [status])