FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
WORKDIR /usr/micropython
COPY firmware/unix_debug_enabled/micropython /usr/local/bin/micropython
EXPOSE 5678
ENTRYPOINT ["/usr/local/bin/micropython"]


# docker build -t micropython/debugpy:0.2 .
# docker run -it --rm -p 5678:5678 -v ./src:/usr/micropython -v ./launcher:/usr/lib/micropython -v ./micropython-lib/python-ecosys/debugpy:/root/.micropython/lib micropython/debugpy:0.2 -m start_debugpy 
