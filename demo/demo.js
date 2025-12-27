// SPHINCS+ Demo JavaScript
// Interactive demonstration of post-quantum signatures

// Parameter sets configuration
const PARAM_SETS = {
    '128s': {
        name: 'SPHINCS+-128s',
        security: 128,
        n: 16,
        h: 63,
        d: 7,
        pkSize: 32,
        skSize: 64,
        sigSize: 7856,
        signSpeed: 3,
        verifySpeed: 5
    },
    '128f': {
        name: 'SPHINCS+-128f',
        security: 128,
        n: 16,
        h: 66,
        d: 22,
        pkSize: 32,
        skSize: 64,
        sigSize: 17088,
        signSpeed: 5,
        verifySpeed: 5
    },
    '192s': {
        name: 'SPHINCS+-192s',
        security: 192,
        n: 24,
        h: 63,
        d: 7,
        pkSize: 48,
        skSize: 96,
        sigSize: 16224,
        signSpeed: 3,
        verifySpeed: 4
    },
    '192f': {
        name: 'SPHINCS+-192f',
        security: 192,
        n: 24,
        h: 66,
        d: 22,
        pkSize: 48,
        skSize: 96,
        sigSize: 35664,
        signSpeed: 5,
        verifySpeed: 4
    },
    '256s': {
        name: 'SPHINCS+-256s',
        security: 256,
        n: 32,
        h: 64,
        d: 8,
        pkSize: 64,
        skSize: 128,
        sigSize: 29792,
        signSpeed: 3,
        verifySpeed: 4
    },
    '256f': {
        name: 'SPHINCS+-256f',
        security: 256,
        n: 32,
        h: 68,
        d: 17,
        pkSize: 64,
        skSize: 128,
        sigSize: 49856,
        signSpeed: 5,
        verifySpeed: 4
    }
};

// Global state
let currentParams = '128s';
let keyPair = null;
let currentMessage = null;
let currentSignature = null;
let originalMessage = null;

// Utility functions
function randomBytes(length) {
    const array = new Uint8Array(length);
    crypto.getRandomValues(array);
    return array;
}

function bytesToHex(bytes) {
    return Array.from(bytes)
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}

function hexToBytes(hex) {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
    }
    return bytes;
}

function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Simulated SPHINCS+ operations (for demo purposes)
// In production, these would call actual SPHINCS+ C implementation via WebAssembly

async function generateKeyPair(params) {
    const paramSet = PARAM_SETS[params];
    
    // Simulate key generation with random data
    const pk = randomBytes(paramSet.pkSize);
    const sk = randomBytes(paramSet.skSize);
    
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
    
    return {
        publicKey: pk,
        secretKey: sk,
        params: params
    };
}

async function signMessage(message, secretKey, params) {
    const paramSet = PARAM_SETS[params];
    
    // Simulate signing process
    const sig = randomBytes(paramSet.sigSize);
    
    // Simulate processing time based on parameter set
    const delay = paramSet.signSpeed === 5 ? 800 : 2000;
    await new Promise(resolve => setTimeout(resolve, delay + Math.random() * 500));
    
    return sig;
}

async function verifySignature(signature, message, publicKey, params) {
    // Simulate verification process
    await new Promise(resolve => setTimeout(resolve, 300 + Math.random() * 200));
    
    // Check if message or signature has been tampered with
    if (message !== originalMessage) return false;
    if (signature !== currentSignature) return false;
    
    return true;
}

// UI Event Handlers

// Tab navigation
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active content
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById(tabName).classList.add('active');
    });
});

// Parameter selection
document.querySelectorAll('input[name="params"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        currentParams = e.target.value;
        console.log('Selected parameters:', currentParams);
    });
});

// Key Generation
document.getElementById('generateKeysBtn').addEventListener('click', async () => {
    const btn = document.getElementById('generateKeysBtn');
    const progress = document.getElementById('keygenProgress');
    const result = document.getElementById('keygenResult');
    
    // Reset and show progress
    btn.disabled = true;
    result.style.display = 'none';
    progress.style.display = 'block';
    
    try {
        // Generate keys
        keyPair = await generateKeyPair(currentParams);
        
        // Display results
        progress.style.display = 'none';
        result.style.display = 'block';
        
        document.getElementById('publicKeyDisplay').textContent = bytesToHex(keyPair.publicKey);
        document.getElementById('secretKeyDisplay').textContent = bytesToHex(keyPair.secretKey);
        document.getElementById('pkSize').textContent = keyPair.publicKey.length;
        document.getElementById('skSize').textContent = keyPair.secretKey.length;
        
        // Enable signing
        document.getElementById('signBtn').disabled = false;
        
    } catch (error) {
        console.error('Key generation failed:', error);
        alert('Key generation failed. Please try again.');
    } finally {
        btn.disabled = false;
    }
});

