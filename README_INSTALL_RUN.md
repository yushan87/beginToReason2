Install django
Install django_ace

python manage.py makemigrations BeginToReason
python manage.py migrate

python manage.py loaddata initialDB.json

python manage.py runserver

In an internet browser go to http://127.0.0.1:8000/admin/BeginToReason/

For ace, I just moves the js file from the old project to the folder in django_ace that contained the rest of the languge files. That method did not work, but I did not want to spend to much time working on it.

The Poll app is part of the django tutorial
