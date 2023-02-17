## Overview

Pwnquery is a Django API that is used for querying a database for credentials from various databreaches (described in more detail below). Additionally, I have included a companion Python script, `pwnquery.py`, used for querying the API. It is possible to interact with the API via web front end and cUrl as well with token-based auth.  

Most of the work that went in to this is based off research in the article listed below (shoutout to Kevin Dick). 

https://threat.tevora.com/diy-leaked-credential/

Another shoutout to @t1d3nio and @pugbrain for the blood sweat and tears endured putting this project together and implementing 3 different working versions. (lol)

## What Next and Steps to get this Running

It is a well written blog post; however, there were a couple gaps with getting the Django REST API stood up with regard to `urls.py` and `settings.py`. 

1. Setup your postgres db and build schema following blog instructions

2. Cleaning up the breach dump data

- I recommend cleaning the data before importing. This includes shredding out the garbage data (anything except email:password format), stripping large amounts of not useful russian accounts, and deduping.

```bash
cat breachfile.txt |  dos2unix -f| grep -a -P -o "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}+[\:\;][A-Za-z0-9\!@#$%^&*()_+-={}[ ;:\'\",<>\.\///?]*$"  | grep -v \.ru > parsed.txt
```
- sort -u parsed.txt > deduped_parsed.txt 

3. Ingesting data into database

While the ingestor used in the blog referenced above uses a custom Python script, I found that Postgres' COPY fucntionality is actually quicker. Bonus, use PV to watch the progress bar as this part takes an extensive amount of time: 

```bash
pv dumpdatacleaned.txt| psql -d databasename -c "COPY tablename from STDIN delimiter ':';"
```

4. Adding indexes to database table columns

Adding indexes: 
```CREATE INDEX domain ON public.tablename USING btree (domain);
CREATE INDEX username_password ON public.tablename USING btree (username, password);
CREATE INDEX password ON public.tablename USING btree (password);
CREATE INDEX username ON public.tablename USING btree (username);
```

Removing Indexes: 
```drop index username_password;
drop index password;
drop index domain;
drop index username;
```
When adding breach data to the database in the future, it may be necessary to delete the indexes, upload the new data, then reapply the indexes. Uploading data to an indexed database is very time consuming depending on your level of optimization and newbness in db administration (my newbness is 10/10). 

Other miscellaneous Postgres commands that are useful: 
```
#switch user to postgres and connect to db using psql
su postgres
psql dbname

#list databses
\l

#connect to database 
\c dbname

#list tables 
\dt

#list constraints and indexes on db table
\d+ tablename
```

5. Implement token-based authentication 

- Edit `settings.py` and add the following within `REST_FRAMEWORK`: 
```
REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
         'rest_framework.authentication.TokenAuthentication', 
     ],
     'DEFAULT_PERMISSION_CLASSES': (
         'rest_framework.permissions.IsAuthenticated',
    ),
}
```
- Edit `views.py` and add `,isAuthenticated` in the "#<--" noted areas listed below 
```python
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated # <-- don't forget this import 
from .models import userProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import userProfileSerializer

# Create your views here.

class UserProfileListCreateView(ListCreateAPIView):
    permission_classes = (isAuthenticated,) #<-- add here 
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (isAuthenticated,) # <-- add here
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
```

- Update `settings.py` to include token auth in installed apps (noted by "#<-- here")

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'leakedpasswords',
    'rest_framework.authtoken', #<-- here
    'rest_auth',
    'templates',
    'djoser',
    'rest_framework_simplejwt'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  #<-- here
    ],
}
```
- Next, migrate the db to instantiate the auth database, create user, create token, and start the server 

```python
python3.6 manage.py migrate
python3.6 manage.py createsuperuser --username fr4nk3nst1ner --email myemail@yolo.com
python3.6 manage.py drf_create_token fr4nk3nst1ner
python3.6 manage.py runserver interface_ip:port
```
 
6. Other things to note

- In a perfect world, you should now be able to query the API
- Use Python3.6 with Django==2.2 or above. This implementation has requirements not compatible with Django 1.
- I had template issues and had to add "django_filters" to INSTALLED_APPS within `settings.py`
- Additionally, I have included a python script for querying the API (`pwnquery.py`) that supports sub args for querying both API endpoints (breach compilation and Facebook breach data). 

## Breach Compilation Descriptions

1. Compilation of Collections #1-5
2. COMB
3. Ducks Unlimited 
4. All data is uniqued and contains no hashes but rather cracked, plaintext passwords

Note: includes hashes that me and some buddies have cracked in a Postgres db that is uniqued and indexed. 
Usefuleness: helps with username enumeration and included plaintext passwords that may or may not be valid anywhere else (for pen tests purposes only of course). 

## Facebook dump description

Facebook breach data that includes names, addresses, employers, and phone numbers (the latter 3 if they included that in their profiles).

## Pwnquery Usage

```bash
Examples:
 python3 query.py function1 --domain targetname.com
 python3 query.py function2 --company target company name

positional arguments:
  function1             Search breach dump data.
  function2             This searches the function2 breach dump.

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Breach data domain to search for. Only use with function1 (e.g., "./query.py function1 -d targetname.com"
  -c COMPANY, --company COMPANY
                        Company name to search for function2 Breach. Only use with function2 (e.g., "./query.py function2 -c target company name"
```
