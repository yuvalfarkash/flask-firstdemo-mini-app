users = {
    "alice": "1234",
    "bob": "abcd",
    "charlie": "pass"
}

def login(username, password):
        if users[username] == password:
            return True
        return False
    

username = input("Enter username: ")
password = input("Enter password: ")

if login(username, password):
    print("Login successful")
else:
    print("Invalid credentials")