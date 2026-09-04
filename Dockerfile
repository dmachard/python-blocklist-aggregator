# Multi-stage Dockerfile to build, test, and package blocklist_aggregator

FROM python:3.12-slim AS builder

ARG VERSION="0.0.0.dev0"

WORKDIR /app

# Build dependencies (pure-cdb contains a C extension requiring gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip build setuptools wheel jinja2

# Pre-compile dependency wheels (including pure-cdb)
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Copy source files
COPY README.md LICENSE MANIFEST.in setup.j2 ./
COPY blocklist_aggregator/ ./blocklist_aggregator/

# Generate setup.py and build sdist and wheel packages
RUN python -c 'import jinja2; jinja2.Template(open("setup.j2").read()).stream(version="'"${VERSION}"'").dump("setup.py")' && \
    python setup.py sdist bdist_wheel && \
    cp dist/*.whl /app/wheels/

# Optional test target (e.g. docker build --target tester .)
FROM builder AS tester
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/ ./tests/
COPY testsdata/ ./testsdata/
RUN mkdir -p outputs && \
    pip install --no-cache-dir --no-index --find-links=/app/wheels blocklist_aggregator && \
    python -m unittest tests.test_fetch -v && \
    python -m unittest tests.test_save -v

# Target to extract artifacts to the host (e.g. docker build --target artifacts --output dist .)
FROM scratch AS artifacts
COPY --from=builder /app/dist/* /

# Final lightweight runtime image (without gcc)
FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /app/wheels /tmp/wheels
RUN pip install --no-cache-dir --find-links=/tmp/wheels blocklist_aggregator && \
    rm -rf /tmp/wheels

CMD ["python3"]
