def xor_stream_cipher(data: bytes, key: bytes) -> bytes:
    out = bytearray()
    key_len = len(key)
    for i, b in enumerate(data):
        out.append(b ^ key[i % key_len])
    return bytes(out)

# Example usage
key = b"mysecretkey"          
message = b"Hello JOga!"

cipher = xor_stream_cipher(message, key)
plain  = xor_stream_cipher(cipher,  key)

print("Cipher (hex):", cipher.hex())
print("Decrypted:", plain)