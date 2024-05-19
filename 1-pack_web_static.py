#!/usr/bin/python3
# generates a .tgz archive from the contents of the web_static

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    now = datetime.today()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    if local("mkdir -p versions").failed:
        return None
    if not local(f"tar -cvzf versions/{archive_name} web_static").failed:
        return f"versions/{archive_name}"
    else:
        None
