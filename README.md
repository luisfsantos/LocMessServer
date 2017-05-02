# LocMessServer
Server for CMU

```
virtualenv .env
source .env/bin/activate

git clone ...this repo...


cd LocMessServer
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver localhost:8080
```

Server is run on __8000__ not __8080__ by default

### For tests run:
```
python manage.py test
```
