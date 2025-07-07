FROM alpine:3.20
RUN apk add --no-cache netcat-openbsd
WORKDIR /app
COPY send.sh listen.sh message.hl7 ./
CMD ["sleep", "infinity"]
