# Application for spending management

## Description

The main goal of the application was to learn/organize my knowledge about software design, flask framework,
sqlalchemy and docker-compose tool. Frontend issues were not taken care of as they were not a goal of this project. 

The application is designed for saving  and analyzing user's spendings.

## 1. Running application on docker

- download spending-app directory and run the following commmands:

cd spending-app/docker-compose

sudo docker-compose build
sudo docker-compose up -d

- application is running on localhost, port 5000
- to check docker ip address run 

sudo docker logs docker-compose_spending_app_1 -f


## 2. Running application locally 

Note: running the application locally needs postgres instance on docker. Commands from point number 1 must be run first. Required libraries are in requirements.txt file. The application running locally is on port 5001. 

## 3. Usage of the application

The navigation bar has three options. "Add new spending" option allows for adding a new spending as well as adding new category/removing existing category. There are two kinds of categories: the main category (e.g. food) and the subcategory that is more precise (e.g. fruits). A user must decide what kind of category he is adding.

Adding a spending
dodać screeny

## 4. Running tests

Go to spending-app/tests. Unittests are run with command "python -m unittest discover -v"

# Conclusion

