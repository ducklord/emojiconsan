#!/bin/bash
backupdir=/emojis

if [ -z ${TOKEN+x} ]; then
    echo "Missing token"
    exit 1
fi

if [ -z ${HOOK+x} ]; then
    echo "Missing web hook"
    exit 1
fi

bearerheader="Authorization: Bearer $TOKEN"
webhookurl="https://hooks.slack.com/services/$HOOK"

mkdir -p "$backupdir"

function save_emoji {
  local url="$1"
  local filename="$2"
  curl -s "${url}" -o "${filename}"
}

function message {
    message="${1}"
    curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$message\"}" $webhookurl# &>/dev/null
}

#TODO detect deleted emojis
curl -s -H "$bearerheader" "https://slack.com/api/emoji.list" \
  | jq -r ".emoji | to_entries[] | [.key, .value] | @sh" \
  | tr -d \' \
  | while read -r name url; do
    if grep -q -e "^alias:" <<<"${url}"; then
      linkname="${backupdir}/${name}"
      target="$(cut -f 2 -d: <<<${url})"
      if [ ! -L "${linkname}" ]; then
        ln -fs "${target}" "${linkname}"
        message "New alias ${name} to :${target}:"
      fi
    else
      extension="${url##*.}"
      filename="${backupdir}/${name}.${extension}"
      if [ -f "${filename}" ]; then
        remote_size=$(curl -s --head "$url" | grep '^content-length:'  | cut -f 2- -d' ' | tr -d '[:space:]')
        locale_size=$(stat -c%s "${filename}")
        if [ $remote_size -ne $locale_size ]; then
          mv "${filename}" "${filename}-$(date +%s.%N)"
          save_emoji "${url}" "${filename}"
          message "Emoji :${name}: (${name}) changed!"
        fi
      else
        # we have a new emoji
        save_emoji "${url}" "${filename}"
        message "New emoji :${name}: (${name})"
      fi
    fi
  done
