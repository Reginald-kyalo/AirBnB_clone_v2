#!/usr/bin/python3
# creates and distributes an archive to web servers

from fabric.api import local, run, put, env
from datetime import datetime
import os.path


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    if local("mkdir -p versions").failed:
        return None
    if not local(f"tar -cvzf versions/{archive_name} web_static").failed:
        return f"versions/{archive_name}"
    else:
        None


env.hosts = ['54.237.64.192', '54.236.12.78']


def do_deploy(archive_path):
    """deploys static files to remote server"""
    if os.path.exists(archive_path) is False:
        return False
    f = archive_path.split('/')[-1]
    n = f.split('.tgz')[0]
    if put(archive_path, '/tmp/{}'.format(f)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(n)).failed is True:
        return False
    if run('sudo mkdir -p /data/web_static/releases/{}'.format(n)).failed:
        return False
    if run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'.
            format(f, n)).failed:
        return False
    if run('rm /tmp/{}'.format(f)).failed:
        return False
    if run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(n, n)).failed:
        return False
    if run('rm /data/web_static/current').failed:
        return False
    if run('sudo ln -s /data/web_static/releases/{} '
            '/data/web_static/current'.format(n)).failed:
        return False


def deploy():
    """creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
