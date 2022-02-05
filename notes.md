ubuntu dockerfile with: 
- python
- python slack development packages
- nvm
   - nvm is an easy way to install npm
      - npm is installed so we can install localtunnel
         - localtunnel gets us a local port available from the internet for dev purposes without having to open router ports etc.

To build the image: `docker build -t slack_dev .`

Then run the container with `docker-compose up`

All python code should go in the slackbot directory. The container will then automatically see the changes when ever its restarted (ctrl-c then docker-compose up again) without having to rebuild the image since docker compose file mounts that directory as a docker volume. 

because we are using localtunnel, no ports have to be opened anywhere which is realy nice but when it runs, it assigns an arbitrary url and its different every time. That is a pain because we have to tell slack what url to talk to the app at so its annoying to have to change it all the time. localtunnel has an option to request a domain so I have been starting and stopping all afternoon requesting the same domain and that has been working fine.. everything is setup to do that automatically but just be aware that if its running but not responding to slack... it may be that it couldn't get the same domain slack is talking to the bot on in which case, just let me know and we can get a new random domain and update the slack config. 

The slack secrets and the domain we are trying to use are stored in a file called dev.conf. This is ignored in the .gitignore so they dont accidentally get checked into gitub because they need to stay secret. 

based on https://www.digitalocean.com/community/tutorials/how-to-build-a-slackbot-in-python-on-ubuntu-20-04
only differences are
- no "virtual env" so no sourcing a special environment
- all the docker and local tunnel stuff.