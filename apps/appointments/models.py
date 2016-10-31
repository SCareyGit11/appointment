from __future__ import unicode_literals

from django.db import models

import re



email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')

class Validator(models.Manager):
	

########## ARE ALL FIELDS COMPLETED?  ###########
	def checkfield(self, first_name, last_name, email, password, confirm):
		error = True
		if len(first_name) > 1 and len(last_name) > 1 and len(email) > 1 and len(password) > 1 and len(confirm) > 1:
			error = False
		return error

######### ARE THE NAMES ONLY LETTERS? ########
	def checkname(self, first_name):
		error = True
		if name_regex.match(first_name):
			error = False
		return error

	def checkname(self, last_name):
		error = True
		if name_regex.match(last_name):
			error = False
		return error


######## IS EMAIL IN VALID FORMAT? ###############
	def checkemail(self, email):
		print "check register method in models.py"
		error = True
		if email_regex.match(email):
			error = False
			
		return error



####### IS PASSWORD AT LEAST 8 CHARACTERS AND MATCH W/ CONFIRM? ###
	def checkpassword(self, password, confirm):
		error = True
		if len(password) > 7 and password == confirm:
			error = False
		return error

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	pw = models.CharField(max_length=256)
	'''dob = models.DateField(auto_now=False)'''
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = Validator()


class Appointment(models.Model):
	task = models.CharField(max_length=45)
	date = models.DateTimeField(auto_now=False)
	user = models.ForeignKey(User)

	DONE = 'DONE'
	PENDING = 'PENDING'
	MISSED = 'MISSED'
	STATUS_CHOICES = (
		(DONE, 'DONE'),
		(PENDING, 'PENDING'),
		(MISSED, 'MISSED')
	)
	status = models.CharField(
		max_length=7,
		choices=STATUS_CHOICES,
		default=PENDING
	)
	

	'''class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )'''