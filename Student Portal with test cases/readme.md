# ERS
## Python and Django web app project
### Django files:
    .
        ├── ERS
        │   ├── asgi.py
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── manage.py

    -   manage.py automatically generated
    -   db.sqlite3 database sqlite 
    -   ERS default app (django app)
    -   ERS/settings.py stttings files for the django application
    -   ERS/urls.py url accessable in the web app
    -   ERS/middleware.py middleware process_request which is called for every request.
        process_request process set the request.member variable to the currect member else the normal user
    -   media folder where the app stores the uploaded files
    -   static folder where we store/put the css js files
    -   Member is a small app in ERS portal
    -   Member/fixtures folder contains data for database initialization
    -   Member/migrations folder is auto generated about the models changes in db
    -   Member/admin.py file registers the all the models in the Member app
    -   Member/app.py file contains the config for Member app
    -   Member/forms.py contains the forms used in app like signup login etc.
    -   Member/models.py contains the DB Models used in the app
    -   Member/storage.py contains method to store the file and if file exist then update file.
    -   Member/urls.py contains the urls accessing by the member
    -   Member/views.py contains the view function which returns the html page and data as per request.
    -   Member/validators.py contains the file excention validation function


## Added Configuration in settings.py
    
        ```
            STATIC_URL = '/static/'
            STATICFILES_DIRS = [
                os.path.join(BASE_DIR, "static"),
            ]
            STATIC_DIR = os.path.join(BASE_DIR,'static')
            STATIC_URL = '/static/'
            STATICFILES_DIRS = [STATIC_DIR,]
            
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            MEDIA_URL = '/media/'
            CRISPY_TEMPLATE_PACK = 'bootstrap4'
            LOGIN_REDIRECT_URL = '/member/home'
            
            DJANGO_SUPERUSER_USERNAME='admin'
            DJANGO_SUPERUSER_PASSWORD='admin@123'
            DJANGO_SUPERUSER_EMAIL='admin@localhost.com'
            AUTH_PASSWORD_VALIDATORS=[]
            LOGIN_URL = '/login/'
            
            LOGIN_REDIRECT_URL = '/'
            
            # Add user_unique_email to INSTALLED_APPS
            INSTALLED_APPS.append('user_unique_email')
            
            # Custom User model
            AUTH_USER_MODEL = 'user_unique_email.User'
        ```
        -    we are using AUTH_USER_MODEL as user_unique_email.User as this has unique email
    

## Models used:
       -    Member
       -    Course
       -    FileType
       -    Post
       -    PostLikes
       -    PostDislikes
## Added Files:
.
├── clear_all.sh
├── db.sqlite3
├── ERS
│   ├── asgi.py
│   ├── __init__.py
│   ├── middleware.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── media
│   ├── courses
│   │   ├── course.png
│   │   └── courses.png
│   ├── posts
│   └── members
├── readme.md
├── requirements.txt
├── static
│   ├── css
│   │   └── profile.css
│   └── js
│       ├── course_search.js
│       └── jsi18.js
├── Member
│   ├── admin.py
│   ├── apps.py
│   ├── fixtures
│   │   ├── Course.json
│   │   ├── FileType.json
│   │   └── Member.json
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
└── templates
    └── Member
        ├── about.html
        ├── base.html
        ├── courses.html
        ├── guidelines.html
        ├── home.html
        ├── index.html
        ├── login.html
        ├── my_timeline.html
        ├── password_change_form.html
        ├── post.html
        ├── profile_card.html
        ├── profile.html
        ├── registration.html
        └── timeline.html


## Django Admin
    -    The Django admin site¶
    -    One of the most powerful parts of Django is the automatic admin interface. It reads metadata from your models to provide a quick, model-centric interface where trusted users can manage content on your site. The admin’s recommended use is limited to an organization’s internal management tool. It’s not intended for building your entire front end around.
    -    The admin has many hooks for customization, but beware of trying to use those hooks exclusively. If you need to provide a more process-centric interface that abstracts away the implementation details of database tables and fields, then it’s probably time to write your own views.
    -    https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

## Forms
    -    we have used different forms for different purpose.
    -   like register, login, post etc.


## templates
    -    Templates are stored in templates/Member folder
    -   The templates are html templates for login register post etc
    
## admin url:
    -   /admin

## Clear all
    - the file clear_all.sh is a bash file use to clear db and files and reset the website

## Sqlite DB
    -    We have used SQLIte DB for database to store the data.
    
## requirements.txt
    -    this file contains the python modules used in this project.

## windows
	- download gitbash
	- download python 3.8.5 (if you already have try running it, if not download this exact version)
		- if you are still having issue running/starting localhost, uninstall all python software
		- download anaconda python (https://www.anaconda.com/products/individual)
			during the installation it will ask you if you want to download python 3.8, check yes

## how to start:
    -   first run sh clear_all.sh or sh clear_all_windows.sh if you are on windows

    -   put admin password when it asked and remember that i.e admin@123
        -   username:admin
        -   password:admin@123
    -   run server with command: python manage.py runserver 0.0.0.0:5000
		- 	open browser
		- 	access portal at localhost:5000
	- 	create a superuser
		- 	open a new gitbash, navigate to your project and type this command: winpty python manage.py createsuperuser  --username admin --email admin@localhost.com
		- create a password
		-	open browser
		-   admin portal at localhost:5000/admin
			-   register for student and teacher with 2 accounts
			-   assign course to a teacher/professor from /admin
				-   now teacher can add students to that course.
				-   now teacher can remove students to that course.
    -   play with website	
		- create tickets
		- view tickets
		- modify tickets
		- create posts
		- share posts


# UNIT Test
    -   python manage.py test
## Test Cases:
    -   test_register(self):
        -   test the register functionality
    -   test_login(self):
        -   test the login functionality
    -   test_password_change(self):
        -   test the password change functionality
    -   test_add_student(self)
        -   test the add student to the course functionality
    -   test_my_student(self)
        -   test the my students view for the teacher functionality
    -   test_remove_student(self)
        -   test the remove student from course functionality
    -   test_online_members(self)
        -   test the online members view functionality
    -   test_add_post(self)
        -   test the add post on timeline functionality
    -   test_like_post(self)
        -   test the like post functionality
    -   test_dislike_post(self)
        -   test the dislike functionality
    -   test_delete_post(self)
        -   test the delete post functionality
    -   test_jira_create(self)
        -   test the jira ticket creation functionality
    -   test_jira_update_status(self)
        -   test the update jira ticket functionality
    -   test_jira_update_assignee(self)
        -   test the update jira assignee functionality


# REFERENCES:
    -   https://docs.djangoproject.com/en/3.2/