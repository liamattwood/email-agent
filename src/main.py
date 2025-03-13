from dotenv import load_dotenv
from agents import Runner
import sys
import argparse
import json
import re
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
import os
import traceback
from src.config.user_config import set_user_name, set_email_style, add_contact, get_user_name, get_email_style, get_all_contacts
from agents import enable_verbose_stdout_logging


# Load environment variables from .env file
load_dotenv()

PRIVACY_MODE = False
VERBOSE_MODE = False

def censor_email(text):
    """Censor email addresses in text if privacy mode is enabled."""
    if not PRIVACY_MODE:
        return text
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    def censor(match):
        email = match.group(0)
        username, domain = email.split('@')
        censored_username = '*' * len(username)
        return f"{censored_username}@{domain}"
    
    return re.sub(email_pattern, censor, text)

def format_agent_response(response):
    """Format the agent's response for display."""
    censored_response = censor_email(response)
    
    console = Console()
    console.print(Panel(
        Markdown(censored_response),
        title="Agent Response",
        border_style="green"
    ))

def run_agent(prompt):
    """Run the agent with the given prompt and display progress."""
    console = Console()
    
    try:
        from src.agents.agent_config import create_email_agent
        
        import smtplib
        smtplib.SMTP.debuglevel = 0
        smtplib.SMTP_SSL.debuglevel = 0
        
        if VERBOSE_MODE:
            enable_verbose_stdout_logging()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Running email agent...[/bold green]"),
            transient=True,
        ) as progress:
            progress.add_task("", total=None)
            agent = create_email_agent()
            
            # Run the agent with the prompt
            result = Runner.run_sync(agent, prompt)
        
        # Display the result
        format_agent_response(result.final_output)
        
    except EnvironmentError as e:
        console.print(f"[bold red]Environment Error:[/bold red] {e}")
        console.print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if VERBOSE_MODE:
            traceback.print_exc()
        sys.exit(1)

def configure_user_settings():
    """Interactive configuration of user settings."""
    console = Console()
    console.print(Panel(
        "User Configuration",
        title="Email Agent Settings",
        border_style="blue"
    ))
    
    current_name = get_user_name()
    current_style = get_email_style()
    
    console.print(f"Current name: [cyan]{current_name}[/cyan]")
    new_name = Prompt.ask("Enter your name", default=current_name)
    if new_name != current_name:
        set_user_name(new_name)
        console.print(f"Name updated to: [green]{new_name}[/green]")
    
    console.print(f"Current email style: [cyan]{current_style}[/cyan]")
    console.print("Available styles: professional, casual, formal, friendly")
    new_style = Prompt.ask("Enter preferred email style", default=current_style)
    if new_style != current_style:
        set_email_style(new_style)
        console.print(f"Email style updated to: [green]{new_style}[/green]")
    
    contacts = get_all_contacts()
    if contacts:
        console.print("\n[bold]Current Contacts:[/bold]")
        for name, email in contacts.items():
            censored_email = censor_email(email)
            console.print(f"- [cyan]{name}[/cyan]: {censored_email}")
    
    while True:
        add_more = Prompt.ask("\nAdd a new contact? (yes/no)", default="no")
        if add_more.lower() not in ["yes", "y"]:
            break
        
        contact_name = Prompt.ask("Contact name")
        contact_email = Prompt.ask("Contact email")
        add_contact(contact_name, contact_email)
        console.print(f"Added contact: [green]{contact_name}[/green]")

def main():
    global PRIVACY_MODE
    global VERBOSE_MODE
    
    parser = argparse.ArgumentParser(description="Email Agent CLI")
    parser.add_argument("--prompt", "-p", type=str, help="Email request prompt")
    parser.add_argument("--privacy", action="store_true", help="Enable privacy mode (censor email addresses)")
    parser.add_argument("--configure", action="store_true", help="Configure user settings")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed agent steps")
    args = parser.parse_args()
    
    console = Console()
    
    PRIVACY_MODE = args.privacy
    VERBOSE_MODE = args.verbose
    
    if PRIVACY_MODE:
        console.print("[yellow]Privacy mode enabled - email addresses will be censored[/yellow]")
    
    if VERBOSE_MODE:
        console.print("[yellow]Verbose mode enabled - showing detailed agent steps[/yellow]")
    
    if args.configure:
        configure_user_settings()
        return
    
    if args.prompt:
        run_agent(args.prompt)
        return
    
    console.print(Panel(
        "Welcome to the Email Agent CLI!",
        title="Email Agent",
        border_style="blue"
    ))
    
    while True:
        try:
            prompt = console.input("\n[bold cyan]Enter your email request (or 'exit' to quit, 'config' to configure):[/bold cyan] ")
            
            if prompt.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if prompt.lower() in ['config', 'configure', 'settings']:
                configure_user_settings()
                continue
            
            run_agent(prompt)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            break

if __name__ == "__main__":
    main() 