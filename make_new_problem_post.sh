#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <name>  (e.g. leetcode-3)"
    exit 1
fi

NAME="$1"
FILE="content/problems/${NAME}.md"

if [ -f "$FILE" ]; then
    echo "Error: $FILE already exists"
    exit 1
fi

DATE=$(date +"%Y-%m-%dT%H:%M:%S%z")

cat > "$FILE" <<EOF
+++
date = '${DATE}'
draft = false
title = '${NAME}'
url = '/posts/${NAME}/'
+++

EOF

echo "Created $FILE"
