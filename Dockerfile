#───────────────────────────────────────────────────────────────────────────────
# Builder stage (Jammy → Lunar 24.04, with GCC 13)
#───────────────────────────────────────────────────────────────────────────────
FROM ubuntu:24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      git \
      python3-dev \
      python3-pip \
      gcc-13 \
      g++-13 \
 && rm -rf /var/lib/apt/lists/* \
 && update-alternatives --install /usr/bin/gcc  gcc  /usr/bin/gcc-13 100 \
 && update-alternatives --install /usr/bin/g++  g++  /usr/bin/g++-13 100

WORKDIR /app
COPY . .

RUN mkdir build
WORKDIR /app/build
RUN cmake -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
          ..
RUN make -j$(nproc)

#───────────────────────────────────────────────────────────────────────────────
# Runtime stage (Lunar 24.04-slim)
#───────────────────────────────────────────────────────────────────────────────
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
 && rm -rf /var/lib/apt/lists/*

# install your Python deps (including Streamlit)
RUN pip3 install --no-cache-dir --break-system-packages streamlit

WORKDIR /app

# pull in your compiled extension (it was placed in /app in the builder)
COPY --from=builder /app/pycrlib.so   ./pycrlib.so

# your Python package
COPY src/py  ./py

# so Python can see it
ENV PYTHONPATH=/app/py:/app

# drop you into a shell for experimentation
COPY tests ./tests

# replace your existing CMD with:
CMD ["python3", "tests/test.py"]
