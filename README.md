# StackOverFlowLite-API [![Build Status](https://travis-ci.org/antonnifo/StackOverflow-lite.svg?branch=develop)](https://travis-ci.org/antonnifo/StackOverflow-lite) [![Maintainability](https://api.codeclimate.com/v1/badges/5c190be007229b41d114/maintainability)](https://codeclimate.com/github/antonnifo/StackOverflow-lite/maintainability) [![Coverage Status](https://coveralls.io/repos/github/antonnifo/StackOverflow-lite/badge.svg?branch=develop)](https://coveralls.io/github/antonnifo/StackOverflow-lite?branch=develop)

### Tech/framework used  
python 3.6.7 and [Flask](http://flask.pocoo.org/docs/dev/)   
### PROJECT OVERVIEW  
A Q and A Platform  
## Installation and Deployment. 
### Getting Started 
> git clone https://github.com/antonnifo/StackOverflow-lite.git 
#### Create a virtual environment and activate it 
> python3 - m venv env  
> source .env  
#### Install all the dependencies using the command
> pip install -r requirements.txt
## contents of `.env`   
```  
source venv/bin/activate  

export FLASK_ENV="development"   
export FLASK_CONFIG="development"  
export DATABASE_URL="dbname='your-database' host='localhost' port='5432' user='your-username' password='your-password'"   
export DATABASE_URL_TEST="dbname='your-test-database' host='localhost' port='5432' user='your-username' password='your-password'"   
export SECRET_KEY="secret-key-goes-here"
``` 
#### How to Run the App
 ```   
source .env
> flask run   
```

#### Test the application  
Tests are to be run with pytest or py.test on the root folder
Set FLASK_CONFIG to testing on your .env file before running tests   

`source .env
pytest --cov=app/` 
 ### Documentation  
 [Postman Documentation](https://web.postman.co/collections/5023026-a96230fc-692f-48da-91f1-e0d44d764d2c?workspace=4d54ae63-9d4b-4731-82b0-90598d247bfc#1d56fb24-901e-4d08-857a-d00d47f50894 "My postman docs link") 
 ### Hosting link
 [Heroko] (https://wakali-stack.herokuapp.com/)
