from PIL import Image
from PIL.Image import Image
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.db.models.functions import Concat
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Member.forms import MemberRegisterForm, MemberLoginForm, MemberPostForm, MemberPasswordChangeForm, JiraCreateForm, \
    CommentCreateForm, FileCreateForm, MemberUpdateForm, AddStudentForm, LinkJiraForm, MemberPostFormWithFiles, \
    RemoveStudentForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from Member.models import Member, Course, FileType, Post, Jira, Status, File, Role
from django.db.models import Value, ExpressionWrapper, CharField, F, Q

from Member.permission import group_required


def index(request):
    if request.member.is_authenticated:
        member = request.member
        courses = member.courses.all
        file_types = FileType.objects.all()
        context = {'member': member, 'courses': courses, 'file_types': file_types}
        print("Member:", member)
        return render(request, 'Member/my_timeline.html', context)
    else:
        return render(request, 'Member/index.html')


@login_required
def courses(request):
    if request.member.is_authenticated:
        member = request.member
        file_types = FileType.objects.all()
        context = {}
        context['member'] = member
        context['courses'] = member.courses.all()
        context['file_types'] = file_types
        print("Member:", member)
        return render(request, 'Member/courses.html', context)
    else:
        return render(request, 'Member/index.html')


@group_required("TEACHER")
@login_required
def add_student(request):
    if request.member.is_authenticated:
        member = request.member
        all_courses = member.courses.all()
        file_types = FileType.objects.all()
        if request.method == 'GET':
            context = {}
            context['member'] = member
            context['courses'] = member.courses.all()
            context['file_types'] = file_types
            context['add_student_form'] = AddStudentForm(request=request)
            print("Member:", member)
            return render(request, 'Member/add_student.html', context)
        else:
            add_student_form = AddStudentForm(request.POST,request=request)
            add_student_form.is_valid()
            context = {}
            context['member'] = member
            context['courses'] = all_courses
            context['file_types'] = file_types
            context['add_student_form'] = add_student_form
            print("Member:", member)
            student = Member.objects.filter(id=request.POST['member']).first()
            course = Course.objects.filter(id=request.POST['course']).first()
            student.courses.add(course)
            student.save()
            return redirect('/course/my/student', context)

    else:
        return render(request, 'Member/add_student.html')


@group_required("TEACHER")
@login_required
def remove_student(request):
    if request.member.is_authenticated:
        member = request.member
        all_courses = member.courses.all()
        file_types = FileType.objects.all()
        if request.method == 'GET':
            context = {}
            context['member'] = member
            context['courses'] = member.courses.all()
            context['file_types'] = file_types
            context['remove_student_form'] = RemoveStudentForm(request=request)
            print("Member:", member)
            return render(request, 'Member/remove_student.html', context)
        else:
            remove_student_form = RemoveStudentForm(request.POST,request=request)
            remove_student_form.is_valid()
            context = {}
            context['member'] = member
            context['courses'] = all_courses
            context['file_types'] = file_types
            context['remove_student_form'] = remove_student_form
            print("Member:", member)
            student = Member.objects.filter(id=request.POST['member']).first()
            course = Course.objects.filter(id=request.POST['course']).first()
            student.courses.remove(course)
            student.save()
            return redirect('/course/my/student', context)

    else:
        return render(request, 'Member/remove_student.html')


@login_required()
def online_members(request):
    if request.method == 'GET':
        if request.member.is_authenticated:
            member = request.member
            context = {}
            context['member'] = member
            context['courses'] = member.courses.all()
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            uid_list=[]
            for session in sessions:
                data = session.get_decoded()
                uid_list.append(data.get('_auth_user_id', None))
            course_id=[]
            member_courses = member.courses.all()
            for c in member_courses:
                course_id.append(c.id)

            context['online_members'] = Member.objects.filter(id__in=uid_list).filter(courses__in=course_id)
            return render(request, 'Member/online_members.html',context)
        else:
            return render(request,'Member/login.html')
    else:
        return render(request, 'Member/login.html')


@group_required("TEACHER")
@login_required()
def my_student(request):
    if request.method == 'GET':
        if request.member.is_authenticated:
            member = request.member
            context = {}
            context['member'] = member
            context['courses'] = member.courses.all()
            students = []
            for c in member.courses.all():
                c_students = c.member_courses.filter(role=Role.STUDENT.name).all()
                for s in c_students:
                    students.append(s)
            context['students'] = students
            return render(request, 'Member/my_student.html',context)
        else:
            return render(request,'Member/login.html')
    else:
        return render(request, 'Member/login.html')


