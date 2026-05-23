FROM ghcr.io/ggml-org/llama.cpp:server-cuda

RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install runpod requests --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

COPY handler.py /handler.py

CMD ["python3", "/handler.py"]
