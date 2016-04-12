from ctypes import *
from mmap import *

libc = cdll.LoadLibrary("libc.so.6")
mmap = libc.mmap

munmap = libc.munmap
munmap.argtype = [c_void_p, c_size_t]


class assemble(object):
    def __init__(self, code, ret_type, *arg_types):
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

