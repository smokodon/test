#!/usr/bin/env bash
set -o errexit

main() {
  local tmp
  tmp="$(mktemp -d)"

  local sudo=''
  if [[ "${TRAVIS}" ]]; then
    sudo='sudo'
  fi

  curl -sSL 'https://github.com/keithf4/pg_partman/archive/v5.2.4.tar.gz' \
    | tar -xzf - -C "${tmp}"

  "${sudo}" make install -C "${tmp}/pg_partman-v5.2.4"
}

main "$@"
