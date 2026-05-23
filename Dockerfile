FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    build-essential cmake curl git libcurl4-openssl-dev python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ggml-org/llama.cpp /llama.cpp && \
    cmake /llama.cpp -B /llama.cpp/build \
      -DBUILD_SHARED_LIBS=OFF \
      -DGGML_CUDA=ON && \
    cmake --build /llama.cpp/build --config Release -j --target llama-server

RUN pip3 install runpod

COPY handler.py /handler.py

CMD ["python3", "/handler.py"]
