# financestore

This project was created for an online store of shares.

Description

Our Django API describes the service of the Share Trading market, where users will be able to view the shares, sort them by categories/subcategories, companies, etc. Users should also be able to order some type of stock, and leave their own credentials(phone, name). Once the User orders the share, the Order will be created, and a random Broker will be assigned to it. Brokers are managing the orders and increasing their own rating(amount_of_trades) by selling shares.

Django consists of 2 applications: core and api.
Models are these: Base(abstract model for inheritance), Category, SubCategory, Company, Share, Order, Broker. There are 4 model Managers; 1 for Brokers, 3 for Orders. Broker Manager filtrates those Broker objects that have 0 amount_of_trades and is called NeedToFire. Orders Managers are used to filter the orders by status(complete, declined, in_progress).
Serializers are as follows, validation rules are applied to some of them. Some Serializers are inheriting  from BaseSerializer that serializes the name and id of the object. Logging is being applied to serializer validations(errors are being logged).
Views have FBV, CBV, ViewSets, FileUploads.

obtain_jwt_token is being used to log in the user.

Class Diagram: 
![photo_2021-05-15 10 21 39](https://user-images.githubusercontent.com/47467224/118347772-91f5dc00-b567-11eb-98be-9a98d264c9ee.jpeg)
