# LocMessServer
Server for CMU

```
virtualenv .env
git clone ...this repo...
source .env/bin/activate
pip install -r requirements.txt
cd LocMessServer
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Server is run on *8000* not *8080*
