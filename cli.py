from requests import request
import json
import click


@click.command()
@click.option('--username',prompt = 'Enter your Email')
@click.option('--password',prompt = 'Enter your Password')
def login(username, password):
    response = request(url='http://127.0.0.1:5000/auth/login', 
                    method = 'POST',
                    data = {'inputEmail':f'username','inputPassword':f'password'})
    click.echo(json.loads(response.text))

    


