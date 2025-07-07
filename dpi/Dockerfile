FROM alpine:3.20
RUN apk add --no-cache python3 py3-pip stunnel
WORKDIR /app
COPY . ./
RUN chmod +x send.sh listen.sh entrypoint.sh
CMD ["/app/entrypoint.sh"]
