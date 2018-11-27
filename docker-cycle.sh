#!/bin/bash
# Basic script to build and run idm-bot on a basic python-slim image
docker build -t datatellers/idm-bot:latest --rm --force-rm .
docker run -d -p5002:5002 datatellers/idm-bot:latest
