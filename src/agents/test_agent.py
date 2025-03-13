import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

@function_tool
def hello(name: str) -> str:
    """Say hello to someone.
    
    Args:
        name: The name of the person to greet
    """
    return f"Hello, {name}!"

def main():
    agent = Agent(
        name="Test Agent",
        instructions="You are a helpful assistant that can greet people.",
        tools=[hello],
        model="o3-mini"
    )
    
    try:
        result = Runner.run_sync(agent, "Say hello to John")
        print(f"Result: {result.final_output}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 