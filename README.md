# inlineasm
Inline assembly/machine code in Python. And you thought it couldn't get any worse.
## Examples

### Assembly example
```python
add_asm = '''
bits 64
mov rax, rdi
add rax, rsi
ret
'''
with assemble(add_asm, c_int, c_int, c_int, nasm=True) as add:
    assert add(1, 2) == 3
```

### Machine Code example
```python
# You can also pass machine code as a string "\xb8\x2a\x00\x00\x00\xc3"
with assemble([0xb8, 0x2a, 0x00, 0x00, 0x00, 0xc3], c_int) as douglas:
    assert douglas() == 42
```
