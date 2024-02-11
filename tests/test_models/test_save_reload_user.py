#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

all_objts = storage.all()
print("-- Reloaded objects --")
for objt_id in all_objts.keys():
    objt = all_objts[objt_id]
    print(objt)

print("-- Create a new User --")
new_user = User()
new_user.first_name = "Betty"
new_user.last_name = "Bar"
new_user.email = "airbnb@mail.com"
new_user.password = "root"
new_user.save()
print(new_user)

print("-- Create a new User 2 --")
new_user2 = User()
new_user2.first_name = "John"
new_user2.email = "airbnb2@mail.com"
new_user2.password = "root"
new_user2.save()
print(new_user2)
