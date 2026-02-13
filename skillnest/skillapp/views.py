from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact, Profile
from django.core.management import call_command
from io import StringIO
import os

def index(request):
    return render(request,"index.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        contact=Contact(name=name,email=email,message=message)
        contact.save()
        return render(request,"contact.html",{'message':'Message Sent Successfully'})
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request,"login.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('confirm_password')

        if pass1!=pass2:
            messages.error(request,"Passwords do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already registered")
            return redirect('signup')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        
        # Create Profile
        profile=Profile(user=myuser, bio="Student at SkillNest")
        profile.save()

        messages.success(request,"Your Account has been created successfully")
        return redirect('login')

    return render(request,"signup.html")

def students(request):
    profiles = Profile.objects.all()
    return render(request,"students.html",{'profiles':profiles})

@login_required(login_url='login')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.branch = request.POST.get('branch')
        profile.year = request.POST.get('year')
        profile.bio = request.POST.get('bio')
        
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
            
        profile.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('profile')
    return render(request, "profile.html", {'profile': profile})

def logout_user(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')

def init_admin(request):
    from django.conf import settings
    out = StringIO()
    
    db_engine = settings.DATABASES['default']['ENGINE']
    db_url_raw = os.getenv('DATABASE_URL', '')
    
    # Cleanup logic (matching settings.py)
    cleaned_url = db_url_raw.strip()
    if cleaned_url.startswith('psql '):
        cleaned_url = cleaned_url[5:].strip()
    cleaned_url = cleaned_url.strip("'").strip('"').strip()

    diagnostics = [
        f"Active Database Engine: {db_engine}",
        f"DATABASE_URL detected: {'Yes' if db_url_raw else 'No'}",
    ]
    
    if db_url_raw:
        diagnostics.append(f"Original URL starts with: {db_url_raw[:15]}...")
        diagnostics.append(f"Cleaned URL starts with: {cleaned_url[:15]}...")
        
        if db_url_raw != cleaned_url:
            diagnostics.append("<b>NOTICE:</b> Your URL was automatically cleaned. It contained extra words like 'psql' or quotes.")

    try:
        call_command('migrate', interactive=False, stdout=out)
        call_command('create_admin', stdout=out)
        status = "Admin Initialization Complete!"
    except Exception as e:
        status = f"Error: {e}"
        if 'readonly' in str(e).lower():
            diagnostics.append("CRITICAL: Still using SQLite. Your cleaned URL is likely still invalid.")

    response_html = f"<h2>{status}</h2>"
    response_html += "<h3>Diagnostics:</h3><ul>"
    for d in diagnostics:
        response_html += f"<li>{d}</li>"
    response_html += "</ul><h3>Logs:</h3><pre>" + out.getvalue() + "</pre>"
    response_html += "<p><b>Next Step:</b> Try logging in now at /admin/ with 'admin' and 'admin123'.</p>"
    
    return HttpResponse(response_html)
