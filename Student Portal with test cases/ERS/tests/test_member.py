import unittest
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from Member.models import Member, Role, Course, Post
from Member.views import add_student, remove_student, my_student, online_members, login, post_to_my_timeline, like_post, \
    dislike_post, delete_post


class MyMemberTestCase(unittest.TestCase):
    def setUp(self) :
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        if len(Member.objects.all()) > 0:
            Member.objects.all().delete()
            User.objects.all().delete()
        self.member = Member(username='test_admin', password='test_admin@123', email='test_admin@localhost.com',role=Role.TEACHER.name,accept=True)
        self.member.set_password('test_admin@123')
        self.member.save()
        self.course = Course(code="TEST1",name="TEST1",description="TEST1")
        self.course.save()
        self.member.courses.add(self.course)
        self.member.save()
        self.student = Member(username='test_student', password='test_student@123', email='test_student@localhost.com',role=Role.STUDENT.name,accept=True)
        self.student.set_password('test_student@123')
        self.student.save()

    def tearDown(self):
        Member.objects.all().delete()
        User.objects.all().delete()
        self.member=None

    def test_add_student(self):
        # Create an instance of a POST request.
        data ={"course":self.course.id,"member":self.student.id}
        request = self.factory.post('/course/add/student',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = add_student(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.get('course/my/student')
        request.user = self.member
        request.member = self.member
        response = my_student(request)
        self.assertTrue(self.student.email in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_my_student(self):
        data ={"course":self.course.id,"member":self.student.id}
        request = self.factory.post('/course/add/student',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = add_student(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.get('course/my/student')
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = my_student(request)
        self.assertTrue(self.student.email in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_remove_student(self):
        # Create an instance of a POST request.
        data ={"course":self.course.id,"member":self.student.id}
        request = self.factory.post('/course/remove/student',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = remove_student(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.get('course/my/student')
        request.user = self.member
        request.member = self.member
        response = my_student(request)
        self.assertFalse(self.student.email in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_online_members(self):
        data = {"email": "test_admin@localhost.com", "password": "test_admin@123"}
        request = self.factory.post('/login/', data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data = {"email": "test_student@localhost.com", "password": "test_student@123"}
        request = self.factory.post('/login/', data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 302)
        request = self.factory.get('course/online/members')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.user = self.member
        request.member = self.member
        response = online_members(request)
        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        data = {"email": "test_student@localhost.com", "password": "test_student@123"}
        request = self.factory.post('/login/', data=data)
        middleware = SessionMiddleware()
        request.user = self.student
        request.member = self.student
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data={"title":"test_title","content":"test_content","member":self.member.id,"course":self.course.id}
        request = self.factory.post('/timeline/post/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = post_to_my_timeline(request)
        self.assertTrue("test_title" in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_like_post(self):
        data = {"email": "test_student@localhost.com", "password": "test_student@123"}
        request = self.factory.post('/login/', data=data)
        middleware = SessionMiddleware()
        request.user = self.student
        request.member = self.student
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data={"title":"test_title","content":"test_content","member":self.member.id,"course":self.course.id}
        request = self.factory.post('/timeline/post/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = post_to_my_timeline(request)
        self.assertTrue("test_title" in str(response.content))
        self.assertEqual(response.status_code, 200)
        post = Post.objects.filter(title="test_title").first()
        request = self.factory.post('like/post/'+str(post.id)+'/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = like_post(request,post_id=post.id)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.filter(id=post.id).get()
        self.assertTrue(str(self.student) in str(post.likes.all()))

    def test_dislike_post(self):
        data = {"email": "test_student@localhost.com", "password": "test_student@123"}
        request = self.factory.post('/login/', data=data)
        middleware = SessionMiddleware()
        request.user = self.student
        request.member = self.student
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data={"title":"test_title","content":"test_content","member":self.member.id,"course":self.course.id}
        request = self.factory.post('/timeline/post/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = post_to_my_timeline(request)
        self.assertTrue("test_title" in str(response.content))
        self.assertEqual(response.status_code, 200)
        post = Post.objects.filter(title="test_title").first()
        request = self.factory.post('dislike/post/'+str(post.id)+'/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = dislike_post(request,post_id=post.id)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(id=post.id)
        self.assertTrue(str(self.student) in str(post.dislikes.all()))

    def test_delete_post(self):
        data = {"email": "test_student@localhost.com", "password": "test_student@123"}
        request = self.factory.post('/login/', data=data)
        middleware = SessionMiddleware()
        request.user = self.student
        request.member = self.student
        middleware.process_request(request)
        request.session.save()
        response = login(request)
        self.assertEqual(response.status_code, 302)
        data={"title":"test_title","content":"test_content","member":self.member.id,"course":self.course.id}
        request = self.factory.post('/timeline/post/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = post_to_my_timeline(request)
        self.assertTrue("test_title" in str(response.content))
        self.assertEqual(response.status_code, 200)
        post = Post.objects.filter(title="test_title").first()
        request = self.factory.post('delete/post/'+str(post.id)+'/', data=data)
        request.user = self.student
        request.member = self.student
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = delete_post(request,post_id=post.id)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.filter(id=post.id)
        self.assertTrue(not post)


if __name__ == '__main__':
    unittest.main()
