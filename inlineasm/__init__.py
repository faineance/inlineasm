from ctypes import *
from mmap import *
import tempfile
import subprocess
import os

libc = cdll.LoadLibrary("libc.so.6")
mmap = libc.mmap

munmap = libc.munmap
munmap.argtype = [c_void_p, c_size_t]


class assemble(object):
    def __init__(self, code, ret_type, *arg_types, raw=False):
        if not raw:
            with tempfile.NamedTemporaryFile(suffix='.asm') as tmp:
                tmp.write(str.encode(code))
                tmp.flush()
                output_path = "{}.bin".format(tmp.name)
                subprocess.check_call(["nasm", tmp.name, "-o", output_path])

                output = open(output_path, 'rb')
                code = output.read()
                output.close()
                os.remove(output_path)

        if not isinstance(code, list) and isinstance(code, str):
            code = [ord(c) for c in code]

        self.length = len(code)

        mmap.restype = POINTER(ARRAY(c_ubyte, self.length))
        mem = mmap(0, self.length, PROT_READ | PROT_WRITE | PROT_EXEC,
                   MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)[0]
        getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
        func = CFUNCTYPE(ret_type, *arg_types)(getaddr(mem))

        mem[:] = code
        self.func = func
        self.mem = mem

    def __enter__(self):
        return self.func

    def __exit__(self, exc_type, exc_val, exc_tb):
        munmap(self.mem, self.length)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __del__(self):
        munmap(self.mem, self.length)
