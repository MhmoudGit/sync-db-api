## Models
1 - Categories:

    - id
    - name [Animals - Accessories - lost]
    - list[Items] -Relation

2 - Items:

    - id
    - category_id -Relation
    - title
    - description
    - owner_name
    - phone_number
    - location

3 - Users:

    - id
    - username
    - password
    - role[Seller-Buyer]
    - name
    - phone
    - location


## Routes
1 - Auth:

    - register
    - login
    - logout

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