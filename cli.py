import requests
import json
import click


    
@click.group()
def main():

    pass

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
    print('\nTOKEN SAVED\n**** \nYou have successfully logged in!')
    



@main.command()
def get_profile():
    with open("token.txt") as f:
        token = f.read()
    response = requests.request(method='GET',
                    url = 'http://127.0.0.1:5000/auth/current_user',
                    headers={'JWT':str(token)}
                    )
    data = json.loads(response.text)['data']
    current_user = data['client_name']
    email = data['email']

    print(f'\ncurrent user: \nname :{current_user}\nemail:{email}')






if __name__ == '__main__':
    main()
