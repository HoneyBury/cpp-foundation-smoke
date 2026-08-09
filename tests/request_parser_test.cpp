#include "foundation_smoke_service/request_parser.h"

#include <cstdlib>

int main() {
    if (foundation_smoke_service::parse_request("GET /health HTTP/1.1\r\n") !=
        foundation_smoke_service::RequestKind::health)
        return EXIT_FAILURE;
    if (foundation_smoke_service::parse_request("GET /metrics HTTP/1.1\r\n") !=
        foundation_smoke_service::RequestKind::metrics)
        return EXIT_FAILURE;
    if (foundation_smoke_service::parse_request("POST /health HTTP/1.1\r\n") !=
        foundation_smoke_service::RequestKind::unknown)
        return EXIT_FAILURE;
    if (foundation_smoke_service::parse_request("GET /unknown HTTP/1.1\r\n") !=
        foundation_smoke_service::RequestKind::unknown)
        return EXIT_FAILURE;
    if (foundation_smoke_service::parse_request("GET ") !=
        foundation_smoke_service::RequestKind::unknown)
        return EXIT_FAILURE;
    if (foundation_smoke_service::parse_request("invalid") !=
        foundation_smoke_service::RequestKind::unknown)
        return EXIT_FAILURE;
    return EXIT_SUCCESS;
}
