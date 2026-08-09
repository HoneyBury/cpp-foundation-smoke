function(foundation_enable_warnings target)
    if(MSVC)
        target_compile_options(${target} PRIVATE /W4 /permissive-)
        if(FOUNDATION_WARNINGS_AS_ERRORS)
            target_compile_options(${target} PRIVATE /WX)
        endif()
    elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(
            ${target}
            PRIVATE -Wall
                    -Wextra
                    -Wpedantic
                    -Wconversion
                    -Wsign-conversion
                    -Wshadow
                    -Wformat=2
                    -Wundef
                    -Wnon-virtual-dtor
                    -Wold-style-cast
                    -Woverloaded-virtual
        )
        if(FOUNDATION_WARNINGS_AS_ERRORS)
            target_compile_options(${target} PRIVATE -Werror)
        endif()
    endif()
endfunction()

function(foundation_enable_coverage target)
    if(NOT FOUNDATION_ENABLE_COVERAGE)
        return()
    endif()
    if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        message(FATAL_ERROR "FOUNDATION_ENABLE_COVERAGE requires GCC or Clang")
    endif()
    target_compile_options(${target} PRIVATE -O0 -g --coverage)
    target_link_options(${target} PRIVATE --coverage)
endfunction()
