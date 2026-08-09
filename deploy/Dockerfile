FROM ubuntu:24.04@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90
RUN useradd --system --uid 10001 --no-create-home app
COPY bin/foundation-smoke-service /usr/local/bin/foundation-smoke-service
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/foundation-smoke-service"]
