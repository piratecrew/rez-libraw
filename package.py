name = "libraw"

version = "0.20.2"

variants = [
    ["platform-linux"]
]

@early()
def build_requires():
    # check if the system gcc is too old <9
    # then we require devtoolset-9
    from subprocess import check_output
    valid = check_output(r"expr `gcc -dumpversion | cut -f1 -d.` \>= 9 || true", shell=True).strip().decode() == "1"
    if not valid:
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
