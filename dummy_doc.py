from models.healthcare_provider import Practitioner

class Practitioner:
    def __init__(self, first_name, second_name, email, password, phone_number, specification):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.specification = specification


print("-- Create a new User --")
my_user = Practitioner("Foo", "Bar", "bkimathi@gmail.com", "root", 123456789, "Dentist")
my_user.save()

print(my_user)
