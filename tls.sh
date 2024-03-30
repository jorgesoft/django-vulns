docker run -it --rm \
    -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    -p "80:80" \
    certbot/certbot certonly \
    --standalone \
    --preferred-challenges http \
    -d db.nubitlan.com
