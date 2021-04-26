from functools import wraps
import requests
import json
import click


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open('token.txt') as f:
            token = f.read()
            if token is None:
                print('/nPlease Login!')
                login()
            else:
                func(*args, **kwargs, token = token)
    return wrapper

def extract_response(response):
    data = json.loads(response.text)['data']
    error = json.loads(response.text)['error']
    info = json.loads(response.text)['info']

    if not error:
        print('++++++ action performed without error ++++++')
        print(f'++++++ {info} ++++++')
        return data
    else:
        print('/n++++++ !!! ++++++')
        print(f"++++++ there was an error, {info}: {error} ++++++")
        return False

@click.group()
def main():
    pass

@main.command()
@click.option('--username', prompt='Enter your Email')
@click.option('--password', prompt='Enter your Password')
def login(username, password):
    '''
    Login and generate token
    '''
    response = requests.request(url='http://127.0.0.1:5000/auth/login',
                                method='POST',
                                data={'inputEmail': username,
                                      'inputPassword': password}
                                )

    
    error = json.loads(response.text)['error']
    token = json.loads(response.text)['data']
    if error:
        print('email or password is incorrect')
        retry = input('RETRY? y/n ')
        if retry == 'y':
            login()
        if retry == 'n':
            quit()
    f = open("token.txt", "w")
    f.write(token)
    f.close()
    print('\n****\nTOKEN SAVED\nYou have successfully logged in!\n****')


@main.command()
@login_required
def get_profile(token):
    '''
    Return user's profile using saved token (name and email)
    '''
    response = requests.request(method='GET',
                                url='http://127.0.0.1:5000/auth/current_user',
                                headers={'JWT': token}
                                )
    data = extract_response(response)
    if data:
        print(f"current user: \nname :{data['client_name']}\nemail:{data['email']}")




@main.command()
@click.option('--prompt', prompt = 'Logout? Y/N')
def logout(prompt):
    '''
    Logout
    '''
    if prompt.upper() == 'Y':
        with open('token.txt', 'w') as f:
            f.write("")
            f.close()
            quit()
    elif prompt.upper() == 'N':
        print('logout canceled')
        print('Your current profile is: ')
        get_profile()
    else:
        print('Wrong Command')
        logout()


@main.command()
@click.option('--name', prompt = "Enter contact's name")
@click.option('--number', prompt = "Enter contact's number")
@login_required
def add_contact(name, number, token):
    response = requests.post(
                    url = 'http://127.0.0.1:5000/contacts/add',
                    headers= {'JWT':token},
                    data = {'Name':name,
                            'Number':number}
                            )

    data = extract_response(response)
    if data:
        contact_id = json.loads(response.text)['data']['contact_id']
        print(f'New contact added with id : {contact_id}')

    while True:
        retry = input('RETRY? y/n ')
        if retry.upper() =='Y':
            main()['add-contact']
            break
        elif retry.upper() == 'N':
            quit()
            break
        else:
            continue





if __name__ == '__main__':
    main()
