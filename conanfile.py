from conans import ConanFile, CMake, tools


class WebsocketppConan(ConanFile):
    name = "websocketpp"
    version = "0.7.0"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    build_policy = "missing"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/zaphoyd/websocketpp.git")
        self.run("cd websocketpp && git checkout %s" % self.version)
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("websocketpp/CMakeLists.txt", "PROJECT(websocketpp)", '''PROJECT(websocketpp)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        else:
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        if self.settings.os != "Windows" and self.options.fPIC:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "True"
            
        cmake.definitions["ENABLE_CPP11"] = "ON"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_TESTS"] = "OFF"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder

        cmake.configure(source_dir="websocketpp")
        cmake.build()
        cmake.install()
