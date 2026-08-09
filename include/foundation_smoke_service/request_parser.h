#pragma once

#include <string_view>

namespace foundation_smoke_service {

enum class RequestKind { health, metrics, unknown };

RequestKind parse_request(std::string_view request) noexcept;

} // namespace foundation_smoke_service
