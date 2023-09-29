FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

# Install updates and OS deps
RUN apt update && apt install -y \
    git \
    software-properties-common \
    curl

# Install and setup Python and pip
RUN add-apt-repository -y ppa:deadsnakes/ppa \
    && apt install -y \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Set python3.10 to default python3 and python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 \
    && ln -sf /usr/bin/python3.10 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# Pull repo
RUN git clone https://github.com/billhowelab/llama-fine-tune.git

# Move to speakerbox specific and install
WORKDIR /llama-fine-tune/

# Install all requirements
RUN pip install -r requirements.txt