def about(request):
    context = {}
    if request.member.is_authenticated:
        member = request.member
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context['member'] = member
        context['courses'] = courses
        context['file_types'] = file_types
        print("Member:", member)

    return render(request, 'Member/about.html', context)


def guidelines(request):
    context = {}
    if request.member.is_authenticated:
        member = request.member
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context['member'] = member
        context['courses'] = courses
        context['file_types'] = file_types
        print("Member:", member)

    return render(request, 'Member/guidelines.html', context)


def login(request):
    if request.method == 'POST':
        login_form = MemberLoginForm(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Member.objects.filter(email=email).first() is not None:
            username = Member.objects.filter(email=email).first().username
            member = authenticate(username=username, password=password)
            if member:
                if member.is_active:
                    auth_login(request, member)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'Member/login.html',
                                  {'login_form': login_form, 'message': 'account inactive'})
            else:
                print("Someone tried to login and failed.")
                print("They used email: {} and password: {}".format(email, password))

        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email, password))

        return render(request, 'Member/login.html', {'login_form': login_form, 'message': 'Invalid Login Details'})

    else:
        login_form = MemberLoginForm()
    return render(request, 'Member/login.html', {'login_form': login_form})


@login_required
def logout(request):
    auth_logout(request)
    request.session.flush()
    request.session.clear()
    return HttpResponseRedirect(reverse('index'))


@login_required
def password_change(request):
    password_changed = False
    if request.method == 'POST':
        form = MemberPasswordChangeForm(member=request.member, data=request.POST)
        if form.is_valid():
            print("form valid")
            print(request.POST)
            password = request.POST["new_password1"]
            request.member.set_password(password)
            request.member.save()
            update_session_auth_hash(request, form.member)
            password_changed = True
        else:
            print("form invalid")
            print(form.errors)
    else:
        form = MemberPasswordChangeForm(member=request.member)

    member = request.member
    courses = Course.objects.all()
    return render(request, 'Member/password_change_form.html',
                  {'form': form, 'member': member, 'courses': courses, 'password_changed': password_changed})


def register(request):
    registered = False
    if request.method == 'POST':
        print(request.POST.dict(), request.FILES.dict())
        member_register_form = MemberRegisterForm(request.POST, request.FILES)
        if member_register_form.is_valid():
            member = member_register_form.save()
            member.set_password(member.password)
            member.save()
            registered = True
            auth_login(request, member)
            return HttpResponseRedirect(reverse('index'))
        else:
            print(member_register_form.errors)
    else:
        member_register_form = MemberRegisterForm()

    print(member_register_form)

    return render(request, 'Member/registration.html',
                  {'member_register_form': member_register_form,
                   'registered': registered})


@login_required
def password_change(request):
    password_changed = False
    if request.method == 'POST':
        form = MemberPasswordChangeForm(member=request.member,data=request.POST)
        if form.is_valid():
            print("form valid")
            print(request.POST)
            password = request.POST["new_password1"]
            request.member.set_password(password)
            request.member.save()
            update_session_auth_hash(request, form.member)
            password_changed = True
        else:
            print("form invalid")
            print(form.errors)
    else:
        form = MemberPasswordChangeForm(member=request.member)

    member = request.member
    all_courses = member.courses.all()
    return render(request, 'Member/password_change_form.html',
                  {'form': form,'member':member,'courses':all_courses,'password_changed':password_changed})


@login_required
def profile(request):
    print("profile")
    if request.method == 'POST':
        print(request.POST.dict(), request.FILES.dict())
        member_update_form = MemberUpdateForm(request.POST, request.FILES,instance=request.member)
        if member_update_form.is_valid():
            member = member_update_form.save()
            member.save()
            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(member_update_form.errors)
    else:
        member_update_form = MemberUpdateForm(instance=request.member)

    member = request.member
    context = {}
    context['member'] = member
    context['courses'] = member.courses.all()
    context['member_update_form'] = member_update_form
    return render(request, 'Member/profile.html', context)


