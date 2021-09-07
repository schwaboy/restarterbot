import discord
import os
from dotenv import load_dotenv
import requests
import logging
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


def restart_container():
    '''Restart a Docker container using the Portainer API'''
    logging.basicConfig(filename='thebot.log', filemode='a', level=logging.DEBUG)
    portainer_pass = os.getenv('PORTAINER_PASS')
    portainer_user = os.getenv('PORTAINER_USER')
    portainer_url = os.getenv('PORTAINER_URL')
    portainer_login = {
        "password": portainer_pass,
        "username": portainer_user
    }

    auth_response = requests.post(f"{portainer_url}/auth", json=(portainer_login))
    d = auth_response.json()
    portainer_token = d['jwt']
    headers = {"Authorization": "Bearer " + portainer_token}

    restart_response = requests.post(f"{portainer_url}/endpoints/1/docker/containers/{os.getenv('CONTAINER_ID')}/restart", headers=headers)
    return restart_response.status_code



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.lower().startswith('greetings'):
        channel = message.channel
        await channel.send('Hello {.author.display_name}!'.format(message))
    elif message.content.endswith(os.getenv('DISCORD_TEST_TRIGGER')):
        channel = message.channel
        await channel.send(os.getenv('DISCORD_TEST_RESPONSE'))
    elif message.content == os.getenv('RESTART_TRIGGER'):
        channel = message.channel
        status = restart_container()
        if status == 204:
            await channel.send("Restarting the bot at the request of {.author.display_name}.".format(message))
        else:
            await channel.send("Failed to restart the bot. Error code: " + status)


client.run(TOKEN)
