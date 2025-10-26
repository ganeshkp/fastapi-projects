"""
Function Assignment
- Create a function that takes in 3 parameters(firstname, lastname, age) and
returns a dictionary based on those values
"""


def owner_dictionary(firstname, lastname, age):
    created_owner_dictionary = {
        "firstname": firstname,
        "lastname": lastname,
        "age": age,
    }
    return created_owner_dictionary


solution_dictionary = owner_dictionary(firstname="Eric", lastname="Roby", age=32)
print(solution_dictionary)
