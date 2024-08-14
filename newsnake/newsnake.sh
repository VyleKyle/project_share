#!/bin/sh
echo -ne '\033c\033]0;newsnake\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/newsnake.x86_64" "$@"
