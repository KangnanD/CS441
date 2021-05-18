from django.conf.urls import url
from django.urls import path

from Member import views
from django.contrib.auth import views as auth_view
# SET THE NAMESPACE!
app_name = 'Member'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^about/$',views.about,name='about'),
    url(r'^guidelines/$',views.guidelines,name='guidelines'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    path('timeline/<int:course_id>/', views.timeline, name='timeline'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.password_change, name='password_change'),
    path('password-change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('timeline/', views.my_timeline, name='my_timeline'),
    path('timeline/<int:course_id>/<int:member_id>/post/', views.post_to_timeline, name='post_to_timeline'),
    path('timeline/', views.my_timeline, name='my_timeline'),
    path('timeline/post/', views.post_to_my_timeline, name='post_to_my_timeline'),
    path('like/post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('delete/post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('api/courses', views.search, name='search'),
    path('api/search_posts', views.search_posts, name='search_posts'),
    path('get_posts/<str:name>', views.get_posts, name='get_posts'),
    path('courses', views.courses, name='courses'),
    path('course/add/student', views.add_student, name='add_student'),
    path('course/remove/student', views.remove_student, name='remove_student'),
    path('course/my/student', views.my_student, name='my_student'),
    path('course/online/members', views.online_members, name='online_members'),
    path('jira/', views.jira, name='jira'),
    path('jira/create', views.jira_create, name='jira_create'),
    path('api/update/jira/status', views.update_jira_status, name='update_jira_status'),
    path('api/update/jira/assignee', views.update_jira_assignee, name='update_jira_assignee'),
    path('jira/<int:jira_id>/view', views.jira_view, name='jira_view'),
    path('jira/<int:jira_id>/edit', views.jira_edit, name='jira_edit'),
    path('jira/<int:jira_id>/link', views.jira_link, name='jira_link'),
    path('files/upload/', views.files_upload, name='files_upload'),
    path('files/delete/', views.files_delete, name='files_delete'),
]