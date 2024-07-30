FROM ruby:3.2.2-slim

RUN apt update && apt install -y --no-install-recommends postgresql-client git make gcc g++ libcurl4 libpq-dev &&    rm -rf /var/lib/apt/lists/*

WORKDIR /travis-migrations

COPY . ./

RUN echo "hello"

CMD /bin/bash