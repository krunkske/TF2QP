#!/bin/sh
echo -ne '\033c\033]0;TF2QP\a'
base_path="$(dirname "$(realpath "$0")")"
"$base_path/tf2qp.x86_64" "$@"
