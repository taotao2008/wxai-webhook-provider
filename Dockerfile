# Bundle Stage
FROM python:3.10.10-slim-buster
RUN apt-get update && apt-get install -y ca-certificates
RUN apt-get install git -y
WORKDIR /opt/
RUN git clone -b wali https://github.com/taotao2008/wxai-webhook-provider.git
WORKDIR /opt/wxai-webhook-provider/src
RUN git pull
RUN pip install --no-cache-dir -r requirements.txt
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]