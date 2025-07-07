#!/bin/sh
set -e
DIR=$(dirname "$0")
cd "$DIR"
mkdir -p certs

# CA
openssl req -x509 -newkey rsa:2048 -keyout certs/ca.key -out certs/ca.crt \
  -days 3650 -nodes -subj "/CN=MLLP-CA"

# EAI cert
openssl req -newkey rsa:2048 -keyout certs/eai.key -out eai.csr \
  -nodes -subj "/CN=eai"
openssl x509 -req -in eai.csr -CA certs/ca.crt -CAkey certs/ca.key \
  -CAcreateserial -out certs/eai.crt -days 3650
rm eai.csr

# DPI cert
openssl req -newkey rsa:2048 -keyout certs/dpi.key -out dpi.csr \
  -nodes -subj "/CN=dpi"
openssl x509 -req -in dpi.csr -CA certs/ca.crt -CAkey certs/ca.key \
  -CAcreateserial -out certs/dpi.crt -days 3650
rm dpi.csr

