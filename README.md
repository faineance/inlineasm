# inlineasm

## Examples

### Machine Code Example
```python
# You can also pass machine code as a string "\xb8\x2a\x00\x00\x00\xc3"
with assemble([0xb8, 0x2a, 0x00, 0x00, 0x00, 0xc3], c_int) as douglas:
    assert douglas() == 42
```

### 
