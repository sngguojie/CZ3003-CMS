from django.test import TestCase, Client
from CMSStatus.models import CMSStatus
from common import datetime_util
import json

class CMSStatusTest(TestCase):
	"""
	To test that the CMSStatus functions as expected
	"""
	def test_setup(self):
		"""
		"""
		self.client = Client()
		execfile('initialize_db.py')
		self.assertEqual(len(CMSStatus.objects.filter(id=1)), 1)


	def test_initial(self):
		"""
		Test initial state at startup is correct
		"""
		self.test_setup()
		
		response = self.client.get('/CMSStatus/read/1/')
		
		self.assertEqual(response.status_code, 200)

		response_data = json.loads(response.content)

		self.assertEqual(response_data['active'], False)
		self.assertEqual(response_data['success'], True)


		
		self.assertEqual(len(CMSStatus.objects.filter(id=1)), 1)
		cms = CMSStatus.objects.get(id=1)
		
		self.assertEqual(cms.last_sent, None)

	def test_update_true(self):
		"""
		Test CMSStatus is updated to active correctly
		"""
		self.test_setup()
		
		data = json.dumps({"active": True})

		before = datetime_util.sgt_now()
		response = self.client.post('/CMSStatus/update/1/', data, content_type="application/json")
		after = datetime_util.sgt_now()
		
		self.assertEqual(response.status_code, 200)
		

		response_data = json.loads(response.content)
		self.assertTrue(response_data['success'] == True)

		self.assertTrue(len(CMSStatus.objects.filter(id=1)), 1)
		
		cms = CMSStatus.objects.get(id=1)
		self.assertTrue(cms.last_sent > before)
		self.assertTrue(cms.last_sent < after)

	def test_update_false(self):
		"""
		Test CMSStatus is updated to inactive correctly
		"""
		self.test_setup()
		
		data = json.dumps({"active": False})

		response = self.client.post('/CMSStatus/update/1/', data, content_type="application/json")
		
		self.assertEqual(response.status_code, 200)

		response_data = json.loads(response.content)
		self.assertTrue(response_data['success'] == True)