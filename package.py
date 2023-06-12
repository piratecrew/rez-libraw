name = "libraw"

version = "0.21.1.1"

variants = [
    ["platform-linux"]
]

@early() # type: ignore
def build_requires():
    # check if the system gcc is too old <9
    # then we require devtoolset-9
    from subprocess import check_output
    gcc_major = int(check_output(r"gcc -dumpversion | cut -f1 -d.", shell=True).strip().decode())
    if gcc_major < 9:
        return ["devtoolset-9"]

    return []

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
