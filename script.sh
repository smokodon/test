#!/usr/bin/env bash

set -o errexit

function main() {
 touch /etc/default/grub
 echo "GRUB_CMDLINE_LINUX=systemd.unified_cgroup_hierarchy=1" >> /etc/default/grub
 ls /etc/default/grub
}

main "$@"