// Message Signing
document.getElementById('signBtn').addEventListener('click', async () => {
    if (!keyPair) {
        alert('Please generate keys first!');
        return;
    }
    
    const message = document.getElementById('messageInput').value;
    if (!message) {
        alert('Please enter a message to sign!');
        return;
    }
    
    const btn = document.getElementById('signBtn');
    const progress = document.getElementById('signProgress');
    const result = document.getElementById('signResult');
    
    // Reset and show progress
    btn.disabled = true;
    result.style.display = 'none';
    progress.style.display = 'block';
    
    // Animate signing steps
    const steps = progress.querySelectorAll('.step');
    for (let i = 0; i < steps.length; i++) {
        steps[i].classList.add('active');
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    try {
        const startTime = performance.now();
        
        // Sign message
        const encoder = new TextEncoder();
        const messageBytes = encoder.encode(message);
        currentSignature = await signMessage(messageBytes, keyPair.secretKey, currentParams);
        currentMessage = message;
        originalMessage = message;
        
        const endTime = performance.now();
        const duration = ((endTime - startTime) / 1000).toFixed(3);
        
        // Display results
        steps.forEach(step => step.classList.remove('active'));
        progress.style.display = 'none';
        result.style.display = 'block';
        
        document.getElementById('signatureDisplay').textContent = bytesToHex(currentSignature);
        document.getElementById('sigSize').textContent = formatBytes(currentSignature.length);
        document.getElementById('sigTime').textContent = duration + ' seconds';
        
        // Enable verification
        document.getElementById('verifyBtn').disabled = false;
        document.getElementById('tamperMessageBtn').disabled = false;
        document.getElementById('tamperSigBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;
        
    } catch (error) {
        console.error('Signing failed:', error);
        alert('Signing failed. Please try again.');
    } finally {
        btn.disabled = false;
    }
});

// Signature Verification
document.getElementById('verifyBtn').addEventListener('click', async () => {
    if (!currentSignature || !currentMessage || !keyPair) {
        alert('Please sign a message first!');
        return;
    }
    
    const btn = document.getElementById('verifyBtn');
    const progress = document.getElementById('verifyProgress');
    const result = document.getElementById('verifyResult');
    
    // Reset and show progress
    btn.disabled = true;
    result.style.display = 'none';
    progress.style.display = 'block';
    
    try {
        // Verify signature
        const encoder = new TextEncoder();
        const messageBytes = encoder.encode(currentMessage);
        const isValid = await verifySignature(currentSignature, currentMessage, keyPair.publicKey, currentParams);
        
        // Display results
        progress.style.display = 'none';
        result.style.display = 'block';
        
        const resultContent = result.querySelector('.verify-result-content');
        if (isValid) {
            resultContent.innerHTML = `
                <div class="verify-success">
                    <i class="fas fa-check-circle"></i>
                    <h3>✅ Signature Valid!</h3>
                    <p>The signature is authentic and the message has not been tampered with.</p>
                </div>
            `;
        } else {
            resultContent.innerHTML = `
                <div class="verify-failure">
                    <i class="fas fa-times-circle"></i>
                    <h3>❌ Signature Invalid!</h3>
                    <p>The signature verification failed. The message may have been tampered with or the signature is corrupt.</p>
                </div>
            `;
        }
        
    } catch (error) {
        console.error('Verification failed:', error);
        alert('Verification failed. Please try again.');
    } finally {
        btn.disabled = false;
    }
});

// Tampering buttons
document.getElementById('tamperMessageBtn').addEventListener('click', () => {
    currentMessage = currentMessage + ' [TAMPERED]';
    document.getElementById('messageInput').value = currentMessage;
    alert('Message has been tampered with! Try verifying now.');
});

document.getElementById('tamperSigBtn').addEventListener('click', () => {
    // Corrupt one byte of the signature
    currentSignature[0] ^= 0xFF;
    document.getElementById('signatureDisplay').textContent = bytesToHex(currentSignature);
    alert('Signature has been corrupted! Try verifying now.');
});

document.getElementById('resetBtn').addEventListener('click', () => {
    currentMessage = originalMessage;
    document.getElementById('messageInput').value = originalMessage;
    
    // Regenerate signature
    document.getElementById('signBtn').click();
});

// Comparison Chart
function drawComparisonChart() {
    const canvas = document.getElementById('comparisonChart');
    if (!canvas || !canvas.getContext) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Set styles
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, width, height);
    
    // Draw chart
    const params = Object.keys(PARAM_SETS);
    const barWidth = width / (params.length * 2);
    const maxSigSize = Math.max(...params.map(p => PARAM_SETS[p].sigSize));
    
    ctx.font = '12px Arial';
    ctx.fillStyle = '#ffffff';
    
    params.forEach((param, index) => {
        const paramSet = PARAM_SETS[param];
        const x = (index * 2 + 1) * barWidth;
        const barHeight = (paramSet.sigSize / maxSigSize) * (height - 100);
        const y = height - barHeight - 50;
        
        // Draw bar with gradient
        const gradient = ctx.createLinearGradient(x, y, x, y + barHeight);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#764ba2');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x - barWidth / 2, y, barWidth, barHeight);
        
        // Draw label
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(paramSet.name, x, height - 30);
        ctx.fillText(formatBytes(paramSet.sigSize), x, height - 15);
    });
    
    // Draw title
    ctx.font = 'bold 16px Arial';
    ctx.fillStyle = '#667eea';
    ctx.textAlign = 'center';
    ctx.fillText('Signature Size Comparison', width / 2, 30);
}

// Merkle Tree Visualization
function drawMerkleTree() {
    const canvas = document.getElementById('merkleTreeCanvas');
    if (!canvas || !canvas.getContext) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, width, height);
    
    // Tree parameters
    const levels = 4;
    const nodeRadius = 20;
    const levelHeight = height / (levels + 1);
    
    // Draw tree
    function drawNode(x, y, level, color, label) {
        // Draw circle
        ctx.beginPath();
        ctx.arc(x, y, nodeRadius, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw label
        ctx.fillStyle = '#ffffff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, x, y);
    }
    
    function drawConnection(x1, y1, x2, y2, color) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.stroke();
    }
    
    // Draw level 0 (root)
    const rootX = width / 2;
    const rootY = levelHeight;
    drawNode(rootX, rootY, 0, '#667eea', 'Root');
    
    // Draw level 1
    const level1Y = levelHeight * 2;
    const level1Left = width / 3;
    const level1Right = (2 * width) / 3;
    
    drawConnection(rootX, rootY + nodeRadius, level1Left, level1Y - nodeRadius, '#f093fb');
    drawConnection(rootX, rootY + nodeRadius, level1Right, level1Y - nodeRadius, '#f093fb');
    
    drawNode(level1Left, level1Y, 1, '#f093fb', 'L1');
    drawNode(level1Right, level1Y, 1, '#f093fb', 'R1');
    
    // Draw level 2
    const level2Y = levelHeight * 3;
    for (let i = 0; i < 4; i++) {
        const x = (width / 5) * (i + 1);
        const parentX = i < 2 ? level1Left : level1Right;
        
        drawConnection(parentX, level1Y + nodeRadius, x, level2Y - nodeRadius, '#4facfe');
        drawNode(x, level2Y, 2, '#4facfe', `N${i}`);
    }
    
    // Draw level 3 (leaves)
    const level3Y = levelHeight * 4;
    for (let i = 0; i < 8; i++) {
        const x = (width / 9) * (i + 1);
        const parentX = (width / 5) * (Math.floor(i / 2) + 1);
        
        drawConnection(parentX, level2Y + nodeRadius, x, level3Y - nodeRadius, '#43e97b');
        drawNode(x, level3Y, 3, '#43e97b', `L${i}`);
    }
    
    // Draw title
    ctx.font = 'bold 16px Arial';
    ctx.fillStyle = '#667eea';
    ctx.textAlign = 'center';
    ctx.fillText('SPHINCS+ Hypertree Structure', width / 2, 30);
}

// Reset visualization
document.getElementById('resetVisualization')?.addEventListener('click', () => {
    drawMerkleTree();
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('SPHINCS+ Demo initialized');
    
    // Draw visualizations
    setTimeout(() => {
        drawComparisonChart();
        drawMerkleTree();
    }, 500);
    
    // Handle window resize
    window.addEventListener('resize', () => {
        drawComparisonChart();
        drawMerkleTree();
    });
});
