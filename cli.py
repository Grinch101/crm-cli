from functools import wraps
from stdiomask import getpass
from prettytable import PrettyTable, from_db_cursor
import requests
import json
import click
import asis


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open('token.txt') as f:
            token = f.read()
            if token is None:
                print('/nPlease Login!')
                quit()
            else:
                func(*args, **kwargs, token=token)
    return wrapper


def extract_response(response):
    data = json.loads(response.text)['data']
    error = json.loads(response.text)['error']
    info = json.loads(response.text)['info']
    if error is not None:
        print('++++++ there was an error !!! ++++++')
        raise Exception(f'Command Failed!:\n{error}')
    return info, data, error


def plotter(data, info, data_as_list=False):
    table = PrettyTable()
    if data_as_list is False:
        table.field_names = list(data.keys())
        table.add_row(list(data.values()))
    elif data_as_list is True:
        table.field_names = list(data[0].keys())
        for i in range(len(data)):
            table.add_row(list(data[i].values()))
    print(table.get_string(title=f"{info}"))


@click.group()
def main():
    pass


@main.command()
def signup():
    '''
    Register a user
    '''
    inputEmail = input('Enter Your Email: ')
    inputPassword1 = getpass('Enter Your Password: ')
    inputPassword2 = getpass('Confirm Your Password: ')
    if inputPassword1 != inputPassword2:
        print('Passwords are mismatched!')
        print('please retry')
        quit()
    elif inputPassword1 == inputPassword2:
        client_name = input('Enter your name: ')
        data = {'inputEmail': inputEmail,
                'inputPassword': inputPassword2,
                'client_name': client_name}
        response = requests.request(method='POST',
                                    url='http://127.0.0.1:5000/auth/signup',
                                    data=data)
        info, data, error = extract_response(response)
        plotter(data, info)


@main.command()
def login():
    '''
    Login and generate token
    '''
    username = input('Enter your Email: ')
    password = getpass('Enter your password: ')
    response = requests.request(url='http://127.0.0.1:5000/auth/login',
                                method='POST',
                                data={'inputEmail': username,
                                      'inputPassword': password})

    info, data, error = extract_response(response)
    if error:
        print(f'{error}')
        retry = input('RETRY? y/n ')
        if retry.lower() == 'y':
            main()['login']
        if retry.lower() == 'n':
            quit()
    f = open("token.txt", "w")
    f.write(data)
    f.close()
    if data:
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
    info, data, error = extract_response(response)
    plotter(data, info)


@main.command()
def logout():
    '''
    Logout
    '''
    with open('token.txt', 'w') as f:
        f.write("")
        f.close()
        print('You are now logged out!')
        quit()


@main.command()
@click.option('--name', prompt="Enter contact's name")
@click.option('--number', prompt="Enter contact's number")
@login_required
def add_contact(name, number, token):
    '''
    Add a contact to your phonebook
    '''
    response = requests.post(
        url='http://127.0.0.1:5000/contacts/add',
        headers={'JWT': token},
        data={'Name': name,
              'Number': number}
    )
    info, data, error = extract_response(response)
    plotter(data, info)


@main.command()
@login_required
def update_user(token):
    """
    Update username and password
    """
    new_email = input('Enter Your new Email ')
    new_name = input('Enter your new username ')
    new_password = getpass('Enter Your new password ')
    data_dic = {}
    if new_name is not None:
        data_dic['new_name'] = new_name
    if new_email is not None:
        data_dic['new_email'] = new_email
    if new_password is not None:
        data_dic['new_password'] = new_password

    response = requests.put(url='http://127.0.0.1:5000/auth/user_update',
                            headers={'JWT': token},
                            data=data_dic)

    info, data, error = extract_response(response)
    plotter(data, info)


@main.command()
@login_required
def get_all_contacts(token):
    '''
    Retrieve all contacts of the user
    '''
    response = requests.request(method='GET',
                                url='http://127.0.0.1:5000/contacts/all',
                                headers={'JWT': token})
    info, data, error = extract_response(response)
    plotter(data, info, data_as_list=True)


@main.command()
@click.option('--contact_id', prompt='Enter contact id to delete')
@login_required
def delete_contact(token, contact_id):
    '''
    Delete a contact with the given ID
    '''
    response = requests.request(
        method='DELETE',
        url=f'http://127.0.0.1:5000/contacts/delete/{contact_id}',
        headers={'JWT': token}
    )
    info, data, error = extract_response(response)
    plotter(data, info)


@main.command()
@click.option('--contact_id',
              prompt="Get contact's id to get activities associated with")
@login_required
def get_all_activity(token, contact_id):
    '''
    Retrieve all activites associated with a contact
    '''
    response = requests.get(
        url=f'http://127.0.0.1:5000/activity/{contact_id}',
        headers={'JWT': token}
        )
    info, data, error = extract_response(response)
    plotter(data, info, data_as_list=True)


@main.command()
@click.option('--contact_id', prompt='Enter contact id to add activity to: ')
@click.option('--action', prompt="Enter action's Type: ")
@click.option('--description', default="",
              prompt='Enter any description (optional): ')
@click.option('--date', prompt="Enter data in format: yyyy-mm-dd: ")
@click.option('--time', prompt="Enter time in format: hh:mm: ")
@login_required
def add_activity(token, contact_id, action, description, date, time):
    '''
    Add an activity to a contact
    '''
    response = requests.post(
        url=f'http://127.0.0.1:5000/activity/{contact_id}',
        headers={'JWT': token},
        data={'action': action,
              'description': description,
              'date': date,
              'time': time
              }
        )
    info, data, error = extract_response(response)
    plotter(data, info)


if __name__ == '__main__':
    main()
