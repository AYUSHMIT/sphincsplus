# 🚀 SPHINCS+ Quick Start Guide

Get up and running with SPHINCS+ post-quantum signatures in **5 minutes**!

---

## 📋 Prerequisites

- GCC or Clang compiler
- Make
- Python 3.6+ (for demos)
- Basic understanding of cryptography (helpful but not required)

---

## ⚡ 5-Minute Quick Start

### Step 1: Clone and Build (2 minutes)

```bash
# Clone the repository
git clone https://github.com/AYUSHMIT/sphincsplus.git
cd sphincsplus/ref

# Build with default parameters (SHAKE-128f)
make

# Run a quick test
make test
```

**Expected output:**
```
✅ All tests passed!
```

### Step 2: Generate Your First Key Pair (1 minute)

```bash
# Build the test program
make tests

# Run the SPHINCS+ test
./test/spx
```

**What happens:**
- Generates a key pair
- Signs a test message
- Verifies the signature
- ✅ Confirms everything works!

### Step 3: Try Different Parameters (1 minute)

```bash
# Small signatures (7.8 KB)
make clean
make PARAMS=sphincs-shake-128s THASH=robust
./test/spx

# Fast signing (17 KB signatures)
make clean
make PARAMS=sphincs-shake-128f THASH=robust
./test/spx

# Maximum security (256-bit, 29.8 KB)
make clean
make PARAMS=sphincs-shake-256s THASH=robust
./test/spx
```

### Step 4: Run Benchmarks (1 minute)

```bash
make benchmarks
./test/benchmark
```

**You'll see:**
```
keypair: X cycles
sign: Y cycles
verify: Z cycles
```

---

## 🎯 Common Use Cases

### Use Case 1: Sign a Message

Create `sign_example.c`:

```c
#include <stdio.h>
#include <string.h>
#include "api.h"

int main() {
    unsigned char pk[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk[CRYPTO_SECRETKEYBYTES];
    unsigned char sig[CRYPTO_BYTES];
    unsigned char message[] = "Hello, Quantum World!";
    size_t siglen;
    
    printf("🔑 Generating key pair...\n");
    crypto_sign_keypair(pk, sk);
    printf("✅ Keys generated!\n");
    printf("   Public key size: %llu bytes\n", crypto_sign_publickeybytes());
    printf("   Secret key size: %llu bytes\n", crypto_sign_secretkeybytes());
    
    printf("\n✍️  Signing message: \"%s\"\n", message);
    crypto_sign_signature(sig, &siglen, message, strlen((char*)message), sk);
    printf("✅ Signature created!\n");
    printf("   Signature size: %zu bytes\n", siglen);
    
    printf("\n🔍 Verifying signature...\n");
    if (crypto_sign_verify(sig, siglen, message, strlen((char*)message), pk) == 0) {
        printf("✅ Signature is VALID!\n");
    } else {
        printf("❌ Signature is INVALID!\n");
    }
    
    return 0;
}
```

**Compile and run:**
```bash
gcc sign_example.c $(ls *.c | grep -v PQCgenKAT | grep -v test/) \
    -o sign_example -DPARAMS=sphincs-shake-128s
./sign_example
```

### Use Case 2: File Signing

Create `sign_file.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "api.h"

int main(int argc, char **argv) {
    if (argc != 3) {
        printf("Usage: %s <file> <signature_output>\n", argv[0]);
        return 1;
    }
    
    unsigned char pk[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk[CRYPTO_SECRETKEYBYTES];
    unsigned char sig[CRYPTO_BYTES];
    size_t siglen;
    
    // Read file
    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        printf("❌ Cannot open file: %s\n", argv[1]);
        return 1;
    }
    
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    unsigned char *content = malloc(fsize);
    fread(content, 1, fsize, f);
    fclose(f);
    
    // Generate keys
    printf("🔑 Generating key pair...\n");
    crypto_sign_keypair(pk, sk);
    
    // Sign
    printf("✍️  Signing file: %s (%ld bytes)\n", argv[1], fsize);
    crypto_sign_signature(sig, &siglen, content, fsize, sk);
    
    // Save signature
    FILE *sigfile = fopen(argv[2], "wb");
    fwrite(sig, 1, siglen, sigfile);
    fclose(sigfile);
    
    printf("✅ Signature saved to: %s\n", argv[2]);
    printf("   Signature size: %zu bytes\n", siglen);
    
    free(content);
    return 0;
}
```

**Compile and use:**
```bash
gcc sign_file.c $(ls *.c | grep -v PQCgenKAT | grep -v test/) \
    -o sign_file -DPARAMS=sphincs-shake-128s

# Sign any file
./sign_file README.md signature.bin
```

### Use Case 3: Key Generation with Seed

