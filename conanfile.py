from conans import ConanFile, CMake, tools


class WebsocketppConan(ConanFile):
    name = "websocketpp"
    version = "0.7.0"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    build_policy = "missing"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
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
        flags = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else "-DBUILD_SHARED_LIBS=OFF"
        flags += " -DENABLE_CPP11=ON -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF"
        flags += " -DCMAKE_INSTALL_PREFIX=%s" % self.package_folder
        self.run('cmake websocketpp %s %s' % (cmake.command_line, flags))
        self.run("cmake --build . --target install%s" % cmake.build_config)
