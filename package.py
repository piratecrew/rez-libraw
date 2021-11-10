name = "libraw"

version = "0.20.2"

variants = [
    ["platform-linux"]
]

requires = [
    "jpegturbo-2"
]

build_command = "make -f {root}/Makefile {install}"

def commands():
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib")

    if building:
        env.LibRaw_ROOT="{root}" # CMake Hint
        env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")
