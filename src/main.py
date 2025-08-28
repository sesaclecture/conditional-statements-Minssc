
from enum import Enum
import json

class Menu(Enum):
    NULL = ""
    SIGNUP = "1"
    LOGIN = "2"

class Action(Enum):
    NULL = ""
    LOGOUT = "0"
    EDIT_SELF = "1"
    DELETE_SELF = "2"
    EDIT_OTHER = "3"
    DELETE_OTHER = "4"

database = {
    "minssc": {
        "name": "minsung",
        "birthday": "19970528",
        "password": "1234",
        "role": "admin"
    },
    "bot": {
        "name": "bot01",
        "birthday": "19700101",
        "password": "0000",
        "role": "viewer"
    }
}

print("List of users:")
print(json.dumps(database, indent=2))

while True:
    jobs = input("Select action (Sign up:1, Log in:2, Quit otherwise): ")
    match Menu(jobs):
        case Menu.SIGNUP:
            id = input("Enter id: ")
            if not id.strip():
                print("ID cannot be blank")
                continue
            if id in database:
                print(f"ID {id} already exists!")
                continue
            password = input("Enter password(length > 4, must include special char): ")
            if len(password) <= 4:
                print("Password too short!")
                continue
            scar = False
            if '~' in password or '!' in password or '@' in password or '#' in password or '$' in password:
                scar = True
            elif '%' in password or '^' in password or '&' in password or '*' in password or '(' in password or ')' in password:
                scar = True
            elif '-' in password or '_' in password or '=' in password or '+' in password or '\\' in password or '|' in password:
                scar = True
            if not scar:
                print("Must include a special character!")
                continue
            bday = input("Enter birthdate (yyyymmdd): ")
            _month = int(bday[4:6])
            _day = int(bday[6:8])
            if not bday.isnumeric() or len(bday) != 8 or _month == 0 or _month > 12 or _day > 31 or _day == 0:
                print(f"Invalid birthday: {bday}")
                continue
            name = input("Enter name: ")
            role = input("Enter your role (admin, editor, viewer): ") # skipping input verification. 
            database[id] = {"name": name, "birthday": bday, "password": password, "role": role}

            print("Successfully signed up!")
            print("List of users:")
            print(json.dumps(database, indent=2))

        case Menu.LOGIN:
            id = input("Enter ID: ")
            if id in database:
                data = database[id]
                password = input("Enter password: ")
                if password == data["password"]:
                    print(f"Logged in as {id} - {data["role"]}")

                    while True:
                        itxt = "Select action (Logout:0, Edit my profile:1, Delete account:2"
                        if data["role"] == "admin" or data["role"] == "editor":
                            itxt += ", Edit other profile:3"
                        if data["role"] == "admin":
                            itxt += ", Delete other account:4"
                        itxt += "): "
                        action = input(itxt)
                        match Action(action):
                            case Action.LOGOUT:
                                print(f"Good bye {id}!")
                                break

                            case Action.EDIT_SELF:
                                field = input("Enter field to edit (name, birthday, password, role): ")
                                if field in data:
                                    value = input("Enter new value: ")
                                    data[field] = value # Could check for birthday and password validity but it'd just be duplicate code. Skipping.
                                    print("\nList of users:")
                                    print(json.dumps(database, indent=2))
                                else:
                                    print(f"Unknown field {field}.")

                            case Action.DELETE_SELF:
                                confirm = input("Are you sure? (y/n): ")
                                if confirm.lower() == "y":
                                    print("Good bye.")
                                    database.pop(id)
                                    print("\nList of users:")
                                    print(json.dumps(database, indent=2))
                                    break            

                            case Action.EDIT_OTHER:
                                if data["role"] == "viewer":
                                    continue
                                id = input(f"Enter id to edit ({', '.join(database)}): ")
                                if id in database:
                                    _data = database[id]
                                    field = input("Enter field to edit (name, birthday, password, role): ")
                                    if field in _data:
                                        value = input("Enter new value: ")
                                        _data[field] = value
                                        print("\nList of users:")
                                        print(json.dumps(database, indent=2))
                                else:
                                    print(f"Unknown ID {id}")
                                    continue

                            case Action.DELETE_OTHER:
                                if data["role"] != "admin":
                                    continue
                                _id = input(f"Enter id to delete ({", ".join(database)}): ")
                                if _id in database:
                                    confirm = input("Are you sure? (y/n): ")
                                    if confirm.lower() == "y":
                                        database.pop(_id)
                                        print("\nList of users:")
                                        print(json.dumps(database, indent=2))
                                        if _id == id:
                                            print(f"Good bye")
                                            break
                                else:
                                    print(f"Unknown ID {id}")
                                    continue
                else:
                    print("Wrong password.")
            else:
                print(f"ID {id} doesn't exist!")

        case _:
            break


