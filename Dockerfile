FROM ubuntu:jammy
RUN apt update -y && apt install -y nginx
CMD ["nginx", "-g", "daemon off;"]
