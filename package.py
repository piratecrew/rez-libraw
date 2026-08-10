name = "libraw"

version = "0.21.3"

variants = [
    ["platform-linux"]
]

private_build_requires = [
    "gcc-11"
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
