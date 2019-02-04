from werkzeug.security import generate_password_hash

password = generate_password_hash("hello123")
test_user = {
        "user_name":"mzito",
        "first_name": "john",
        "last_name": "doe",
        "email": "johndoe@example.com",
        "phone": "0707741793",
        "isAdmin": True,
        "registered": "Thu, 13 Dec 2018 21:00:00 GMT",
        "password": password
}

question_data = {
    "user_id":1,
    "title":"How to update linux",
    "question":"i was wondering how do u allow automatic updates"
}

user = {
    "user_name": "ule msee",
    "first_name" : "John",
    "last_name" : "Doe",
    "email" : "john@doe.com",
    "phone" :"0727426274",   
    "password" : "hello123",
    "isAdmin" : False
}

answer_data = {
"answer":"you just allow automatic updates hello"

}

data5 = {
    "user_name" : "ule msee",
    "password" : "hello123"
}

data6 = {
    "user_name" : "ule msee",
    "password" : "hello1232"
}