#include "foundation_smoke_service/request_parser.h"

#include <cstddef>
#include <string>

namespace foundation_smoke_service {
namespace {

bool matches(std::string_view input, std::size_t offset, std::size_t length,
             std::string_view expected) noexcept {
    if (length != expected.size() || offset > input.size() || length > input.size() - offset) {
        return false;
    }
    return std::char_traits<char>::compare(input.begin() + static_cast<std::ptrdiff_t>(offset),
                                           expected.begin(), length) == 0;
}

} // namespace

RequestKind parse_request(std::string_view request) noexcept {
    const auto first_space = request.find(' ');
    if (first_space == std::string_view::npos)
        return RequestKind::unknown;
    const auto second_space = request.find(' ', first_space + 1);
    if (second_space == std::string_view::npos)
        return RequestKind::unknown;
    if (!matches(request, 0, first_space, "GET"))
        return RequestKind::unknown;
    const auto path_offset = first_space + 1;
    const auto path_length = second_space - path_offset;
    if (matches(request, path_offset, path_length, "/health"))
        return RequestKind::health;
    if (matches(request, path_offset, path_length, "/metrics"))
        return RequestKind::metrics;
    return RequestKind::unknown;
}

} // namespace foundation_smoke_service
