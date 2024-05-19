#!/usr/bin/env bash
#sets up web servers for the deployment of web_static

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
cat << EOF > "/data/web_static/releases/test/index.html"
<html>
<head>
	<title>Test Page</title>
</head>
<body>
	<h1>Hello, World!</h1>
</body>
</html>
EOF
ln -sf "/data/web_static/releases/test/" "/data/web_static/current"

chown -R ubuntu /data/
chgrp -R ubuntu /data/

cat <<EOL > /etc/nginx/sites-available/default
server {
    listen 80;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /etc/nginx/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}
EOL

service nginx restart
