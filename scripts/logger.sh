#!/usr/bin/env bash

# Created by crzorz on 2022/09/16
# Copyright © 2022 BaldStudio. All rights reserved.

# debug:0; info:1; warn:2; error:3
LOG_LEVEL=0
LOG_DETAIL=0

Logging() {
  local level
  level=$1
  readonly level

  local msg
  msg=$2
  readonly msg

  local timestamp
  timestamp=$(date +'%F %H:%M:%S')
  readonly timestamp

  local format
  format="[${timestamp}][${level}] ${msg}"
  if [[ ${LOG_DETAIL} -eq 1 ]]; then
    format="[${timestamp}] [${level}] [${FUNCNAME[2]} - $(caller 0 | awk '{print$1}')] ${msg}"
  fi
  readonly format

  case $level in
  DEBUG)
    if [[ $LOG_LEVEL -le 0 ]]; then
      echo -e "\033[37m${format}\033[0m"
    fi
    ;;
  INFO)
    if [[ $LOG_LEVEL -le 1 ]]; then
      echo -e "\033[32m${format}\033[0m"
    fi
    ;;
  WARNING)
    if [[ $LOG_LEVEL -le 2 ]]; then
      echo -e "\033[33m${format}\033[0m"
    fi
    ;;
  ERROR)
    if [[ $LOG_LEVEL -le 3 ]]; then
      echo -e "\033[31m${format}\033[0m"
    fi
    ;;
  esac
}

LogDebug() {
  Logging DEBUG "$*"
}

LogInfo() {
  Logging INFO "$*"
}

LogWarn() {
  Logging WARNING "$*"
}

LogError() {
  Logging ERROR "$*"
}