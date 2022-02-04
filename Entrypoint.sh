#!/bin/bash

NODE_VERSION=$(cat /root/.nvm/alias/default)
/root/.nvm/versions/node/v$NODE_VERSION/bin/node /root/.nvm/versions/node/v$NODE_VERSION/bin/lt --subdomain $LT_SUBDOMAIN --port 3000&
python3 /slackbot/app.py