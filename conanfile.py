from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout

from conan import ConanFile


class FoundationSmokeServiceConan(ConanFile):
    name = "foundation_smoke_service_workspace"
    version = "0.1.0"
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        self.requires("fmt/11.2.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        CMakeDeps(self).generate()
        CMakeToolchain(self).generate()
