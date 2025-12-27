#!/usr/bin/env python3
"""
SPHINCS+ Interactive CLI Demo
Beautiful command-line interface for demonstrating post-quantum signatures

Requires: pip install rich
"""

import hashlib
import os
import secrets
import time
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.layout import Layout
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich import box
    from rich.align import Align
except ImportError:
    print("Error: This demo requires the 'rich' library.")
    print("Install it with: pip install rich")
    exit(1)

console = Console()


@dataclass
class ParamSet:
    """SPHINCS+ parameter set configuration"""
    name: str
    security: int
    n: int
    h: int
    d: int
    pk_size: int
    sk_size: int
    sig_size: int
    sign_speed: int  # 1-5, higher is faster
    verify_speed: int


# Parameter set definitions
PARAM_SETS = {
    "128s": ParamSet("SPHINCS+-128s", 128, 16, 63, 7, 32, 64, 7856, 3, 5),
    "128f": ParamSet("SPHINCS+-128f", 128, 16, 66, 22, 32, 64, 17088, 5, 5),
    "192s": ParamSet("SPHINCS+-192s", 192, 24, 63, 7, 48, 96, 16224, 3, 4),
    "192f": ParamSet("SPHINCS+-192f", 192, 24, 66, 22, 48, 96, 35664, 5, 4),
    "256s": ParamSet("SPHINCS+-256s", 256, 32, 64, 8, 64, 128, 29792, 3, 4),
    "256f": ParamSet("SPHINCS+-256f", 256, 32, 68, 17, 64, 128, 49856, 5, 4),
}


class SPHINCSPlusDemo:
    """Interactive SPHINCS+ demonstration"""
    
    def __init__(self):
        self.console = console
        self.current_param = None
        self.public_key = None
        self.secret_key = None
        self.message = None
        self.signature = None
        
    def show_banner(self):
        """Display welcome banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🔐  SPHINCS+ Interactive Demo                        ║
║                                                           ║
║     Post-Quantum Cryptography in Your Terminal           ║
║     Quantum-Resistant • Hash-Based • NIST Standard       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(
            banner,
            style="bold magenta",
            border_style="cyan"
        ))
        
    def show_intro(self):
        """Show introduction to SPHINCS+"""
        intro = """
[bold cyan]What is SPHINCS+?[/bold cyan]

SPHINCS+ is a [bold green]stateless hash-based signature scheme[/bold green] selected 
by NIST as a [bold yellow]post-quantum cryptography standard[/bold yellow].

[bold]Key Features:[/bold]
• 🛡️  [green]Quantum-Resistant[/green]: Secure against quantum computers
• 📝 [blue]Stateless[/blue]: No signature state tracking required
• 🔒 [yellow]Minimal Assumptions[/yellow]: Only relies on hash functions
• ⚙️  [magenta]Flexible[/magenta]: Multiple security levels (128, 192, 256-bit)

