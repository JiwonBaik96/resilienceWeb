from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate #add this
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this

import mimetypes
import os
from django.http.response import HttpResponse

# Create your views here.

def nws(request):
	return render(request, 'main/nws.html', {})
def map(request):
    return render(request, 'main/map.html', {})

def data(request):
    return render(request, 'main/data.html', {})



@login_required
def download_file(request, filename):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # Define the full file path
    filepath = BASE_DIR + '/static/main/images/' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:map")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("main:map")