```c
#include <stdio.h>
#include <string.h>
#include "api.h"

int main() {
    unsigned char pk[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk[CRYPTO_SECRETKEYBYTES];
    unsigned char seed[CRYPTO_SEEDBYTES];
    
    // Use a deterministic seed (DON'T DO THIS IN PRODUCTION!)
    memset(seed, 0x42, CRYPTO_SEEDBYTES);
    
    printf("🌱 Generating key pair from seed...\n");
    crypto_sign_seed_keypair(pk, sk, seed);
    printf("✅ Keys generated!\n");
    
    // Same seed always produces same keys
    unsigned char pk2[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk2[CRYPTO_SECRETKEYBYTES];
    crypto_sign_seed_keypair(pk2, sk2, seed);
    
    if (memcmp(pk, pk2, CRYPTO_PUBLICKEYBYTES) == 0) {
        printf("✅ Deterministic generation confirmed!\n");
    }
    
    return 0;
}
```

---

## 🎨 Interactive Demos

### Web Demo (No Installation!)

```bash
# Open in browser
cd demo
python3 -m http.server 8000

# Navigate to: http://localhost:8000/
```

**Features:**
- Interactive parameter selection
- Visual key generation
- Step-by-step signing process
- Merkle tree visualization
- Performance charts

### CLI Demo (Beautiful Terminal UI)

```bash
# Install dependencies
pip3 install rich

# Run interactive demo
python3 demo_cli.py
```

**Features:**
- Beautiful text-based UI
- Live progress bars
- Parameter comparisons
- ASCII art visualizations

### Jupyter Tutorial

```bash
# Install Jupyter
pip3 install jupyter matplotlib numpy

# Launch tutorial
jupyter notebook tutorial.ipynb
```

---

## 📊 Parameter Selection Guide

### Which parameters should I use?

```
┌─────────────────────────────────────────────────────────┐
│  DECISION TREE                                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Need maximum security?                                 │
│    └─ YES → Use 256s or 256f                           │
│    └─ NO ↓                                             │
│                                                         │
│  Bandwidth/storage constrained?                         │
│    └─ YES → Use XXXs (small signatures)                │
│    └─ NO → Use XXXf (fast signing)                     │
│                                                         │
│  What security level?                                   │
│    └─ Standard (like AES-128) → 128s/f                 │
│    └─ High (like AES-192) → 192s/f                     │
│    └─ Maximum (like AES-256) → 256s/f                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Quick Reference

| If you need... | Use | Example |
|---------------|-----|---------|
| Smallest signatures | 128s | IoT devices, mobile apps |
| Fastest signing | 128f | High-throughput servers |
| Good balance | 192s | General applications |
| Maximum security | 256s/256f | Long-term archives, critical systems |

---

## 🔍 Troubleshooting

### Problem: Build fails with "command not found"

**Solution:**
```bash
# Install build tools (Ubuntu/Debian)
sudo apt-get install build-essential

# Install build tools (macOS)
xcode-select --install
```

### Problem: "undefined reference" errors

**Solution:**
Make sure you're linking all required source files:
```bash
# For shake parameters
gcc your_code.c address.c randombytes.c merkle.c wots.c wotsx1.c \
    utils.c utilsx1.c fors.c sign.c fips202.c hash_shake.c \
    thash_shake_robust.c -o your_program
```

### Problem: Slow performance

**Solution:**
1. Use optimized implementations: `sha2-avx2`, `shake-avx2`, or `haraka-aesni`
2. Use "f" (fast) variants instead of "s" (small)
3. Enable compiler optimizations: `-O3`

### Problem: Signature verification fails

**Solution:**
- Ensure you're using the same parameters for signing and verification
- Check that public/secret keys haven't been corrupted
- Verify message hasn't been modified

---

## 📚 Next Steps

### Learn More
- 📖 Read [DEMO.md](DEMO.md) for comprehensive overview
- 🎓 Complete [tutorial.ipynb](tutorial.ipynb)
- 🌐 Try [web demo](demo/index.html)
- 💻 Explore [CLI demo](demo_cli.py)

### Explore Advanced Topics
- Parameter set selection and trade-offs
- Integration with TLS/SSH
- Hardware acceleration
- Side-channel protection
- Hybrid signatures (classical + post-quantum)

### Benchmarking
```bash
# Full benchmark suite
python3 benchmark.py

# Generate test vectors
python3 vectors.py
```

---

## 🆘 Getting Help

- 📖 [Full Documentation](https://sphincs.org/)
- 🐛 [Report Issues](https://github.com/AYUSHMIT/sphincsplus/issues)
- 💬 [Discussions](https://github.com/AYUSHMIT/sphincsplus/discussions)
- 📧 Contact maintainers

---

## ✅ Checklist

Before moving to production:

- [ ] Understand security requirements
- [ ] Choose appropriate parameter set
- [ ] Test key generation
- [ ] Test signing/verification
- [ ] Benchmark performance
- [ ] Review security considerations
- [ ] Implement proper key storage
- [ ] Plan for key rotation
- [ ] Test error handling
- [ ] Review integration points

---

## 🎉 Success!

You're now ready to use SPHINCS+ post-quantum signatures!

**Remember:**
- 🔐 Keep secret keys secret
- 🌐 Public keys can be shared freely
- 📝 Each signature proves authenticity
- ⚛️ You're quantum-safe!

---

<div align="center">

**Happy signing! 🚀**

[Back to Main README](README.md) | [View Demo](DEMO.md)

</div>
