import  os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mysite.settings")
django.setup()

from django.test import  TestCase
from sign.models import  Event, Guest
from django.contrib.auth.models import User
from django.test import  Client
from datetime import  datetime


class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=200,
                             address='shenzhen', start_time='2018-04-01 10:00:00')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='18734352334',
                            email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(realname='alen')
        self.assertEqual(result.phone, '18734352334')

class PageTest(TestCase):

    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginPage(TestCase):

    def setUp(self):
        User.objects.create_superuser('test', 'test@mail.com', 'test123456')
        self.c = Client()

    def test_login_aciton_username_null(self):
        test_data = {'username':'', 'password':'test123456'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or passwrod error !", response.content)

    def test_login_action_username_password_correct(self):
        test_data = {'username':'test', "password":'test123456'}
        response = self.c.post('/login_action/', data = test_data)
        self.assertEqual(response.status_code,  302)

class EventManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=2, name='Mi5', limit=200, status=True, address = 'beijing', start_time = datetime(2018,4,1,10,0,0))
        self.c = Client()

    def test_event_manage_success(self):
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        response = self.c.post('/event_search_name/', {"name":"Mi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mi5", response.content)
        self.assertIn(b"beijing", response.content)

class GuestManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="Mi5", limit=200, address="shenzhen",
            status=1, start_time=datetime(2018,4,1,14,0,0))

        Guest.objects.create(realname='alen', phone='18676543210',
                             email='alen@mail.com', sign=0,  event_id=1)
        self.c = Client()

    def test_guest_manage_success(self):
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18676543210", response.content)

    def test_guest_search_name(self):
        response = self.c.post('/guest_search_name/', { "phone": '18676543210'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alen', response.content)
        self.assertIn(b'18676543210', response.content)

class SignIndexActionTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="Mi5", limit=200, address="shenzhen",
            status=1, start_time=datetime(2018,4,1,14,0,0))

        Event.objects.create(id=2, name='mate7', limit=200, address="shenzhen",
                             status=1, start_time=datetime(2018,4,3,14,0,0))

        Guest.objects.create(realname='alen', phone='18659531027',
                             email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname='Tom', phone='15203041027',
                             email='tom@mail.com', sign=1, event_id=2)

        self.c = Client()

    def test_sign_index_aciton_phone_null(self):
        response = self.c.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error', response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.c.post('/sign_index_action/2/', { "phone": "18659531027"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event id or name error', response.content)

    def  test_sign_index_aciton_phone_sign_has(self):
        response = self.c.post('/sign_index_action/2/', { 'phone': "15203041027"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in', response.content)

    def test_sign_success(self):
        response = self.c.post('/sign_index_action/1/', {'phone': '18659531027'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success', response.content)
