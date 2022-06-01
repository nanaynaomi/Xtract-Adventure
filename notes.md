
For AWS build
- docker build -t xtract_adventure .
- aws ecr get-login-password | docker login --username AWS --password-stdin 229178395146.dkr.ecr.us-west-2.amazonaws.com (must be done from a computer with awscli and auth tokens)
- docker tag xtract_adventure 229178395146.dkr.ecr.us-west-2.amazonaws.com/summit-dev:xtract-adventure
- docker push 229178395146.dkr.ecr.us-west-2.amazonaws.com/summit-dev:xtract-adventure

Slack config
Xtract Dev > settings & administration > Manage Apps > Build > Xtract Adventure 