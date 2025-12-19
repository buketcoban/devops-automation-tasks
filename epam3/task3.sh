#!/bin/bash

cp passwd passwd_new

awk -F: 'BEGIN{OFS=":"} $1=="saned" {$7="/bin/bash"} {print}' passwd_new > passwd_new.tmp && mv passwd_new.tmp passwd_new

sed -i '' 's/^\(avahi:[^:]*:[^:]*:[^:]*:[^:]*:[^:]*:\).*$/\1\/bin\/bash/' passwd_new

awk -F: '{print $1":"$3":"$5":"$7}' passwd_new > passwd_new.tmp && mv passwd_new.tmp passwd_new

sed -i '' '/daemon/d' passwd_new

awk -F: 'BEGIN{OFS=":"} $2 % 2 == 0 {$4="/bin/zsh"} {print}' passwd_new > passwd_new.tmp && mv passwd_new.tmp passwd_new

truncate -s -1 passwd_new

echo "Task completed! passwd_new file is ready."
