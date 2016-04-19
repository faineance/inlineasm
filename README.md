# inlineasm [![PyPI](https://img.shields.io/pypi/dm/inlineasm.svg?maxAge=2592000)](https://pypi.python.org/pypi/inlineasm/)

Inline assembly/machine code in Python. And you thought it couldn't get any worse.
## Informal Docs
`assemble(<code>, <return_type>, *<arg_types>, <is raw machine code?>`
## Examples

### Assembly example
```python
add_asm = '''
bits 64
mov rax, rdi
add rax, rsi
ret
'''
with assemble(add_asm, c_int, c_int, c_int) as add:
    assert add(1, 2) == 3
    
add = assemble(add_asm, c_int, c_int, c_int)
assert add(2, 2) == 4
```

### Machine Code example
```python

with assemble([0xb8, 0x2a, 0x00, 0x00, 0x00, 0xc3], c_int, raw=True) as douglas:
    assert douglas() == 42
    
with assemble('\xb8\x2b\x00\x00\x00\xc3', c_int, raw=True) as notquitedouglas:
    assert notquitedouglas() == 43
```
