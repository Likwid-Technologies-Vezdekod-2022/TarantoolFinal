#!/bin/bash

sleep 3
gunicorn --bind 0.0.0.0:8081 wsgi:app
