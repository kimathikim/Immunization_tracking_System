#!/usr/bin/python3
from models.parent import Parent

print("-- Create a new User --")
my_user = Parent()
my_user.first_name = "Foo"
my_user.second_Name = "Bar"
my_user.email = "bkimathi@gmail.com"
my_user.password = "root"
my_user.phone_number = 123456789
my_user.county = "Meru"
my_user.save()
print(my_user)
https://moodle.kabarak.ac.ke/pluginfile.php/1/core_admin/logocompact/300x300/1704363894/main_logo.png