@login_required
def my_timeline(request):
    if request.member.is_authenticated:
        member = request.member

        posts = Post.objects.filter(member=member)
        file_types = FileType.objects.all()
        context = {}
        context['member'] = member
        context['courses'] = member.courses.all()
        context['file_types'] = file_types
        context['posts'] = posts
        print("Timeline:", posts)
        return render(request, 'Member/my_timeline.html', context)
    else:
        return redirect("index")


@login_required()
def post_to_my_timeline(request):
    if request.member.is_authenticated and request.method == 'POST':
        member = request.member
        print(request.POST.dict())
        file_types = FileType.objects.all()
        #course = Course.objects.filter(id=request.POST['course']).first()
        member_post_form_with_files = MemberPostFormWithFiles(request.POST, request.FILES)
        if member_post_form_with_files.is_valid():
            print("member post form with files is valid")
            post = member_post_form_with_files.save()
            post.member=member
            post.save()
            posts = Post.objects.filter(member=member)
            context = {}
            context['member'] = member
            context['courses'] = member.courses.all()
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Member/my_timeline.html', context)

        else :
            member_post_form = MemberPostForm(request.POST, request.FILES)
            if member_post_form.is_valid():
                print("member post form is valid")
                post = member_post_form.save()
                post.member = member
                post.save()
                posts = Post.objects.filter(member=member)
                context = {}
                context['member'] = member
                context['courses'] = member.courses.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Member/my_timeline.html', context)
            else:
                print("2.else:", member_post_form.errors)
                posts = Post.objects.filter(member=member)
                context = {}
                context['errors'] = member_post_form.errors
                context['member'] = member
                context['courses'] = member.courses.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Member/my_timeline.html', context)
    elif request.member.is_authenticated and request.method == 'GET':
        posts = Post.objects.filter(member=request.member)
        file_types = FileType.objects.all()
        context = {}
        context['member'] = request.member
        context['courses'] = request.member.courses.all()
        context['file_types'] = file_types
        context['posts'] = posts
        print("Timeline:", posts)
        return render(request, 'Member/my_timeline.html', context)
    else:
        return redirect("index")


@login_required
def timeline(request, course_id):
    if request.member.is_authenticated:
        member = request.member
        course = Course.objects.filter(id=course_id).first()

        if course is not None:
            posts = Post.objects.filter(course=course)
            file_types = FileType.objects.all()
            context = {}
            context['member'] = member
            context['chomeourse'] = course
            context['courses'] = member.courses.all()
            context['course'] = course
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Member/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")


@login_required()
def post_to_timeline(request, course_id, member_id):
    file_types = FileType.objects.all()
    if request.member.is_authenticated:
        member = request.member
        course = Course.objects.filter(id=course_id).first()
        member_post_form = MemberPostForm(request.POST, request.FILES)
        member_post_form_with_files = MemberPostFormWithFiles(request.POST, request.FILES)

        if course is not None and member is not None:
            if member_post_form_with_files.is_valid():
                print("member post form with files is valid")
                member_post_form_with_files.save()
                posts = Post.objects.filter(member=member)
                context = {}
                context['member'] = member
                context['courses'] = member.courses.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Member/my_timeline.html', context)
            elif member_post_form.is_valid():
                    print("member post form is valid")
                    member_post_form.save()
                    posts = Post.objects.filter(member=member)
                    context = {}
                    context['member'] = member
                    context['courses'] = member.courses.all()
                    context['file_types'] = file_types
                    context['posts'] = posts
                    print("Timeline:", posts)
                    return render(request, 'Member/my_timeline.html', context)
            else:
                print("2.else:", member_post_form.errors)
                posts = Post.objects.filter(course=course)
                file_types = FileType.objects.all()
                context = {}
                context['member'] = member
                context['course'] = course
                context['courses'] = member.courses.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Member/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")


@login_required
def like_post(request, post_id):
    member = request.member
    post = Post.objects.filter(id=post_id).first()
    print(post.likes.all().count())
    member = Member.objects.get(id=member.id)
    if post.likes.filter(email=member.email).count() >= 1:
        post.likes.remove(member)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        post.likes.add(member)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_post(request, post_id):
    member = request.member
    post = Post.objects.filter(id=post_id).first()
    print(post.dislikes.all().count())
    if post.dislikes.filter(email=member.email).count() >= 1:
        post.dislikes.remove(member)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        post.dislikes.add(member)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_post(request, post_id):
    print(request.META.get('HTTP_REFERER'))
    member = request.member
    post = Post.objects.filter(id=post_id).filter(member=member).first()
    print(post)
    if post is not None:
        member = Member.objects.get(id=member.id)
        post.file.delete()
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def search(request):
    name = request.GET['name']
    member = request.member
    base_url = '/timeline/'
    base_image = '/media/'

    courses = Course.objects.filter(name__icontains=name).all().annotate(
        course_url=Concat(Value(base_url), 'id', output_field=CharField())).annotate(
        image_url=Concat(Value(base_image), 'image', output_field=CharField()))

    data = {
        "results": list(courses.values('name', 'description', 'image_url', 'course_url')),
        "name": "Course result",
    }
    print(data)
    return JsonResponse(data)


