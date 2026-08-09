#include "foundation_smoke_service/request_parser.h"

#include <cstddef>
#include <cstdint>
#include <string_view>

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t* data, std::size_t size) {
    static_cast<void>(foundation_smoke_service::parse_request(
        std::string_view(reinterpret_cast<const char*>(data), size)));
    return 0;
}
