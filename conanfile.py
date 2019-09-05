from conans import ConanFile, CMake, tools
import os


class UriparserConan(ConanFile):
    name = "uriparser"
    version = "0.9.3"
    license = "BSD"
    author = "Cinder Biscuits <cinder@cinderblocks.biz>"
    url = "https://github.com/cinderblocks/conan-uriparser"
    description = "uriparser is a strictly RFC 3986 compliant URI parsing and handling library written in C89"
    topics = ("net", "uri", "parser")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        checksum = ""
        source_url = "https://github.com/uriparser/uriparser/releases/download/uriparser-0.9.3/uriparser-0.9.3.zip" 
        tools.get(source_url, sha256=checksum)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["URIPARSER_BUILD_TESTS"] = False
        cmake.definitions["URIPARSER_BUILD_DOCS"] = False
        cmake.definitions["URIPARSER_BUILD_TOOLS"] = False
        cmake.configure(source_folder="uriparser-%s" % self.version)
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/uriparser %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["uriparser"]

