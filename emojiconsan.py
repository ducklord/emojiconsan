import datetime
import json
import os
import requests
import sys
from pathlib import Path
from urllib.parse import urlparse

backupdir = '/emojis'

check_size = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--check-size':
        check_size = True

def message(msg):
    webhookurl="https://hooks.slack.com/services/" + os.environ['HOOK']
    response = requests.post(url = webhookurl, data = "{\"text\":\"%s\"}" % msg)

def save_emoji(url, filename):
    resp = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(resp.content)

response = requests.get("https://slack.com/api/emoji.list", headers={'Authorization': 'Bearer '+os.environ['TOKEN']})
data = json.loads(response.text)
for (name, url) in data['emoji'].items():
    #print("%s/%s" % (name, url))
    if url[0:6] == 'alias:':
        linkname = "%s/%s" % (backupdir, name)
        target = url[6:]
        if not os.path.islink(linkname):
            os.symlink(target, linkname)
            message("New alias %s to :%s:" % (name, target))
    else:
        path = urlparse(url).path
        extension = os.path.splitext(path)[1]
        filename = "%s/%s%s" % (backupdir, name, extension)
        if os.path.isfile(filename):
            if check_size:
                response = requests.head(url)
                remote_size = int(response.headers['Content-Length'])
                local_size = os.path.getsize(filename)
                if remote_size != local_size:
                    os.rename(filename, "%s-%s" % (filename, datetime.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")))
                    save_emoji(url, filename)
                    message("Emoji :%s: (%s) changed!" % (name, name))
        else:
            save_emoji(url, filename)
            message("New emoji :%s: (%s)" % (name, name))

Path('/monitoring/emojiconsan.stamp').touch()
