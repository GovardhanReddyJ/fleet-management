from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
# Create your tests here.
class RegTestcase(TestCase):
    client=APIClient()
    @classmethod
    def setUpClass(cls):

        role=cls.client.post('/roles/',data={'name':'admin'})
        cls.role_id=role.json().get('id')
    def setUp(self  ):
        print('this is set up')
    def test_user_reg(self,):
        res = self.client.post('/signup',data={
                                    "username": "aleem",
                                    "password": "12345",
                                    "email": "aleem@gmail.com",
                                    "Aadhar_number":123456789100,
                                    "role":self.role_id
                                    })

        self.assertEqual(res.status_code,201)
        print('this is user registration')

    def tearDown(self):
        print('this isd tear down method')
    @classmethod
    def tearDownClass(cls):
        print('this is teardown class')


    # def test_positive(self):
    #     x = 5
    #     y = 4
    #     result = Multiit(x, y)
    #     self.assertEqual(result, 20)
    #     print('this is positive')