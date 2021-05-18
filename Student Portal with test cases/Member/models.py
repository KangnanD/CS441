
from PIL import Image
from django.contrib.auth.models import Group, User
from django.core.validators import FileExtensionValidator

# Create your models here.

from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from Member.storage import OverwriteStorage

from enum import Enum


class Role(Enum):
    TEACHER = 'Teacher'
    TEACHER_ASSISTANT = 'TeacherAssistant'
    STUDENT = 'Student'


class Member(User):
    ROLE_CHOICES = (
        (Role.STUDENT.name, Role.STUDENT.name),
        (Role.TEACHER_ASSISTANT.name, Role.TEACHER_ASSISTANT.name),
        (Role.TEACHER.name, Role.TEACHER.name),
    )

    def upload_to(self, filename):
        return "students/{}.{}".format(self.username, filename.split('.')[-1])

    image = models.ImageField(upload_to=upload_to, storage=OverwriteStorage(),default="students/student.png")
    accept = models.BooleanField()
    fixture = ['Member.json']
    role = models.CharField(choices=ROLE_CHOICES,max_length=20,default=Role.STUDENT.name)
    courses = models.ManyToManyField('Member.Course', related_name='member_courses', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.groups.add(Group.objects.filter(name=self.role).first())
        img = Image.open(self.image.path)  # Open image using self
        new_size = (530, 530)
        new_img = img.resize(new_size, Image.ANTIALIAS)
        new_img.save(self.image.path)
        print(new_img)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Member {} : {} : {} : {} '.format(self.username,self.email,self.accept,self.role)


class Course(models.Model):
    def upload_to(self,filename):
        return "courses/{}.{}".format(self.name,filename.split('.')[-1])

    fixture = ['Course.json']
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    image = models.ImageField(upload_to=upload_to,default='courses/course.png',storage=OverwriteStorage())
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.description)

    def save(self):
        super(Course, self).save()
        img = Image.open(self.image.path)  # Open image using self
        new_size = (530, 530)
        new_img = img.resize(new_size,Image.ANTIALIAS)
        new_img.save(self.image.path)
        print(new_img)


class FileType(models.Model):
    FILE_CHOICES = (
        ("docs", "Documents"),
        ("image", "Images"),
        ("file", "File"),
        ("link", "URL LINK"),
        ("zip", "Archive"),
    )

    fixtures = ['Course.json']
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=FILE_CHOICES,max_length=20,default="image")

    def __str__(self):
        return '{} : {}'.format(self.name, self.category)


class Post(models.Model):
    def upload_to(self,filename):
        return "posts/{}_{}_{}.{}".format(self.course.id,self.member.id,str(timezone.now()),filename.split('.')[-1])

    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    file = models.FileField(null=True,upload_to=upload_to,validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls','zip','7z','rar','mp4','avi','mp3'])])
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE,null=True)
    publish_date = models.DateTimeField('publish_date', default=timezone.now())
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    likes = models.ManyToManyField('Member.Member', related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField('Member.Member', related_name='post_dislikes', blank=True)

    def __str__(self):
        return 'Post: {} : {} {} '.format(self.content, self.member, self.file)


class Status(Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=50)
    fixtures = ['Status.json']

    def __str__(self):
        return 'Status: {} : {} {} '.format(self.name, self.description, self.tag)


class Tag(Model):
    tag = models.CharField(max_length=15)

    def __str__(self):
        return 'Tag: {} '.format(self.tag)


class Comment(Model):
    text = models.CharField(max_length=500)
    files = models.ManyToManyField('Member.File', related_name='comment_files', blank=True)
    created_at = models.DateTimeField('created_date', default=timezone.now())
    updated_at = models.DateTimeField('updated_date', default=timezone.now())
    user = models.ForeignKey(Member, related_name='comment_user', on_delete=models.CASCADE)

    def __str__(self):
        return 'Comment: {}:{} '.format(self.id,self.text,self.user.username)

class IssueType(Enum):
    EPIC = 'EPIC'
    STORY = 'STORY'
    TASK = 'TASK'
    ISSUE = 'ISSUE'
    BUG = 'BUG'
    SUB_TASK = 'SUB_TASK'


class Jira(Model):
    def upload_to(self, filename):
        return "jira/{}/{}".format(self.id,filename)

    ISSUE_CHOICES = (
        (IssueType.EPIC.name, IssueType.EPIC.name),
        (IssueType.STORY.name, IssueType.STORY.name),
        (IssueType.TASK.name, IssueType.TASK.name),
        (IssueType.ISSUE.name, IssueType.ISSUE.name),
        (IssueType.BUG.name, IssueType.BUG.name),
        (IssueType.SUB_TASK.name, IssueType.SUB_TASK.name),
    )
    type = models.CharField(choices=ISSUE_CHOICES,max_length=15,default=IssueType.ISSUE.name)
    code = models.CharField(max_length=15)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    files = models.ManyToManyField('Member.File', related_name='jira_files', blank=True)
    created_at = models.DateTimeField('created_date', default=timezone.now())
    updated_at = models.DateTimeField('updated_date', default=timezone.now())
    due_at = models.DateTimeField('due_date', default=timezone.now())
    reporter = models.ForeignKey(Member,related_name='reported', on_delete=models.CASCADE)
    assignee = models.ForeignKey(Member,related_name='assignee', on_delete=models.CASCADE,null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    links = models.ManyToManyField('Member.Jira', related_name='jira_links', blank=True)
    likes = models.ManyToManyField('Member.Member', related_name='jira_likes', blank=True)
    comments = models.ManyToManyField('Member.Comment', related_name='jira_comments', blank=True)

    def save(self, *args, **kwargs):
        self.code = self.course.code
        super().save(*args, **kwargs)
        self.code = self.course.code + '-' + str(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Jira:{}: {} : {} {} '.format(self.code,self.title, self.description, self.status)


class File(Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
    user = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return 'File: {}:{}:{}'.format(self.name,self.file.name,self.user)
