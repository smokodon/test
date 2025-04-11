#!/usr/bin/env bash
set -o errexit

main() {
  local tmp
  tmp="$(mktemp -d)"

  local sudo=''
  if [[ "${TRAVIS}" ]]; then
    sudo='sudo'
  fi

  wget 'https://github.com/pgpartman/pg_partman/archive/refs/tags/v5.2.4.tar.gz' \
    | tar -xzf - -C "${tmp}"

  "${sudo}" make install -C "${tmp}/pg_partman-v5.2.4"
}

main "$@"