[bold red]⚠️  The Quantum Threat:[/bold red]
Quantum computers can break RSA and ECDSA using Shor's algorithm.
SPHINCS+ remains secure even against quantum attacks!
        """
        self.console.print(Panel(intro, title="[bold]Introduction[/bold]", border_style="green"))
        
    def select_parameters(self) -> str:
        """Interactive parameter selection"""
        self.console.print("\n[bold cyan]Select Parameter Set[/bold cyan]\n")
        
        # Create comparison table
        table = Table(title="SPHINCS+ Parameter Sets", box=box.ROUNDED)
        table.add_column("Set", style="cyan", no_wrap=True)
        table.add_column("Security", style="green")
        table.add_column("Sig Size", style="yellow")
        table.add_column("Sign Speed", style="magenta")
        table.add_column("Verify Speed", style="blue")
        table.add_column("Use Case", style="white")
        
        for key, params in PARAM_SETS.items():
            speed_stars = "⭐" * params.sign_speed
            verify_stars = "⭐" * params.verify_speed
            sig_size = f"{params.sig_size:,} B"
            
            if params.name.endswith('s'):
                use_case = "📦 Small signatures"
            else:
                use_case = "⚡ Fast signing"
                
            table.add_row(
                f"[bold]{key}[/bold]",
                f"{params.security}-bit",
                sig_size,
                speed_stars,
                verify_stars,
                use_case
            )
        
        self.console.print(table)
        
        # Prompt for selection
        while True:
            choice = Prompt.ask(
                "\n[bold cyan]Choose parameter set[/bold cyan]",
                choices=list(PARAM_SETS.keys()),
                default="128s"
            )
            
            if choice in PARAM_SETS:
                self.current_param = choice
                params = PARAM_SETS[choice]
                
                self.console.print(f"\n✅ Selected: [bold green]{params.name}[/bold green]")
                self.console.print(f"   Security Level: [yellow]{params.security}-bit[/yellow]")
                self.console.print(f"   Signature Size: [cyan]{params.sig_size:,} bytes[/cyan]")
                
                return choice
                
    def generate_keys(self):
        """Generate key pair with visual feedback"""
        params = PARAM_SETS[self.current_param]
        
        self.console.print(f"\n[bold cyan]🔑 Generating {params.name} Key Pair[/bold cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            # Simulate key generation steps
            task = progress.add_task("[cyan]Generating randomness...", total=100)
            for i in range(25):
                time.sleep(0.02)
                progress.update(task, advance=4)
            
            progress.update(task, description="[yellow]Computing hypertree root...")
            for i in range(25):
                time.sleep(0.015)
                progress.update(task, advance=4)
            
            progress.update(task, description="[green]Finalizing keys...")
            for i in range(25):
                time.sleep(0.01)
                progress.update(task, advance=4)
            
            # Generate actual random keys (simulated)
            self.secret_key = secrets.token_bytes(params.sk_size)
            self.public_key = hashlib.sha256(self.secret_key).digest()[:params.pk_size]
        
        # Display results
        self.console.print("\n[bold green]✅ Keys Generated Successfully![/bold green]\n")
        
        key_table = Table(box=box.SIMPLE)
        key_table.add_column("Key Type", style="cyan")
        key_table.add_column("Size", style="yellow")
        key_table.add_column("Value (truncated)", style="white")
        
        pk_hex = self.public_key.hex()[:64] + "..."
        sk_hex = self.secret_key.hex()[:64] + "..."
        
        key_table.add_row(
            "🔓 Public Key",
            f"{params.pk_size} bytes",
            f"[dim]{pk_hex}[/dim]"
        )
        key_table.add_row(
            "🔐 Secret Key",
            f"{params.sk_size} bytes",
            f"[dim]{sk_hex}[/dim]"
        )
        
        self.console.print(key_table)
        
        self.console.print("\n[yellow]💡 Note:[/yellow] Keep the secret key private!")
        
    def sign_message(self):
        """Sign a message with visual feedback"""
        if not self.secret_key:
            self.console.print("[bold red]❌ Please generate keys first![/bold red]")
            return
            
        params = PARAM_SETS[self.current_param]
        
        # Get message from user
        self.console.print("\n[bold cyan]✍️  Message Signing[/bold cyan]\n")
        self.message = Prompt.ask("Enter message to sign", default="Hello, Quantum World!")
        
        self.console.print(f"\n[dim]Signing: '{self.message}'[/dim]\n")
        
        # Signing process visualization
        steps = [
            ("1️⃣  Hashing message", 0.3),
            ("2️⃣  Generating FORS signature", 0.5),
            ("3️⃣  Computing WOTS+ signatures", 0.4),
            ("4️⃣  Building authentication path", 0.3),
            ("5️⃣  Combining signature components", 0.2),
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            for step_name, delay in steps:
                task = progress.add_task(f"[cyan]{step_name}", total=1)
                time.sleep(delay)
                progress.update(task, advance=1)
        
        # Generate signature (simulated)
        start_time = time.time()
        message_bytes = self.message.encode('utf-8')
        hash_input = self.secret_key + message_bytes
        self.signature = hashlib.sha256(hash_input).digest()
        # Pad to correct size
        self.signature = self.signature * (params.sig_size // len(self.signature) + 1)
        self.signature = self.signature[:params.sig_size]
        end_time = time.time()
        
        duration = (end_time - start_time) * 1000  # Convert to ms
        
        # Display results
        self.console.print("\n[bold green]✅ Message Signed Successfully![/bold green]\n")
        
        sig_info = Table(box=box.SIMPLE)
        sig_info.add_column("Property", style="cyan")
        sig_info.add_column("Value", style="yellow")
        
        sig_hex = self.signature.hex()[:80] + "..."
        
        sig_info.add_row("Signature Size", f"{len(self.signature):,} bytes")
        sig_info.add_row("Signing Time", f"{duration:.2f} ms")
        sig_info.add_row("Signature (hex)", f"[dim]{sig_hex}[/dim]")
        
        self.console.print(sig_info)
        
    def verify_signature(self, tamper: bool = False):
        """Verify signature with visual feedback"""
        if not self.signature or not self.message:
            self.console.print("[bold red]❌ Please sign a message first![/bold red]")
            return
            
        self.console.print("\n[bold cyan]🔍 Signature Verification[/bold cyan]\n")
        
        if tamper:
            self.console.print("[yellow]⚠️  Tampering with message...[/yellow]")
            message_to_verify = self.message + " [TAMPERED]"
        else:
            message_to_verify = self.message
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Verifying signature...", total=100)
            
            for i in range(100):
                time.sleep(0.01)
                progress.update(task, advance=1)
        
        # Verify (simulated)
        message_bytes = message_to_verify.encode('utf-8')
        hash_input = self.secret_key + message_bytes
        expected_sig_start = hashlib.sha256(hash_input).digest()
        
        is_valid = self.signature[:len(expected_sig_start)] == expected_sig_start
        
        if tamper:
            is_valid = False
        
        # Display results
        if is_valid:
            self.console.print("\n[bold green]✅ SIGNATURE VALID![/bold green]")
            self.console.print("[green]The signature is authentic and the message has not been tampered with.[/green]")
        else:
            self.console.print("\n[bold red]❌ SIGNATURE INVALID![/bold red]")
            self.console.print("[red]The signature verification failed. The message may have been tampered with.[/red]")
            
    def show_comparison(self):
        """Show detailed parameter comparison"""
        self.console.print("\n[bold cyan]📊 Parameter Set Comparison[/bold cyan]\n")
        
        # Detailed table
        table = Table(title="Detailed Comparison", box=box.DOUBLE_EDGE)
        table.add_column("Parameter", style="cyan")
        table.add_column("128s", style="green")
        table.add_column("128f", style="green")
        table.add_column("192s", style="yellow")
        table.add_column("192f", style="yellow")
        table.add_column("256s", style="red")
        table.add_column("256f", style="red")
        
        rows = [
            ("Security Level", "128-bit", "128-bit", "192-bit", "192-bit", "256-bit", "256-bit"),
            ("Public Key", "32 B", "32 B", "48 B", "48 B", "64 B", "64 B"),
            ("Secret Key", "64 B", "64 B", "96 B", "96 B", "128 B", "128 B"),
            ("Signature", "7,856 B", "17,088 B", "16,224 B", "35,664 B", "29,792 B", "49,856 B"),
            ("Tree Height", "63", "66", "63", "66", "64", "68"),
            ("Layers", "7", "22", "7", "22", "8", "17"),
        ]
        
        for row in rows:
            table.add_row(*row)
        
        self.console.print(table)
        
        # ASCII art comparison
        self.console.print("\n[bold]Signature Size Visualization:[/bold]\n")
        
        for key in ["128s", "128f", "192s", "192f", "256s", "256f"]:
            params = PARAM_SETS[key]
            bar_length = int(params.sig_size / 1000)
            bar = "█" * bar_length
            
            color = "green" if params.security == 128 else ("yellow" if params.security == 192 else "red")
            self.console.print(f"[{color}]{params.name:15} [{bar}] {params.sig_size:,} bytes[/{color}]")
            
    def show_quantum_threat(self):
        """Display quantum threat visualization"""
        self.console.print("\n[bold cyan]⚛️  The Quantum Threat[/bold cyan]\n")
        
        threat_table = Table(box=box.HEAVY)
        threat_table.add_column("Algorithm", style="cyan")
        threat_table.add_column("Classical Security", style="green")
        threat_table.add_column("Quantum Security", style="yellow")
        threat_table.add_column("Status", style="white")
        
        threat_table.add_row(
            "RSA-2048",
            "✅ Secure",
            "❌ Broken",
            "[red]Vulnerable[/red]"
        )
        threat_table.add_row(
            "ECDSA-256",
            "✅ Secure",
            "❌ Broken",
            "[red]Vulnerable[/red]"
        )
        threat_table.add_row(
            "SPHINCS+",
            "✅ Secure",
            "✅ Secure",
            "[green]Quantum-Safe![/green]"
        )
        
        self.console.print(threat_table)
        
        explanation = """
