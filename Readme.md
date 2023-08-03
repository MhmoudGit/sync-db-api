## To run the project
1 - pip install -r requirements.txt
2 - set the .env file to your local database
3 - uvicorn api.main:app --reload


## Setup and Required libararies
    - Fastapi[ALL]
    - psycopg2 -> a driver for postgresql
    - sqlalchemy -> orm
    - pyjwt -> for jwt 
    - passlib[bcrypt] -> for hashing passwords

## Database Relations 
1 - one to one 
2 - one to many
3 - many to many

## primary key and forign key
A primary key is used to ensure data in the specific column is unique. A foreign key is a column or group of columns in a relational database table that provides a link between data in two tables

## Models
1 - Users:

    - id
    - username
    - password
    - role[Seller-Buyer]
    - name
    - phone
    - location

2 - Categories:

    - id
    - name [Animals - Accessories - lost]
    - list[Items] -Relation

3 - Items:

    - id
    - image
    - category_id -Relation forign key
    - title
    - description
    - owner_name
    - phone_number
    - location




## Routes
1 - Auth:

    - register
    - login

2 - Categories:

    - get all
    - get by id 
    - post  [Seller]
    - put   [Seller]
    - delete    [Seller]

3 - Items:

    - get by category
    - get by id 
    - post  [Seller]
    - put   [Seller]
    - delete    [Seller]