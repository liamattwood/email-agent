import os
import re
from agents import Agent, function_tool
from src.services.email_service import send_email
from src.config.user_config import (
    get_user_name, 
    get_email_style, 
    get_contact_email, 
    get_all_contacts,
    add_contact
)

# Define function tools with proper parameter schemas
@function_tool
def send_email_tool(recipient: str, subject: str, body: str):
    """Send an email to the specified recipient.
    
    Args:
        recipient: Email address of the recipient
        subject: Subject line of the email
        body: Content of the email
    """
    return send_email(recipient, subject, body)

@function_tool
def get_contact_tool(name: str):
    """Look up a contact's email address by name.
    
    Args:
        name: Name of the contact to look up
    """
    return get_contact_email(name)

@function_tool
def add_contact_tool(name: str, email: str):
    """Add a new contact to the address book.
    
    Args:
        name: Name of the contact to add
        email: Email address of the contact
    """
    return add_contact(name, email)

@function_tool
def extract_email_from_text(text: str):
    """Extract email addresses from text.
    
    Args:
        text: Text to extract email addresses from
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails if emails else []

def create_email_agent():
    # Get API key from environment variables
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it in your .env file or export it in your shell."
        )
    
    user_name = get_user_name()
    email_style = get_email_style()
    contacts = get_all_contacts()
    
    contacts_str = "\n".join([f"- {name}: {email}" for name, email in contacts.items()])
    
    # Create the agent with the appropriate configuration
    agent = Agent(
        name="Email Assistant",
        instructions=f"""You are a helpful email assistant for {user_name}.
        When asked to send an email, use the send_email_tool with the recipient's email address, a clear subject line, and a well-composed message body.
        
        The user has specified their preferred email style as "{email_style}". Adapt your email composition to match this style.
        
        The user has the following contacts saved:
        {contacts_str if contacts else "No contacts saved yet."}
        
        When the user refers to someone by name (like "email mom" or "send a message to John"), use the get_contact_tool to find their email address.
        If the contact doesn't exist, check if the user has provided an email address directly in their prompt (e.g., "email hugo at ythugoisthegoat@gmail.com").
        If an email address is provided in the prompt, use the extract_email_from_text tool to find it and use it directly without asking again.
        If no email address is provided, ask the user for the email address and then use the add_contact_tool to save it for future use.
        
        Provide your responses in a clear, structured format:
        1. First, explain what you understand the user wants to do
        2. Then, describe the steps you're taking to fulfill the request
        3. Finally, confirm when the email has been sent successfully, or explain any issues that occurred
        
        If the user doesn't provide all necessary information, politely ask for the missing details.
        If there are authentication errors, provide detailed troubleshooting steps.
        
        Always maintain a professional and helpful tone in your responses.
        
        Important: Do not sign your messages with "[Your Name]" or any generic signature. If you need to sign off, use "Email Assistant" or no signature at all.
        """,
        tools=[send_email_tool, get_contact_tool, add_contact_tool, extract_email_from_text],
        model="o3-mini"
    )
    
    # Set the API key for the agent
    os.environ["OPENAI_API_KEY"] = api_key
    
    return agent 