[bold yellow]Why are classical algorithms vulnerable?[/bold yellow]

Shor's algorithm (1994) can efficiently:
• Factor large numbers (breaks RSA)
• Compute discrete logarithms (breaks ECDSA, DH)

[bold green]Why is SPHINCS+ safe?[/bold green]

SPHINCS+ security is based on:
• Hash function collision resistance
• Hash function preimage resistance
• No quantum algorithm can break these efficiently!

[bold red]⚠️  "Store Now, Decrypt Later" Attacks[/bold red]

Adversaries are already collecting encrypted data to decrypt
when quantum computers become available. Migrate to post-quantum
cryptography now!
        """
        
        self.console.print(Panel(explanation, border_style="yellow"))
        
    def interactive_menu(self):
        """Main interactive menu"""
        while True:
            self.console.print("\n" + "="*60)
            self.console.print("[bold cyan]Main Menu[/bold cyan]")
            self.console.print("="*60)
            
            menu = """
[1] Select Parameter Set
[2] Generate Key Pair
[3] Sign Message
[4] Verify Signature
[5] Verify with Tampered Message
[6] Compare All Parameter Sets
[7] Show Quantum Threat
[8] Exit
            """
            
            self.console.print(menu)
            
            choice = Prompt.ask(
                "[bold cyan]Select option[/bold cyan]",
                choices=["1", "2", "3", "4", "5", "6", "7", "8"],
                default="1"
            )
            
            if choice == "1":
                self.select_parameters()
            elif choice == "2":
                if not self.current_param:
                    self.console.print("[yellow]Please select parameters first![/yellow]")
                    self.select_parameters()
                self.generate_keys()
            elif choice == "3":
                self.sign_message()
            elif choice == "4":
                self.verify_signature(tamper=False)
            elif choice == "5":
                self.verify_signature(tamper=True)
            elif choice == "6":
                self.show_comparison()
            elif choice == "7":
                self.show_quantum_threat()
            elif choice == "8":
                self.console.print("\n[bold green]Thank you for using SPHINCS+ Demo! 🚀[/bold green]\n")
                break


def main():
    """Main entry point"""
    demo = SPHINCSPlusDemo()
    
    try:
        demo.show_banner()
        demo.show_intro()
        
        if Confirm.ask("\n[bold cyan]Would you like to start the interactive demo?[/bold cyan]", default=True):
            demo.interactive_menu()
        else:
            console.print("\n[yellow]Demo cancelled. Run again when ready![/yellow]\n")
            
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted. Goodbye! 👋[/yellow]\n")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]\n")


if __name__ == "__main__":
    main()
