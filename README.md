# This is going away soon. I intend to replace it with a whole new repository.
# Big changes coming soon!

## Starting to turn this into more of a Sports-themed Discord bot. We'll see how it goes!

# Restarterbot

A Discord bot that restarts a Docker container via Portainer.

## Configuration

Configure the bot via the variables defined in the `.env` file.

<pre>
DISCORD_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PORTAINER_USER=username
PORTAINER_PASS=password
PORTAINER_URL=http://example.com:9000/
CONTAINER_ID=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
RESTART_TRIGGER=restart the container
DISCORD_TEST_TRIGGER=>** discordtest
DISCORD_TEST_RESPONSE=Hello, Discord!
</pre>

## Usage

`python3 ./restarterbot.py`

Say the $RESTART_TRIGGER phrase in any channel the bot is in, or via DM, to restart your container.

### :warning: Requires Python3.6 or greater

## Built with

- [Python3](https://docs.python.org/3/)
