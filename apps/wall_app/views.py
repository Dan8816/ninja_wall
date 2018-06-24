from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.wall_app.models import User, UserManager, Message, Comment
from django.contrib import messages
import re, bcrypt


def index(request):
    return render(request, 'wall_temps/index.html')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
            print(errors)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['confirmpassword'].encode(), bcrypt.gensalt())
        )
        print("successfully created users")
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/confirm')

def confirm(request):
    if 'email' not in request.session:
        return redirect('/')
    context = {
        "users" : User.objects.all(),
    }
    return render(request, "wall_temps/confirm.html", context)

def login(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print('email and password matches, successful login')
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            return redirect('/success')
        else:
            print("failed password")
            return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "messages" : Message.objects.order_by("created_at")[:2],
        "users" : User.objects.all(),
        "comments" : Comment.objects.all()
    }
    print(request.session['user_id'])
    return render(request, "wall_temps/success.html", context)

def populars(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "messages" : Message.objects.order_by("like_count")[:3],
        "users" : User.objects.all(),
        "comments" : Comment.objects.all()
    }
    print(request.session['user_id'])
    return render(request, "wall_temps/populars.html", context)

def logout(request):
    request.session.clear()    
    return redirect('/')

def create_msg(request):
    Message.objects.create(msg=request.POST["msg"], user_id=request.session['user_id'])
    return redirect('/success')

def like(request, id):
    this_user = User.objects.get(id=request.POST['user_id'])
    this_msg = Message.objects.get(id=id)
    this_msg.likes.add(this_user)
    this_msg.like_count += 1
    this_msg.save()
    return redirect('/success')

def del_msg(request, id):
    d = Message.objects.get(id=id)
    if int(request.session['user_id']) == d.user_id:
        d.delete()
        return redirect('/success')
    else:
        print("You did not post this")
        return redirect('/success')

def create_cmnt(request):
    this_message = Message.objects.get(id=request.POST['id'])##later found this was not needed, below could have used msg_id = request.POST['id]
    Comment.objects.create(comnt=request.POST["cmnt"], msg_id=this_message.id,user_id=request.session['user_id'])
    return redirect('/success')

def del_comnt(request, id):
    d = Comment.objects.get(id=id)
    if int(request.session['user_id']) == d.user_id:
        d.delete()
        return redirect('/success')
    else:
        print("You did not make this comment")
        return redirect('/success')