@login_required()
def search_posts(request):
    name = request.GET['name']
    member = request.member
    base_url = '/get_posts/' + name
    base_image = '/media/'

    posts = Post.objects.filter(Q(content__icontains=name) | Q(title__icontains=name)).all().annotate(
        post_url=Value(base_url, output_field=CharField()))
    data = {
        "results": list(posts.values('title', 'content', 'course', 'post_url', 'member')),
        "name": "Post result",
    }
    print(data)
    return JsonResponse(data)


@login_required()
def get_posts(request, name):
    member = request.member
    if member.is_authenticated:
        member = request.member
        course = Course.objects.filter().first()

        if course is not None:
            posts = Post.objects.filter(Q(content__icontains=name) | Q(title__icontains=name)).all()
            file_types = FileType.objects.all()
            context = {}
            context['member'] = member
            context['course'] = course
            context['courses'] = member.courses.all()
            context['course'] = course
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Member/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")


@login_required
def jira(request):
    member = request.member
    jira_tickets = Jira.objects.all()
    jira_all = {}
    for s in Status.objects.all():
        jira_all[s] = Jira.objects.filter(status = s)

    context = { 'member':member,'jira_tickets':jira_tickets,'jira_all':jira_all}

    return render(request, 'Member/jira_dashboard.html',context)


@login_required
def jira_create(request):
    context = {}
    member = request.member
    jira_tickets = Jira.objects.all()
    context['member'] = member
    context['courses'] = member.courses.all()
    context['jira_tickets'] = jira_tickets
    if request.method == 'POST':
        jira_create_form = JiraCreateForm(request.POST, request.FILES)
        if jira_create_form.is_valid():
            files = jira_create_form.save_files(request.FILES.getlist('files'))
            if len(files) == 0 and 'files' in request.session:
                files = File.objects.filter(id__in=request.session['files'])
                del request.session['files']

            jira = jira_create_form.save(commit=False)
            jira.save()
            for f in files:
                jira.files.add(f)
            jira.save()
            context['jira_create_form'] = jira_create_form
            return render(request, 'Member/jira_create.html', context)
        else:
            print(jira_create_form.errors)
    else:
        jira_create_form = JiraCreateForm()

    context['jira_create_form'] = jira_create_form
    jira_create_form.reporter = request.member
    return render(request, 'Member/jira_create.html', context)


@login_required
def jira_view(request,jira_id):
    context = {}
    jira_tickets = Jira.objects.all()
    jira_ticket = Jira.objects.filter(id=jira_id).get()
    member = request.member
    context['member'] = member
    context['courses'] = member.courses.all()
    course_members = jira_ticket.course.member_courses.all()
    context['assign_to'] = list(filter(lambda x: (x.email != member.email), course_members))
    context['jira_tickets'] = jira_tickets
    context['jira'] = jira_ticket
    context['all_status'] = Status.objects.all()
    context['comment_form'] = CommentCreateForm()

    if request.method == "POST":
        comment_create_form = CommentCreateForm(request.POST, request.FILES)
        if comment_create_form.is_valid():
            files = request.FILES.getlist('files')
            if len(files) == 0 and 'files' in request.session:
                files = File.objects.filter(id__in=request.session['files'])
                del request.session['files']
            comment = comment_create_form.save(commit=False)
            comment.user = request.member
            comment.save()
            for f in files:
                comment.files.add(f)
            comment.save()
            jira_ticket.comments.add(comment)
            jira_ticket.save()
        else:
            print("form not valid")
    else:
        jira_tickets = Jira.objects.all()
        jira_ticket = Jira.objects.filter(id=jira_id).get()
        member = request.member
        context['member'] = member
        context['jira_tickets'] = jira_tickets
        context['jira'] = jira_ticket
        context['comment_form'] = CommentCreateForm()

    return render(request, 'Member/jira_view.html', context)


