from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
# Create your views here.
def home(request):
	records = Record.objects.all()

	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In...")
			return redirect('home')
		else:
			messages.success(request, "Could Not Verify Credentials, Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records': records})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password1"]
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registerd")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form': form})
	return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
	if request.user.is_authenticated:
		record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'record': record})
	else:
		messages.success(request, "You Must Be Logged In To View The Record...")
		return redirect('home')


def delete_record(request, pk):
	if request.user.is_authenticated:
		to_delete = Record.objects.get(id=pk)
		to_delete.delete()
		messages.success(request, f"Record deleted: {to_delete}" )
		return redirect('home')
	else:
		messages.success(request, f"You Must Be Logged In To Delete The Record..." )
		return redirect('home')
	

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				new_user = form.save()
				messages.success(request, f"You Have Successfully Added: {new_user}")
				return redirect('home')
		return render(request, 'add_record.html', {'form': form})
	else:
		messages.success(request, f"You Must Be Logged In To Add A Record..." )
		return redirect('home')
	
def update_record(request, pk):
	if request.user.is_authenticated:
		to_update = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=to_update)
		if form.is_valid():
			form.save()
			messages.success(request, f"Record updated: {to_update}" )
			return redirect('home')
		else:
			return render(request, 'update_record.html', {'form': form})
	else:
		messages.success(request, f"You Must Be Logged In To Update The Record..." )
		return redirect('home')