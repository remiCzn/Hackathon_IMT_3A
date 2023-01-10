FROM nginx
WORKDIR /app
COPY default.conf /etc/nginx/conf.d/default.conf
RUN apk update && \
    apk add --no-cache openssl && \
    openssl req -x509 -nodes -days 365 \
    -subj  "/C=FR/ST=Nantes/O=Hackathon IMT/CN=chillpaper.fr" \
     -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key \
     -out /etc/ssl/certs/nginx-selfsigned.crt;