#!/usr/bin/python3
# distributes an archive to web servers
from fabric import Connection, Config
import os

env.hosts=['54.237.64.192', '54.236.12.78']
env.users=['ubuntu']
env.key_filename = ['~/.ssh/school']
config=Config(overrides=env)

def do_deploy(archive_path):
    """deploys static files to remote server"""
    return False if !os.path.exists(archive_path)
    with Connection(config=config) as c:
        f = archive_path.split('/')[-1]
        dir_name = f.split('.tgz')[0]
        return False if c.put(local = archive_path, remote = '/tmp/').failed
        return False if c.run(f'mkdir -p data/web_static/releases/{dir_name}').failed
        return False if c.run(f'tar -xzf /tmp/{f} -C /data/web_static/releases/{compressed_file.strip(".tgz")}').failed
        return False if c.run(f'rm /tmp/{compressed_file.strip(".tgz")}').failed
        return False if c.run(f'rm /data/web_static/current').failed
        return False if c.run(f'ln -s /data/web_static/current /data/web_static/releases/{dir_name}').failed

