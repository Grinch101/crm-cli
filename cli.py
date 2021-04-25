import requests
import json
import click


    
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

@main.command()
def get_profile():
    token = open("token.txt")
    response = requests.request(method='GET',
                    url = 'http://127.0.0.1:5000/auth/current_user',
                    headers={'JWT':token})
    
    print(json.load(response.text)['data'])






if __name__ == '__main__':
    main()
