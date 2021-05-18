import unittest
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from Member.models import Member, Role, Course
from Member.views import login, register, password_change


class MyLoginTestCase(unittest.TestCase):
    def setUp(self) :
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        if len(Member.objects.all()) > 0:
            Member.objects.all().delete()
            User.objects.all().delete()
        #self.user = User.objects.create(username='test_admin', password='test_admin@123', email='test_admin@localhost.com')
        self.member = Member(username='test_admin', password='test_admin@123', email='test_admin@localhost.com',role=Role.STUDENT.name,accept=True)
        self.member.set_password('test_admin@123')
        self.member.save()

    def tearDown(self):
        Member.objects.all().delete()
        User.objects.all().delete()
        self.member=None

    def test_register(self):
        # Create an instance of a POST request.
        data = {
                  "email":"admin_member@localhost.com",
                  "password":"test_admin@123",
                  "username":"admin_member",
                  "accept": "True"
               }
        request = self.factory.post('/register', data=data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = register(request)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Create an instance of a POST request.
        data ={"email":"test_admin@localhost.com","password":"test_admin@123"}
        request = self.factory.post('/login/',data=data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)

    def test_password_change(self):
        # Create an instance of a POST request.
        data = {"email": "test_admin@localhost.com", "password": "test_admin@123"}
        request = self.factory.post('/login/', data=data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data ={"email": "test_admin@localhost.com","old_password":"test_admin@123","new_password1":"test_admin1@123","new_password2":"test_admin1@123"}
        request = self.factory.post('/password-change',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = password_change(request)
        self.assertEqual(response.status_code, 200)
        data = {"email": "test_admin@localhost.com", "password": "test_admin1@123"}
        request = self.factory.post('/login', data=data)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
