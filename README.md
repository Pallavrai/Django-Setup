# Ready-To-Deploy Django, gunicorn, NGINX, Docker Application
Getting a Django 4.2 app up in no time. In this project, gunicorn is used as a WSGI. NGINX is used as a reverse proxy server.

## Premise
I have seen one too many Dockerfile with unreadable code. Many code base out there have Docker setup so elaborately that it is unmodifiable. Here, I try to simplify Dockerfile and Docker Compose file as much as possible, so that more than one developer in a team will understand how it works.

## For Development
In the root level of this repository, copy the file named `django.env.example` to `django.env` and adjust file variables
```
cp django.env.example django.env
```

Now generate secret key for your django.env file

```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Build code with docker compose
```
docker-compose build
```

Run the built container
```
docker-compose up
```

## Deploy as a Simple Application
Here is a script to install docker and docker-compose. After running these commands, exit from ssh and reconnect to the instance. This can be used in AWS Launch Config
```
#!/bin/bash
sudo yum -y update
sudo yum install -y docker
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
For Ubuntu
```
sudo apt update
sudo apt install -y docker.io
sudo usermod -a -G docker $(whoami)
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
# Reset Project for new repo

```
-- Remove the history from 
rm -rf .git

-- recreate the repos from the current content only
git init
git add .
git commit -m "Initial commit"
```