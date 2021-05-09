#!/bin/bash
uwsgi --ini /usr/src/app/uwsgi.ini
/etc/init.d/nginx start -g "daemon off"