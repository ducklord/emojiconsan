import datetime
import os
import requests

backupdir = './emojis'

def message(msg):
    #requests.post(url = webhookurl, data = "{\"text\":\"%s\"}" % msg)
    print(msg)

def save_emoji(url, filename):
    resp = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(resp.content)

with open('data', 'r', encoding='utf-8') as infile:
    for line in infile:
        parts = line.split()
        name = parts[0]
        url = parts[1]
        #print("%s/%s" % (name, url))
        if url[0:6] == 'alias:':
            linkname = "%s/%s" % (backupdir, name)
            target = url[6:]
            if not os.path.islink(linkname):
                os.symlink(target, linkname)
                message("New alias %s to :%s:" % (name, target))
        else:
            extension = url.split('.')[1]
            filename = "%s/%s.%s" % (backupdir, name, extension)
            if os.path.isfile(filename):
                response = requests.head(url)
                remote_size = int(response.headers['Content-Length'])
                local_size = os.path.getsize(filename)
                if remote_size != local_size:
                    print("r %d l %d" % (remote_size, local_size))
                    os.rename(filename, "%s-%s" % (filename, datetime.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")))
                    save_emoji(url, filename)
                    message("Emoji :%s: (%s) changed!" % (name, name))
            else:
                save_emoji(url, filename)
                message("New emoji :%s: (%s)" % (name, name))
