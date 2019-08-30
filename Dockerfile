FROM pinellolab/stream:0.3.8

RUN mkdir /stream
COPY visualization_command_line.py /stream/visualization_command_line.py

ENTRYPOINT []
