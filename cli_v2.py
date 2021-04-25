import requests
import json
import jwt


def menu():
    command = input('''
                -> Enter command:
                P : to get user's profile
                C : to add contact
                L : to login
                X : to Exit and Logout
                ''')

    if command.upper() == 'L':
        login()
    elif command.upper() == 'P':
        get_profile()
    elif command.upper() == 'C':
        add_contact()
    elif command.upper() == 'X':
        logout()
    else:
        print('Wrong Command!')
        menu()


def loop_command(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        menu()
    return wrapper


def login_required(func):
    def wrapper(*args, **kwargs):
        with open('token.txt') as f:
            TOKEN = f.read()
            if TOKEN:
                func(*args, **kwargs, TOKEN = TOKEN)
            else:
                print('please login!')
                login()
    return wrapper


@loop_command
def login():
    username = input('Enter Your Email: ')
    password = input('Enter Your Password: ')
    response = requests.request(url='http://127.0.0.1:5000/auth/login', 
                        method = 'POST',
                        data = {'inputEmail':username,'inputPassword':password}
                        )

    error = json.loads(response.text)['error']
    token = json.loads(response.text)['data'] 
    if error:
        retry = input('Login Failed /nRETRY? y/n ')
        if retry =='y':
            login()
        if retry == 'n':
            quit()
    f = open("token.txt", "w")
    f.write(token)
    f.close()

def logout():
    with open('token.txt', 'w') as f:
        f.write("")
        f.close()
        quit()


@loop_command
@login_required
def get_profile(TOKEN):
    response = requests.request(method='GET',
                    url = 'http://127.0.0.1:5000/auth/current_user',
                    headers={'JWT':TOKEN})
    
    data =json.loads(response.text)['data']
    print(f'Welcome {data["client_name"]}')


@loop_command
@login_required
def add_contact(TOKEN):
    name = input("Enter the contact's name: ")
    number = input("Enter the contact's number: ")
    response = requests.post(
                    url = 'http://127.0.0.1:5000/contacts/add',
                    headers= {'JWT':TOKEN},
                    data = {'Name':str(name),
                            'Number':int(number)}
                            )

    data = json.loads(response.text)['data']['contact_id']
    print(f'New contact added - id : {data}')

    while True:
        retry = input('RETRY? y/n ')
        if retry =='y':
            add_contact()
            break
        elif retry == 'n':
            menu()
            break
        else:
            continue




if __name__ == '__main__':
    menu()