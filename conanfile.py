from conans import ConanFile, CMake, tools


class UriparserConan(ConanFile):
    name = "uriparser"
    version = "0.9.0"
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
        self.run("git clone https://github.com/cinderblocks/uriparser.git")
        self.run("cd uriparser && git checkout master")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("uriparser/CMakeLists.txt", "project(UriParser C)",
                              '''project(UriParser C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="uriparser")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/uriparser %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="uriparser/include")
        self.copy("*uriparser.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["uriparser"]