@login_required
def jira_edit(request,jira_id):
    context = {}
    jira_tickets = Jira.objects.all()
    jira_ticket = Jira.objects.filter(id=jira_id).get()
    member = request.member
    context['member'] = member
    context['jira_tickets'] = jira_tickets
    context['jira'] = jira_ticket
    context['files'] = jira_ticket.files
    if request.method == 'POST':
        jira_create_form = JiraCreateForm(request.POST, request.FILES,instance=jira_ticket)
        if jira_create_form.is_valid():
            files = jira_create_form.save_files(request.FILES.getlist('files'))
            jira = jira_create_form.save(commit=False)
            jira.save()
            for f in files:
                jira.files.add(f)
            jira.save()
            context['jira_create_form'] = jira_create_form
            return render(request, 'Member/jira_create.html', context)
        else:
            print(jira_create_form.errors)
    else:
        context['jira_create_form'] = JiraCreateForm(instance=jira_ticket)
    return render(request, 'Member/jira_create.html', context)


@login_required
def jira_link(request,jira_id):
    context = {}
    jira_tickets = Jira.objects.all()
    jira_ticket = Jira.objects.filter(id=jira_id).get()
    member = request.member
    context['member'] = member
    context['jira_tickets'] = jira_tickets
    context['jira'] = jira_ticket
    context['files'] = jira_ticket.files
    if request.method == 'POST':
        jira_link_form = LinkJiraForm(request.POST, request.FILES,instance=jira_ticket,request=request)
        if jira_link_form.is_valid():
            jira_link_to = Jira.objects.filter(id=request.POST['links']).first()
            jira_ticket.links.add(jira_link_to)
            jira_link_to.links.add(jira_ticket)
            jira_ticket.save()
            jira_link_to.save()
            return redirect('/jira/', context)
        else:
            context['jira_link_form'] = LinkJiraForm(request=request)
            print("Member:", member)
            return render(request, 'Member/jira_link.html', context)
    else:
        context['jira_link_form'] = LinkJiraForm(request=request,instance=jira_ticket)
        print("Member:", member)
        return render(request, 'Member/jira_link.html', context)


@login_required
@csrf_exempt
def files_upload(request):
    context = {}
    member = request.member
    context['member'] = member
    if request.method == 'POST':
        files_upload_form = FileCreateForm(request.POST, request.FILES)
        if files_upload_form.is_valid():
            file = files_upload_form.save(commit=False)
            file.user = member
            file.name = file.file.name
            file.save()
            if 'files' in request.session:
                request.session['files'].append(file.id)
            else:
                files = [file.id]
                request.session['files'] = files

            return HttpResponse({"file.id":file.id,"status":"success"})
        else:
            print(files_upload_form.errors)
            return HttpResponse({"file.id":"","status":"failed"})


@login_required
@csrf_exempt
def files_delete(request):
    context = {}
    member = request.member
    context['member'] = member
    if request.method == 'POST':
        file_id = request.POST['id']
        file = File.objects.filter(id=file_id).get()
        if file:
            if 'files' in request.session:
                files = request.session['files']
                files.remove(file.id)
                request.session['files'] = files

            file.delete()
            return HttpResponse({"file.id":file.id,"status":"success"})
        else:
            print("error deleting")
            return HttpResponse({"file.id":"","status":"failed"})


@login_required()
@csrf_exempt
def update_jira_status(request):
    if request.method=='POST':
        jira_id = request.POST['jira_id']
        new_status = request.POST['status']
        jira = Jira.objects.filter(id=jira_id).get()
        status = Status.objects.filter(tag=new_status).first()
        if jira and status:
            jira.status=status
            jira.save()
            return HttpResponse({'success':True},200)
        else:
            return HttpResponse({'success':False},500)

    else:
        return redirect("/")


@login_required()
@csrf_exempt
def update_jira_assignee(request):
    if request.method=='POST':
        jira_id = request.POST['jira_id']
        new_assignee = request.POST['assignee']
        jira = Jira.objects.filter(id=jira_id).get()
        assignee = Member.objects.filter(id=new_assignee).first()
        if jira and assignee:
            jira.assignee = assignee
            jira.save()
            return HttpResponse({'success':True},200)
        else:
            return HttpResponse({'success':False},500)
    else:
        return redirect("/")