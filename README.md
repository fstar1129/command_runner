## Command Runner website contains:
* Run command on background using celery task on Django app



## Usage :
Input command and get the link for result
### Run project by :

``` python

# change database connection information in settings.py DATABASES default values with your info then run 
1. pip install -r requirements.txt

2. install redis

3. run redis-service

4. run redis-cli

5. celery worker -A scan --loglevel=debug --concurrency=4

6. python manage.py migrate

7. python manage.py runserver

```

That's it.

## Done :

Now the project is running at `http://localhost:8000` and your routes is:


| Route                                                      | HTTP Method 	   | Description                           	      |
|:-----------------------------------------------------------|:----------------|:---------------------------------------------|
| {host}       	                                             | GET       	     | Home page                                    |


For detailed explanation on how project work, read the [Django Docs](https://docs.djangoproject.com/en/2.1/)
