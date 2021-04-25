import requests
import json
import click


# @click.group()
# @click.option('--command', prompt='Enter a command', help='''
#                                                     P : to get user's profile
#                                                     c : to add contact
#                                                     L : to login ''')
# def main(command):
# def get_command():
#     command = input('''
#                 -> Enter command:
#                 P : to get user's profile
#                 C : to add contact
#                 L : to login
#                 X : EXIT
#                 ''')

#     if command == 'L':
#         login()
#     elif command == 'P':
#         get_profile()
#     elif command == 'X':
#         quit()

# def loop_command(func):
    # def wrapper(*args, **kwargs):
    #     func(*args, **kwargs)
    #     get_command()
    # return wrapper
    
@click.group()
def main():
    command = input('''
                -> Enter command:
                P : to get user's profile
                C : to add contact
                L : to login
                X : EXIT
                ''')

    if command == 'L':
        login()
    elif command == 'P':
        get_profile()
    elif command == 'X':
        quit()

# @loop_command
@main.command()
@click.option('--username',prompt = 'Enter your Email')
@click.option('--password',prompt = 'Enter your Password')
def login(username, password):
    response = requests.request(url='http://127.0.0.1:5000/auth/login', 
                        method = 'POST',
                        data = {'inputEmail':username,'inputPassword':password}
                        )



    error = json.loads(response.text)['error']
    token = json.loads(response.text)['data'] 
    if error:
        retry = input('RETRY? y/n ')
        if retry =='y':
            login()
        if retry == 'n':
            quit()
    f = open("token.txt", "w")
    f.write(token)
    f.close()

# @loop_command
@main.command()
def get_profile():
    token = open("token.txt")
    response = requests.request(method='GET',
                    url = 'http://127.0.0.1:5000/auth/current_user',
                    headers={'JWT':token})
    
    print(json.load(response.text)['data'])






if __name__ == '__main__':
    main()

# error = True
# while error:
#     email = input('Enter Your Email: ')
#     password = input('Enter Your Password: ')
#     response = requests.post(url='http://127.0.0.1:5000/auth/login', 
#                         data = {'inputEmail':email,'inputPassword':password}
#                             )

#     error = json.loads(response.text)['error']
#     token = json.loads(response.text)['data'] 
#     retry = input('RETRY? y/n')
#     if retry =='n':
#         break
# token_file = open("myfile.txt", "w")
# token_file.write(token)
# token_file.close




