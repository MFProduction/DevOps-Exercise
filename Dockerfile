FROM python:2.7-alpine
MAINTAINER ferenc.matej@gmail.com

ENV APP_NAME app
ENV APP_PATH /${APP_NAME}
WORKDIR $APP_PATH
ADD . $APP_PATH

RUN apk update
RUN apk add --no-cache --update bash curl gcc libc-dev jq
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/main postgresql-dev
RUN pip install -r requirements.txt
RUN chmod +x test_service_api.sh mind_the_gap.py run.sh

ENTRYPOINT ["/bin/bash","./run.sh"]
CMD ["-v"]
