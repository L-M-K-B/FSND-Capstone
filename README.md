# FSND-Capstone
## Introduction
This is the final project of my fullstack developer nano degree. I used the following technologies:
 
    - Coding in Python 3
    - Relational database architecture (PostgreSQL)
    - Modeling data objects with SQLAlchemy
    - Internet protocols and communication
    - Developing a Flask API
    - Testing Flask applications
    - Authentication and access management with Auth0 and Flask
    - Role-Based Access Control (RBAC)
    - Deploying the application with Heroku

## Getting started
Please install the following dependencies:
### Python 3
Follow the instructions in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
### Other dependencies
In this folder you can find a `requirements.txt` which you can run with the following command:
```
pip3 install -r requirements.txt
```
### Database setup `(????????????????????)`
## Testing
To run the tests, run
```
dropdb capstone-test
createdb capstone-test
python test_app.py
```
# API Endpoints
## GET: /movies
- fetches a dictionary of movies:
    - keys: ids of movies
    - values: string, name of movie
- request arguments: None
- returns a json file:
```
{
    'success': true,
    'movies': 
        {
            1 : 'Hidden Figures'
        }
}
```
## GET: /actresses
- fetches a list of objects containing all actresses
- each actress entry is formatted as a dictionary containing the following keys: 
    - birth_date (datetime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- request arguments: None
- returns a json file:
```
{
    'success': true,
    'actresses': 
        [
            {
                'birth_date': 'Fri, 11 Sep 1970 00:00:00 GMT',
                'gender': 'female',
                'id': 1,
                'movies': [1],
                'name': 'Taraji P Henson'
            }
        ]
}
```
## POST: /actress
- creates a new actress entry
- request arguments: 
    - birth_date (DateTime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- returns a json file:
```
{
    'success': true,
    'created': <actress_id (int)>
}
```
## POST: /movie
- creates a new movie entry
- request arguments: 
    - id (int)
    - title (str)
    - release_date (DateTime)
    - country (str)
- returns a json file:
```
{
    'success': true,
    'created': <movie_id (int)>
}
```
## DELETE: /actress/<actress_id>
- deletes a single actress
- request arguments: 
    - id of actress
- returns a json file:
```
{
    'success': true,
    'deleted': <actress_id (int)>
}
```
## PATCH: /actress/<actress_id>
- modifies an actress entry
- request arguments (changes are not necessarily applied to all arguments): 
    - birth_date (DateTime)
    - gender (str)
    - id (int)
    - movies (list of movie ids)
    - name (str)
- returns a json file:
```
{
    'success': true,
    'actress': 
        [
            {
                'birth_date': 'Fri, 11 Sep 1970 00:00:00 GMT',
                'gender': 'female',
                'id': 1,
                'movies': [1],
                'name': 'Taraji P Henson'
            }
        ]
}
```