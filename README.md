# Email Assistant Agent

A simple application that uses OpenAI's agents to send emails via Gmail.

## Project Structure

- `email_agent.py` - Main entry point for the application
- `src/` - Source code directory
  - `main.py` - Main application logic
  - `agents/` - Agent-related code
    - `agent_config.py` - Contains agent configuration
    - `test_agent.py` - Simple test agent for testing
  - `config/` - Configuration-related code
    - `user_config.py` - Manages user preferences and contacts
  - `services/` - Service-related code
    - `email_service.py` - Contains email sending functionality
  - `utils/` - Utility functions
- `.env` - Environment variables (not tracked in git)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   GMAIL_USER=your_gmail_address@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   OPENAI_API_KEY=your_openai_api_key
   ```

## Required API Keys

### OpenAI API Key
To use this application, you need an OpenAI API key:
1. Sign up or log in at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to the API keys section
3. Create a new API key
4. Add the key to your `.env` file as `OPENAI_API_KEY`

### Gmail App Password
To use Gmail for sending emails:
1. Enable 2-Step Verification on your Google account
2. Generate an App Password for this application
   - Go to your Google Account > Security > App passwords
   - Select "Mail" and "Other (Custom name)"
   - Enter a name for the app (e.g., "Email Assistant")
   - Copy the generated password to your `.env` file as `GMAIL_APP_PASSWORD`

## Usage

### Interactive CLI Mode

Run the application in interactive mode:

```
python email_agent.py
```

This will start an interactive CLI where you can enter your email requests. Type 'exit' to quit.

### Command Line Arguments

You can also provide your email request directly as a command line argument:

```
python email_agent.py --prompt "Send an email to example@example.com with the subject 'Hello' and tell them about my day"
```

or using the short form:

```
python email_agent.py -p "Send an email to example@example.com with the subject 'Hello' and tell them about my day"
```

### User Configuration

Configure your name, preferred email style, and contacts:

```
python email_agent.py --configure
```

You can also access the configuration menu from the interactive mode by typing 'config'.

### Privacy Mode

Enable privacy mode to censor email addresses in the terminal output:

```
python email_agent.py --privacy
```

This can be combined with other options:

```
python email_agent.py --privacy --prompt "Email mom and tell her I'll be home soon"
```

### Verbose Mode

Enable verbose mode to see detailed steps the agent takes while processing your request:

```
python email_agent.py --verbose
```

or using the short form:

```
python email_agent.py -v
```

You can combine verbose mode with other options:

```
python email_agent.py --privacy --verbose --prompt "Email mom and tell her I'll be home soon"
```

## Features

- Interactive CLI with rich text formatting
- Suppresses SMTP debug output for cleaner interface
- Displays agent responses in a nicely formatted panel
- Progress indicator while the agent is processing your request
- User configuration for name and preferred email style
- Contact management for easy reference to frequent recipients
- Privacy mode to censor email addresses in terminal output
- Natural language requests like "email mom" using saved contacts
- Verbose mode to see detailed agent steps and reasoning 