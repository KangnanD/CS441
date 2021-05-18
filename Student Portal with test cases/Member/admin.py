from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Member.models import Member, Course, FileType, Post, Comment, Jira, File, Tag, Status

# Register your models here.
admin.site.register(Member)
admin.site.register(Course)
admin.site.register(FileType)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Jira)
admin.site.register(File)
admin.site.register(Tag)
admin.site.register(Status)
