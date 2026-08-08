# This example file shows how to set up a secure (encrypted) connection to a server.
# This can also be done via Nginx, which you can use to set up a reverse proxy that will handle the encrypted connection for you.
# It's recommended to set this up, because clients send their login credentials every time they connect to your server.

# If you want to set up secured connection, you can:
# 1. Use Nginx
# 2. If you have SSL certificate and private key, you can add them like this:

# If you have troubles setting this up, no worries, it's not really important.
# However, if you really want to set this up, contact us on Discord and we'll help you out!

# Import the OnlineClicker server library
from onlineclicker.onlineclicker import *

# Create a server
server = Server()

# This is the important part - enter path to your certificate (fullchain.pem) and private key (privkey.pem)
server.initialize(ssl_chain=["custom/ssl/fullchain.pem", "custom/ssl/privkey.pem"])