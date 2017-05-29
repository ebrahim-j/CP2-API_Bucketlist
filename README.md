[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8a1fa4c8931d440d97bdb7711c502f88)](https://www.codacy.com/app/ebrahim-j/CP2-API_Bucketlist?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ebrahim-j/CP2-API_Bucketlist&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/8a1fa4c8931d440d97bdb7711c502f88)](https://www.codacy.com/app/ebrahim-j/CP2-API_Bucketlist?utm_source=github.com&utm_medium=referral&utm_content=ebrahim-j/CP2-API_Bucketlist&utm_campaign=Badge_Coverage)
# CP2-API_Bucketlist
According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying. This app creates an API for an online Bucket List service using Flask.


#### GETTING STARTED:

1. Clone Repo:

    ```
    $ git clone https://github.com/ebrahim-j/CP2-API_Bucketlist.git
    ```
2. Navigate to local directory.

    ```
    $ cd CP2-BucketList_API
    ```
3. Create a virtualenvironment(assuming you have virtualenvwrapper).

    ```
    $ mkvirtualenv -p python3 venv
    ```
4. Install all app requirements

    ```
    $ pip install -r requirements.txt
    ```

5. Create the database and run migrations

    ```
    $ python manage.py create_db [name]
    ```

**To run migrations**:
   `$ python manage.py db init`

   `$ python manage.py db migrate`

   `$ python manage.py db upgrade`

Don't forget to set your APP_SETTINGS to set your app configurations, you can choose from:
    - development
    - testing
    - production
    - staging
    #e.g.
    `$ export APP_SETTINGS='development`

 6. All done! Now, start your server by running `python manage.py runserver`. For best experience, use a GUI platform like [postman](https://www.getpostman.com/) to make requests to the api.

### Endpoints

Here is a list of all the endpoints in bucketlist app.

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
POST /api/v1/auth/login |Logs a user in | PUBLIC
POST /api/v1/auth/register | Registers a user | PUBLIC
POST /api/v1/bucketlists/ | Creates a new bucket list | PRIVATE
GET /api/v1/bucketlists/ | Lists all created bucket lists | PRIVATE
GET /api/v1/bucketlists/id | Gets a single bucket list with the suppled id | PRIVATE
PUT /api/v1/bucketlists/id | Updates bucket list with the suppled id | PRIVATE
DELETE /api/v1/bucketlists/id | Deletes bucket list with the suppled id | PRIVATE
POST /api/v1/bucketlists/id/items/ | Creates a new item in bucket list | PRIVATE
PUT /api/v1/bucketlists/id/items/item_id | Updates a bucket list item | PRIVATE
DELETE /api/v1/bucketlists/id/items/item_id | Deletes an item in a bucket list | PRIVATE

### Features:
* Search by name
* Pagination
* Token based authentication
### Searching

It is possible to search bucketlists using the parameter `q` in the GET request. 
Example:

`GET http://localhost:/bucketlists?q=Spirituality`

This request will return all bucketlists with name similar to `Spirituality`.

### Pagination

It is possible to limit the count of bucketlist data displayed using the parameter `limit` in the GET request. 

Example:

`GET http://localhost:/api/v1/bucketlists?limit=5`

It is also possible to set the record we would like to start viewing from.

Example:

`GET http://localhost:/api/v1/bucketlists?page=5`

### Sample GET response
After a successful resgistration and login, you will receive an athentication token. Pass this token in your request header.
Below is a sample of a GET request for bucketlist

```
{
  "id": 7,
  "name": "Memorable Experiences",
  "items": [],
  "date_created": "Tue, 23 May 2017 14:48:08 GMT",
  "date_modified": "Tue, 23 May 2017 14:48:08 GMT",
  "created_by": "1"
}

```

### Testing
The application tests are based on python’s unit testing framework unittest.
To run tests with nose, run `nosetests` or `python manage.py test`
