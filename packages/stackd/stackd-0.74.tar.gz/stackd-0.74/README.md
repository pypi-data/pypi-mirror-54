# stackd

## Installation

### pre-required
```bash
# install docker
DOCKER_VERSION=19.03.2
sudo curl -L https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz -o /tmp/docker.tgz \
  && cd /tmp && tar xzvf /tmp/docker.tgz \
  && sudo cp docker/* /usr/bin/ \
  && rm -rf docker && rm -f docker.tgz
```

### docker
```bash
# install stackd docker runner
sudo curl https://gitlab.com/youtopia.earth/ops/stackd/docker-container/stackd -o /usr/local/bin
sudo chmod +x /usr/local/bin/stackd
```

### debian
```bash
# install dependencies
sudo apt-get update && apt-get install -y \
 httpie \
 jq \
 bash \
 curl \
 python3 \
 python3-distutils

# install pip
cd /tmp &&\
  curl -L https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py &&\
  sudo python3 /tmp/get-pip.py &&\
  rm /tmp/get-pip.py

# install docker-compose
DOCKER_COMPOSE_VERSION=1.24.1
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose

# install nodejs
NODE_VERSION=12.11.0
NODE_DISTRO=linux-x64
curl -L https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-${NODE_DISTRO}.tar.xz -o /tmp/node.tar.xz \
  && sudo mkdir -p /usr/local/lib/nodejs \
  && sudo tar -xJvf /tmp/node.tar.xz -C /usr/local/lib/nodejs \
  && sudo ln -s /usr/local/lib/nodejs/node-v$NODE_VERSION-$NODE_DISTRO/bin/node /usr/bin/node \
  && sudo ln -s /usr/local/lib/nodejs/node-v$NODE_VERSION-$NODE_DISTRO/bin/npm /usr/bin/npm \
  && sudo ln -s /usr/local/lib/nodejs/node-v$NODE_VERSION-$NODE_DISTRO/bin/npx /usr/bin/npx

# docker-compose-merge
DOCKER_COMPOSE_MERGE_VERSION=${DOCKER_COMPOSE_MERGE_VERSION:-latest}
sudo npm i -g docker-compose-merge@$DOCKER_COMPOSE_MERGE_VERSION \
  && ln -s /usr/local/lib/nodejs/node-v$NODE_VERSION-$NODE_DISTRO/bin/docker-compose-merge /usr/bin/docker-compose-merge

# install stackd pip package
pip install --user stackd
```

## enable bash auto-completion
```bash
sudo curl https://gitlab.com/youtopia.earth/ops/stackd/raw/master/bin/completion-stackd.bash -o /etc/bash_completion.d/stackd
source /etc/bash_completion.d/stackd
```


## Usage

```bash
cd /srv/traefik/
export STACKD_ENV=local,production

# default is current directory name
export STACKD_STACK_NAME=traefik

# default: docker-stack.yml
export STACKD_COMPOSE_FILE_BASE=docker-stack.yml

stackd up
```

## .env precedence
- .env.default (always in first, put it in your git repository)
- .env (create it relatively to host, put it in your gitignore)
- .env.*

The `*` can be anything defined in $ENV, you can define ENV in cli or in .env
the .env extra files can be from repository or created relatively to host.
You can add multiple extra env, by separating them with comma, precedence is defined by the order you provided.

### directory layout
```bash
$ tree /srv/traefik/
/srv/traefik/
  ├── docker-stack.local.yml
  ├── docker-stack.yml
  ├── .env
  ├── .env.default
  ├── .env.local
  ├── .env.production
  ├── .gitignore
```

## License
[MIT](https://choosealicense.com/licenses/mit/)