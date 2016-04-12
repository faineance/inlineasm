# inlineasm

## Examples

### Machine Code example
```python
# You can also pass machine code as a string "\xb8\x2a\x00\x00\x00\xc3"
with assemble([0xb8, 0x2a, 0x00, 0x00, 0x00, 0xc3], c_int) as douglas:
    assert douglas() == 42
```

### Assembly example
```python
add_asm = '''
bits 64
mov rax, rdi
add rax, rsi
ret
'''
with assemble(add_asm, c_int, c_int, c_int, nasm=True) as add:
    print(add(1, 2))
```
