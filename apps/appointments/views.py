from django.shortcuts import render, redirect
from .models import User, Appointment
from django.contrib import messages
import bcrypt, hashlib, datetime

# Create your views here.
def index(request):
	
	return render(request, 'appointments/index.html')


################ REGISTRATION ####################################

def register(request):
	if request.method == 'POST':
		
		
###### RETRIEVE REGISTRATION FORM DATA##
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		
		
		confirm = request.POST['confirm']
		'''dob = request.POST['dob']'''
		

####### CHECK ALL FIELDS COMPLETED ##		
		if User.objects.checkfield(first_name, last_name, email, password, confirm):
			messages.error(request, 'All fields must be Completed', extra_tags='field')

###### CHECK NAMES CONTAIN ONLY LETTERS ##
		elif User.objects.checkname(first_name):
			messages.error(request, 'Names can Only contain Letters', extra_tags='first')

		elif User.objects.checkname(last_name):
			messages.error(request, 'Names can Only contain Letters', extra_tags='last')

###### CHECK EMAIL FORMAT #######
		elif User.objects.checkemail(email):
			messages.error(request, 'Email is Not Valid', extra_tags='email')


##### CHECK PASSWORD AT LEAST 8 CHARACTERS AND MATCHES WITH CONFIRM PASSWORD
		elif User.objects.checkpassword(password, confirm):
			messages.error(request, 'Password must be at least 8 characters and Match Confirm Password', extra_tags='password')
		
			return redirect('/')


######### IF ALL FIELDS ARE VALID ############################

		else:
			'''hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()'''
			
			
			print password
			pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			print pw
			user = User.objects.create(first_name=first_name, last_name=last_name, email=email, pw=pw)
			print user.first_name
			request.session['id'] = user.id
			
			return redirect('/welcome')

	return redirect('/')




#####################LOGIN#########################################

def login(request):

## Retrieve Form Data 
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

## Check for existing User ##
		try:
			user = User.objects.get(email=email)
		
		## If existing User, then check hashed password ##
		
		 
			if bcrypt.hashpw(password.encode(), user.pw.encode()) == user.pw:
				request.session['id'] = user.id
				return redirect('/welcome')

			else:	
				messages.error(request, 'Incorrect Password', extra_tags='loginpwd')
				return redirect('/')
		except:
			messages.error(request, 'Email Not Found', extra_tags='logine')
			return redirect('/')


	else:
		
		return redirect('/')


############## WELCOME PAGE ###################################3

def welcome(request):
	user = User.objects.get(id=request.session['id'])
	print user.first_name

	appointments = Appointment.objects.filter(user_id=request.session['id'])

	context = {
			"users" : user,
			"appointments" : appointments,
			"now" : datetime.datetime.now()
			}


	return render(request, 'appointments/welcome.html', context)


def add(request):

	if request.method == 'POST':
		Appointment.objects.create(task=request.POST['task'], date=request.POST['date'], user_id=request.session['id'])
		return redirect('/welcome')

	else:
		return redirect('/')


def delete(request, id):
	Appointment.objects.get(id=id).delete()
	return redirect('/welcome')

def logout(request):
    request.session.pop('id')
    return redirect('/')


######################## EDIT PAGE ##############################

def edit(request, id):
	context = {
	"id" : id
	}
	return render(request, 'appointments/edit.html', context)

def update(request, id):
	##RETRIEVE FORM DATA##
	if request.method == 'POST':
		task = request.POST['task']
		date = request.POST['date']
		status = request.POST['status']

	##SAVE UPDATE##
		appointment = Appointment.objects.get(id=id)
		appointment.task = task
		appointment.date = date
		appointment.status = status
		appointment.save()

		return redirect('/welcome')

	else:
		return render(request, 'appointments/index.html')





