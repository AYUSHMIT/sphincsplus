# 🔐 SPHINCS+ Interactive Demo

<div align="center">

![SPHINCS+ Logo](https://img.shields.io/badge/SPHINCS+-Post--Quantum-blueviolet?style=for-the-badge&logo=key)
[![Security Level](https://img.shields.io/badge/Security-Post--Quantum-success?style=for-the-badge)](https://sphincs.org/)
[![NIST PQC](https://img.shields.io/badge/NIST-PQC%20Standard-blue?style=for-the-badge)](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography)

**🚀 Experience the Future of Digital Signatures - Quantum-Resistant Cryptography in Action**

[Try the Demo](#interactive-demo) • [Quick Start](QUICKSTART.md) • [Tutorial](#tutorial) • [Documentation](#documentation)

</div>

---

## 📖 Table of Contents

- [What is SPHINCS+?](#what-is-sphincs)
- [Why Post-Quantum Cryptography?](#why-post-quantum-cryptography)
- [Interactive Demo](#interactive-demo)
- [Architecture Overview](#architecture-overview)
- [Parameter Sets](#parameter-sets)
- [Performance Comparisons](#performance-comparisons)
- [Security Analysis](#security-analysis)
- [Getting Started](#getting-started)
- [Use Cases](#use-cases)

---

## 🎯 What is SPHINCS+?

**SPHINCS+** is a stateless hash-based signature scheme selected by NIST as a **post-quantum cryptography standard**. Unlike RSA and ECDSA, SPHINCS+ signatures remain secure even against attackers with quantum computers.

### Key Features ✨

- **🛡️ Quantum-Resistant**: Based on hash functions, resistant to Shor's algorithm
- **📝 Stateless**: No need to track signature state (unlike XMSS)
- **🔒 Minimal Security Assumptions**: Only relies on the security of hash functions
- **⚙️ Flexible Parameters**: Multiple security levels (128, 192, 256-bit)
- **🎯 Trade-offs**: Choose between smaller signatures (s) or faster signing (f)

---

## 🌍 Why Post-Quantum Cryptography?

```
┌──────────────────────────────────────────────────────────────┐
│  THE QUANTUM THREAT                                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Classical Computer       Quantum Computer                  │
│  ─────────────────       ──────────────────                 │
│                                                              │
│  RSA-2048:  ✅ Secure     ❌ Broken in hours                 │
│  ECDSA:     ✅ Secure     ❌ Broken in hours                 │
│  SPHINCS+:  ✅ Secure     ✅ Still Secure!                   │
│                                                              │
│  Shor's Algorithm (1994) can factor large numbers and       │
│  compute discrete logs efficiently on quantum computers,    │
│  breaking RSA, ECDSA, and Diffie-Hellman.                   │
│                                                              │
│  ⚠️  "Store Now, Decrypt Later" attacks are already        │
│     happening - encrypted data harvested today can be       │
│     decrypted when quantum computers become available.      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Timeline

- **2015**: NIST announces Post-Quantum Cryptography project
- **2017**: SPHINCS+ submitted to NIST PQC competition
- **2022**: SPHINCS+ selected as NIST PQC standard
- **2024**: Draft standards published
- **2025-2030**: Expected widespread adoption

---

## 🎮 Interactive Demo

### 🌐 Web-Based Demo

Experience SPHINCS+ in your browser! No installation required.

```bash
# Open the demo
open demo/index.html
# or
python3 -m http.server 8000
# Then navigate to http://localhost:8000/demo/
```

**Features:**
- 🎨 Interactive parameter selection
- 🔑 Real-time key generation visualization
- ✍️ Message signing with step-by-step animation
- ✅ Signature verification with visual feedback
- 📊 Performance benchmarks and comparisons
- 🌳 Merkle tree visualization

### 💻 Command-Line Demo

For a beautiful terminal experience:

```bash
# Install dependencies
pip install rich cryptography

# Run the interactive CLI demo
python3 demo_cli.py
```

**Features:**
- 🎭 Beautiful TUI with rich formatting
- 📊 Live progress bars and animations
- 🎯 Interactive parameter selection
- 📈 Performance comparisons and charts
- 🌈 Colorful ASCII art visualizations

### 📓 Jupyter Notebook Tutorial

Learn SPHINCS+ interactively:

```bash
# Install Jupyter
pip install jupyter matplotlib numpy

# Launch the tutorial
jupyter notebook tutorial.ipynb
```

---

## 🏗️ Architecture Overview

SPHINCS+ combines several cryptographic building blocks in a hypertree structure:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPHINCS+ ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Message (M)                                                   │
│       │                                                         │
│       ├──► FORS (Few-Time Signature)                           │
│       │     • Generates k-time signature                       │
│       │     • Compresses message digest                        │
│       │     • Output: FORS signature + public key              │
│       │                                                         │
│       └──► Hypertree (WOTS+ chain)                            │
│             • Signs FORS public key                            │
│             • d-layer tree structure                           │
│             • Each node uses WOTS+ (Winternitz OTS)            │
│             • Root is the public key                           │
│                                                                 │
│   ┌─────────────────────────────────────┐                      │
│   │     Layer d-1 (Top)                │                      │
│   │         Root (PK)                   │                      │
│   │            │                        │                      │
│   │      ┌─────┴─────┐                 │                      │
│   │   Layer d-2      ...                │                      │
│   │      │       │                      │                      │
│   │    ┌─┴─┐   ┌─┴─┐                   │                      │
│   │  Layer 1  Layer 1                   │                      │
│   │    │ │     │ │                      │                      │
│   │  ┌─┴─┴─┐ ┌─┴─┴─┐                   │                      │
│   │  Layer 0 Layer 0                    │                      │
│   │  (WOTS+) (WOTS+)                    │                      │
│   └─────────────────────────────────────┘                      │
│                                                                 │
│  Final Signature = FORS_sig || Auth_path || WOTS+_sigs        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

1. **FORS (Forest of Random Subsets)**
   - Few-time signature scheme
   - Signs the message directly
   - Produces a small-time signature

2. **WOTS+ (Winternitz One-Time Signature Plus)**
   - One-time signature scheme
   - Signs FORS public key
   - Hash-based chain signature

3. **Hypertree**
   - Multi-layer tree structure
   - Each layer certified by layer above
   - Root forms the public key

4. **Hash Function Variants**
   - **SHA-256**: Standard, widely trusted
   - **SHAKE256**: Based on SHA-3/Keccak
   - **Haraka**: Optimized for short inputs

---

## ⚙️ Parameter Sets

SPHINCS+ offers **6 main parameter sets** across 3 security levels:

| Parameter Set | Security | n  | h  | d  | Signature Size | Speed | Use Case |
|--------------|----------|----|----|----|--------------:|----|----------|
| **SPHINCS+-128s** | NIST-1 | 16 | 63 | 7  | 7,856 bytes  | ⭐⭐⭐ | 📦 Small signatures |
| **SPHINCS+-128f** | NIST-1 | 16 | 66 | 22 | 17,088 bytes | ⭐⭐⭐⭐⭐ | ⚡ Fast signing |
| **SPHINCS+-192s** | NIST-3 | 24 | 63 | 7  | 16,224 bytes | ⭐⭐⭐ | 📦 Small signatures |
| **SPHINCS+-192f** | NIST-3 | 24 | 66 | 22 | 35,664 bytes | ⭐⭐⭐⭐⭐ | ⚡ Fast signing |
| **SPHINCS+-256s** | NIST-5 | 32 | 64 | 8  | 29,792 bytes | ⭐⭐⭐ | 📦 Small signatures |
| **SPHINCS+-256f** | NIST-5 | 32 | 68 | 17 | 49,856 bytes | ⭐⭐⭐⭐⭐ | ⚡ Fast signing |

### Parameter Meanings

- **n**: Hash output length (security parameter)
- **h**: Total tree height
- **d**: Number of hypertree layers
- **s/f**: Small signature vs Fast signing
- **Security bits**: 128 (equivalent to AES-128), 192, or 256

### Choosing Parameters

```python
# For IoT devices with limited bandwidth → 128s
# For secure messaging apps → 192s
# For long-term document signing → 256s
# For high-throughput servers → 128f/192f/256f
```

---

## 📊 Performance Comparisons

### Signature Size Comparison

```
Classical vs Post-Quantum Signature Sizes:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  RSA-2048:      256 bytes  ████                        │
│  ECDSA-256:      64 bytes  █                           │
│                                                         │
│  SPHINCS+-128s:  7,856 B   ████████████████████████    │
│  SPHINCS+-128f: 17,088 B   ██████████████████████████████████████
│  SPHINCS+-192s: 16,224 B   ██████████████████████████████████████
│  SPHINCS+-192f: 35,664 B   ████████████████████████████████████████████████████
│  SPHINCS+-256s: 29,792 B   ████████████████████████████████████████████████
│  SPHINCS+-256f: 49,856 B   ████████████████████████████████████████████████████████████
│                                                         │
│  ⚠️  Note: Post-quantum signatures are larger, but     │
│     they're quantum-resistant!                         │
└─────────────────────────────────────────────────────────┘
```

### Speed Comparison (operations/second)

```
                  KeyGen    Sign     Verify
SPHINCS+-128s:     ~1,000   ~100     ~5,000
SPHINCS+-128f:     ~1,000   ~500     ~5,000
SPHINCS+-192s:     ~500     ~50      ~2,000
SPHINCS+-192f:     ~500     ~250     ~2,000
SPHINCS+-256s:     ~250     ~25      ~1,000
SPHINCS+-256f:     ~250     ~125     ~1,000

RSA-2048:          ~10      ~1,000   ~50,000
ECDSA-256:         ~10,000  ~10,000  ~5,000
```

---

## 🔒 Security Analysis

### Security Foundations

SPHINCS+ security is based on:

1. **Collision Resistance** of hash functions
2. **Second-Preimage Resistance** of hash functions
3. **Pseudorandomness** of hash function outputs

### Attack Resistance

| Attack Type | Classical | Quantum | SPHINCS+ |
|------------|-----------|---------|----------|
| Brute Force | ✅ Hard | ✅ Hard | ✅ Secure |
| Shor's Algorithm | ❌ Breaks RSA/ECC | ✅ N/A | ✅ Secure |
| Grover's Algorithm | ✅ N/A | ⚠️ Speedup | ✅ Secure* |
| Hash Collision | ✅ Hard | ⚠️ Speedup | ✅ Secure* |

*Parameters account for quantum speedup (Grover's algorithm provides ~√n speedup)

### Security Levels (NIST Categories)

- **NIST-1 (128-bit)**: At least as hard to break as AES-128
- **NIST-3 (192-bit)**: At least as hard to break as AES-192
- **NIST-5 (256-bit)**: At least as hard to break as AES-256

---

## 🚀 Getting Started

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/AYUSHMIT/sphincsplus.git
cd sphincsplus

# Build the reference implementation
cd ref
make PARAMS=sphincs-shake-128s THASH=robust

# Run tests
make test

# Run benchmarks
make benchmark
```

### Basic Usage (C API)

```c
#include "api.h"

int main() {
    unsigned char pk[CRYPTO_PUBLICKEYBYTES];
    unsigned char sk[CRYPTO_SECRETKEYBYTES];
    unsigned char sig[CRYPTO_BYTES];
    unsigned char msg[] = "Hello, Quantum World!";
    size_t siglen;
    
    // Generate keypair
    crypto_sign_keypair(pk, sk);
    
    // Sign message
    crypto_sign_signature(sig, &siglen, msg, sizeof(msg), sk);
    
    // Verify signature
    if (crypto_sign_verify(sig, siglen, msg, sizeof(msg), pk) == 0) {
        printf("✅ Signature valid!\n");
    } else {
        printf("❌ Signature invalid!\n");
    }
    
    return 0;
}
```

For more examples, see [QUICKSTART.md](QUICKSTART.md).

---

## 💡 Use Cases

### 1. 🌐 Secure Software Updates

```
Software vendor signs updates with SPHINCS+
→ Users verify signatures before installation
→ Quantum-safe even 20 years from now
```

### 2. 📜 Long-term Document Signing

```
Legal documents signed with 256s
→ Signatures remain valid for decades
→ Quantum computers won't break them
```

### 3. 🔐 IoT Device Authentication

```
Constrained devices use 128s (smaller signatures)
→ Authenticate to cloud services
→ Quantum-resistant identity
```

### 4. 💬 Secure Messaging

```
End-to-end encrypted chat with SPHINCS+ authentication
→ Message authenticity guaranteed
→ Forward-secure against quantum attacks
```

### 5. 🏛️ Government & Military

```
Classified communications using 256s/256f
→ Maximum security level
→ Future-proof against quantum threats
```

---

## 📚 Additional Resources

### Documentation
- [SPHINCS+ Website](https://sphincs.org/)
- [NIST PQC Project](https://csrc.nist.gov/Projects/Post-Quantum-Cryptography)
- [Specification (PDF)](https://sphincs.org/data/sphincs+-specification.pdf)

### Tutorials
- [Jupyter Notebook Tutorial](tutorial.ipynb)
- [Quick Start Guide](QUICKSTART.md)
- [Web Demo](demo/index.html)
- [CLI Demo](demo_cli.py)

### Visualizations
- [Comparison Charts](visuals/comparison_chart.svg)
- [Security Trade-offs](visuals/security_tradeoffs.svg)
- [Merkle Tree Structure](visuals/merkle_tree.svg)
- [Workflow Diagram](visuals/workflow_diagram.svg)
- [Quantum Threat](visuals/quantum_threat.svg)

---

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- 🎨 Additional visualizations
- 📖 More tutorials and examples
- ⚡ Performance optimizations
- 🧪 Additional test vectors
- 🌍 Translations

---

## 📄 License

This project is released into the public domain. See [LICENSE](LICENSE) for details.

---

<div align="center">

### 🌟 Star this repository if you find it useful!

**Built with ❤️ for a quantum-safe future**

</div>
