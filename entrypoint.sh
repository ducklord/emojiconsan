#!/bin/bash
printenv | grep TOKEN >> /etc/environment
printenv | grep HOOK >> /etc/environment
cron -f
