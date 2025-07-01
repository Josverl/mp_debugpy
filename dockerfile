FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
WORKDIR /usr/micropython
COPY firmware/unix_settrace_set_local/micropython /usr/local/bin/micropython
EXPOSE 5678
ENTRYPOINT ["/usr/local/bin/micropython"]


# docker build -t micropython/debugpy:0.4 -t micropython/debugpy:latest .
# docker run -it --rm -p 5678:5678 -v ./src:/usr/micropython -v ./launcher:/usr/lib/micropython -v ./micropython-lib/python-ecosys/debugpy:/root/.micropython/lib micropython/debugpy:latest -m start_debugpy run_pystone main 

