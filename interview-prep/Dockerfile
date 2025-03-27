# Use a multi-stage build to keep the final image small
FROM alpine:3.15 as builder

# Install tools we'll need for our scenarios
RUN apk add --no-cache stress-ng curl bind-tools busybox-extras

FROM alpine:3.15

# Copy tools from builder
COPY --from=builder /usr/bin/stress-ng /usr/bin/stress-ng
COPY --from=builder /usr/bin/curl /usr/bin/curl
COPY --from=builder /usr/bin/nslookup /usr/bin/nslookup
COPY --from=builder /usr/bin/dig /usr/bin/dig
COPY --from=builder /usr/bin/traceroute /usr/bin/traceroute

# Create problematic files and directories
RUN mkdir -p /problematic && \
    touch /problematic/missing-file && \
    rm /problematic/missing-file && \
    dd if=/dev/zero of=/problematic/large-file bs=1M count=100

# Create a script that will simulate different failure modes
COPY simulate-failures.sh /simulate-failures.sh
RUN chmod +x /simulate-failures.sh

# Create a health check that will fail in interesting ways
COPY health-check.sh /health-check.sh
RUN chmod +x /health-check.sh

# Create a script to consume memory
COPY consume-memory.sh /consume-memory.sh
RUN chmod +x /consume-memory.sh

# Create a script with DNS issues
COPY dns-issues.sh /dns-issues.sh
RUN chmod +x /dns-issues.sh

CMD ["/simulate-failures.sh"]
