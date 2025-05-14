FROM alpine:latest

WORKDIR /opt/qtile-analyzer
COPY . .
RUN apk add --no-cache python3 py3-pip && \
        echo gunicorn >> requirements.txt && \
        pip3 install -r requirements.txt --no-cache-dir \
        --break-system-packages && \
        apk del --rdepends py3-pip && rm requirements.txt && \
        flask init-db

EXPOSE 8000
USER nobody

CMD ["gunicorn", "app:app", "-b", "0.0.0.0"]

