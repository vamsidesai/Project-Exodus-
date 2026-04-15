import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.state import ModeState
from core.rules import RulesEngine, RuleViolation
from core.guardian import Guardian
from memory.vault import IdentityVault

# Initialize System
console = Console()
state = ModeState()
rules = RulesEngine()
guardian = Guardian()
vault = IdentityVault()

def boot_sequence():
    console.print(Panel.fit("[bold cyan]PROJECT EXODUS[/bold cyan] v0.1\n[dim]Initializing Kernel...[/dim]", border_style="cyan"))
    # Verify environment (Mock)
    state.mode = "OTHERS" # Default start
    console.print("[green]✔[/green] Kernel Active")
    console.print("[green]✔[/green] Guardian Active")
    console.print("[yellow]![/yellow] Mode: [bold]OTHERS[/bold] (Protected)")

def main_loop():
    while True:
        try:
            # 1. INPUT
            user_input = Prompt.ask(f"\n[bold { 'cyan' if state.mode == 'MASTER' else 'white' }]EXODUS[/] >")
            
            if user_input.lower() in ["exit", "quit", "shutdown"]:
                console.print("[bold red]Shutting down...[/bold red]")
                break
            
            # 2. GUARDIAN PRE-CHECK (Drift)
            if guardian.check_drift(user_input, []):
                console.print("[bold red]⚠ SYSTEM ALERT: Emotional Drift Detected. Enforcing Rule-Based Fallback.[/bold red]")
                # Trigger Safe Mode?
                # state.safe_mode = True 
                
            # 3. RULES CHECK
            rules.enforce(state, user_input)
            
            # 4. COMMAND HANDLING (Simple V1)
            if user_input.startswith("/"):
                handle_command(user_input)
                continue
            
            # 5. OUTPUT GENERATION (Mock LLM interaction for now)
            # In real implementation, this calls 'brain.py' -> Ollama
            response = "I am listening." 
            if state.mode == "MASTER":
                response = f"Yes, Boss. Processed: {user_input}"
            else:
                response = f"Input received: {user_input}"

            # 6. GUARDIAN POST-CHECK
            safe_response = guardian.validate_output(state, response)
            
            console.print(f"[dim]>>[/dim] {safe_response}")

        except RuleViolation as e:
            console.print(f"[bold red]⛔ RULE VIOLATION:[/bold red] {e}")
        except Exception as e:
            console.print(f"[bold red]ERROR:[/bold red] {e}")

def handle_command(cmd_str):
    parts = cmd_str.split(" ")
    cmd = parts[0]
    
    if cmd == "/auth":
        if len(parts) > 1 and parts[1] == "exodus_init":
            state.mode = "MASTER"
            vault.unlock(parts[1], state)
            console.print("[bold green]ACCESS GRANTED: MASTER MODE ENGAGED[/bold green]")
        else:
            console.print("[bold red]ACCESS DENIED[/bold red]")
    elif cmd == "/lock":
        state.reset()
        console.print("[bold yellow]SYSTEM LOCKED. REVERTING TO OTHERS MODE.[/bold yellow]")
    elif cmd == "/status":
        console.print(state.to_dict())

if __name__ == "__main__":
    boot_sequence()
    main_loop()
