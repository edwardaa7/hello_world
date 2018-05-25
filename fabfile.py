import os
from fabric.api import require, env, sudo, put
from fabric.context_managers import cd, settings, quiet
from fabric.contrib import files

# Global environment
env.app_dir = 'hello_world'

# Docker credentials
env.docker_registry = os.getenv('DOCKER_REGISTRY')
env.docker_username = os.getenv('DOCKER_USER')
env.docker_password = os.getenv('DOCKER_PASS')
env.docker_image = os.getenv('DOCKER_IMAGE')


# Environments
def production():
    # Server credentials
    env.hosts = [os.getenv('REMOTE_HOST')]
    env.key = os.getenv('SSH_KEY')
    env.sudo_password = os.getenv('SUDO_PASS')


# Tasks
def setup():
    sudo(f'mkdir -p {env.app_dir}')
    update_config()


def update_config():
    put('docker-compose.yml', env.app_dir, use_sudo=True)


def deploy():
    if not files.exists(env.app_dir):
        setup()
    update_config()
    docker_login()
    docker_deploy()


def docker_login():
    require('docker_username', 'docker_password')
    sudo(f'docker logout {env.docker_registry}')

    login_prompts = {
        'Username: ': env.docker_username,
        'Password: ': env.docker_password,
    }

    with settings(prompts=login_prompts):
        sudo(f'docker logout {env.docker_registry}')
        with quiet():
            sudo(f'docker login {env.docker_registry}')


def docker_deploy():
    require('docker_image')
    sudo(f'docker image pull {env.docker_image}')

    with cd(env.app_dir):
        sudo('docker-compose down')
        sudo('docker-compose up -d')
