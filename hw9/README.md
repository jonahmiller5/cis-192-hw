DEPENDENCIES

	os
	flask
		Flask, flash, request, redirect, render_template
	flask_mail
		Mail, Message
	werkzeug.utils
		secure_filename
	re
	requests


SETUP

INSTALLATION
	
	instantiate and enter a virtual environment
	pip install flask
	pip install flask-mail
	pip install requests

DIRECTORY STRUCTURE

	>static
		redir.png
	>templates
		email.html
		home.html
		texter.html
	>uploads
		>email
		>sms

EXECUTION

IN COMMAND LINE
	
	cd path/to/flask/app
	export FLASK_APP=hw9.py; flask run
	
IN GOOGLE CROME

	http://localhost:5000/
