# Use a multi-stage build to keep the final image small
FROM python:3.9-alpine as builder

# Install build dependencies
RUN apk add --no-cache build-base

# Create problematic files and directories
RUN mkdir -p /problematic && \
    touch /problematic/missing-file && \
    rm /problematic/missing-file && \
    dd if=/dev/zero of=/problematic/large-file bs=1M count=100

FROM python:3.9-alpine

# Install runtime dependencies
RUN apk add --no-cache --virtual .runtime-deps curl bind-tools busybox-extras

# Copy problematic files from builder
COPY --from=builder /problematic /problematic

# Install Python dependencies
RUN pip install --no-cache-dir numpy

# Copy the Python script
COPY troubleshoot_scenarios.py /troubleshoot_scenarios.py
RUN chmod +x /troubleshoot_scenarios.py

# Set the entrypoint
ENTRYPOINT ["/troubleshoot_scenarios.py"]
