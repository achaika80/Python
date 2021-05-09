#!/bin/bash
uwsgi --ini /usr/src/app/uwsgi.ini
/etc/init.d/nginx -g "daemon off;"