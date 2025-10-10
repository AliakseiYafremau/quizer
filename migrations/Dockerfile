FROM alpine:3

RUN apk --no-cache add curl
RUN curl -fsSL https://raw.githubusercontent.com/pressly/goose/master/install.sh | sh

WORKDIR /src
COPY 20251008174848_initial.sql .
ENTRYPOINT [ "goose" ]