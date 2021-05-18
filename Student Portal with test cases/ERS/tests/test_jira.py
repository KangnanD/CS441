import unittest
import unittest
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from Member.models import Member, Role, Course, Post, Jira, Status
from Member.views import add_student, remove_student, my_student, online_members, login, post_to_my_timeline, like_post, \
    dislike_post, delete_post, jira_view, update_jira_assignee, update_jira_status, jira_create


class MyJiraTestCase(unittest.TestCase):

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

    def test_jira_create(self):
        # Create an instance of a POST request.
        data ={'type':'STORY','title':'TITLE', 'description':'DESCRIPTION', 'due_at':"04/04/2022", 'reporter':self.member.id,'assignee':self.member.id, 'status':'1','course':self.course.id}
        request = self.factory.post('/jira/create',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = jira_create(request)
        self.assertEqual(response.status_code, 200)
        jira = Jira.objects.filter(title="TITLE").get()
        request = self.factory.get('jira/'+str(jira.id)+'/view')
        request.user = self.member
        request.member = self.member
        response = jira_view(request,jira_id=jira.id)
        self.assertTrue(jira.title in str(response.content))
        self.assertEqual(response.status_code, 200)

    def test_jira_update_status(self):
        # Create an instance of a POST request.
        data ={'type':'STORY','title':'TITLE', 'description':'DESCRIPTION', 'due_at':"04/04/2022", 'reporter':self.member.id,'assignee':self.member.id, 'status':'1','course':self.course.id}
        request = self.factory.post('/jira/create',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = jira_create(request)
        self.assertEqual(response.status_code, 200)
        jira = Jira.objects.filter(title="TITLE").get()
        request = self.factory.get('jira/'+str(jira.id)+'/view')
        request.user = self.member
        request.member = self.member
        response = jira_view(request,jira_id=jira.id)
        self.assertTrue(jira.title in str(response.content))
        self.assertEqual(response.status_code, 200)
        data={'jira_id':jira.id,'status':'IN_PROGRESS'}
        request = self.factory.post('api/update/jira/status',data)
        request.user = self.member
        request.member = self.member
        response = update_jira_status(request)
        jira = Jira.objects.filter(title="TITLE").get()
        self.assertEqual(str(jira.status.tag),'IN_PROGRESS')
        self.assertEqual(response.status_code, 200)

    def test_jira_update_assignee(self):
        # Create an instance of a POST request.
        data ={'type':'STORY','title':'TITLE', 'description':'DESCRIPTION', 'due_at':"04/04/2022", 'reporter':self.member.id,'assignee':self.member.id, 'status':'1','course':self.course.id}
        request = self.factory.post('/jira/create',data=data)
        request.user = self.member
        request.member = self.member
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = jira_create(request)
        self.assertEqual(response.status_code, 200)
        jira = Jira.objects.filter(title="TITLE").get()
        request = self.factory.get('jira/'+str(jira.id)+'/view')
        request.user = self.member
        request.member = self.member
        response = jira_view(request,jira_id=jira.id)
        self.assertTrue(jira.title in str(response.content))
        self.assertEqual(response.status_code, 200)
        data={'jira_id':jira.id,'assignee':self.student.id}
        request = self.factory.post('api/update/jira/assignee',data)
        request.user = self.member
        request.member = self.member
        response = update_jira_assignee(request)
        jira = Jira.objects.filter(title="TITLE").get()
        self.assertEqual(str(jira.assignee),str(self.student))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
