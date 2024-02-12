#!/usr/bin/python3
"""Test file"""
from models import storage
from models.base_model import BaseModel

all_objts = storage.all()
print("-- Reloaded objects --")
for objt_id in all_objts.keys():
    objt = all_objts[objt_id]
    print(objt)

print("-- Create a new object --")
new_model = BaseModel()
new_model.name = "My_First_Model"
new_model.new_number = 89
new_model.save()
print(new_model)
