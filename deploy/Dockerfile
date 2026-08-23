FROM ubuntu:24.04@sha256:33ceb71981b602c1a7443a53469e4dba065f7503eab3078a2d7a57a2ab987517
RUN useradd --system --uid 10001 --no-create-home app
COPY bin/foundation-smoke-service /usr/local/bin/foundation-smoke-service
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/foundation-smoke-service"]
