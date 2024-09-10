#!/usr/bin/env python3
from dotenv import load_dotenv
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import asyncio
import json
import sys
import os

# Find / create config in home directory
def find_config_dir():
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".terminai")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

CONFIG_DIR = find_config_dir()
# .env and ai_config.json files should be inside .terminai directory for easy access
ENV_FILE = os.path.join(CONFIG_DIR, '.env')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'ai_config.json')

# Load environment variables from .env file
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    print(f"Warning: .env file not found at {ENV_FILE}. Please create one with your API keys.")

# Check for API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize clients based on available keys
openai_client = None
anthropic_client = None
if openai_api_key and anthropic_api_key:
    openai_client = AsyncOpenAI(api_key=openai_api_key)
    anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)
elif openai_api_key:
    openai_client = AsyncOpenAI(api_key=openai_api_key)
elif anthropic_api_key:
    anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)
else:
    print(f"Error: No API keys found in {ENV_FILE}")
    print(f"\nPlease add at least one API key to the .env file at {ENV_FILE}.")
    print("Example .env file content:")
    print("OPENAI_API_KEY='your_openai_api_key_here'")
    print("ANTHROPIC_API_KEY='your_anthropic_api_key_here'")
    exit(1)


# Load or initialize configuration based on available API clients
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"provider": "openai" if openai_client else "anthropic", "model": "gpt-3.5-turbo" if openai_client else "claude-3-opus-20240229"}


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

# Anthropic does not have a list models API. Hardcode list from https://docs.anthropic.com/en/docs/about-claude/models
ANTHROPIC_MODELS = ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]


# Stream responses from selected LLM based on current configuration
async def stream_llm_response(prompt):
    if config["provider"] == "openai":
        stream = await openai_client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        print("AI:\n")
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='', flush=True)
    elif config["provider"] == "anthropic":
        stream = await anthropic_client.messages.create(
            model=config["model"],
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )  
        print("AI:\n")
        async for message in stream:
            if message.type == "content_block_start":
                continue
            elif message.type == "content_block_delta":
                print(message.delta.text, end="", flush=True)
            elif message.type == "content_block_stop":
                break
    print("\n")


# Print available models to the terminal
async def list_models():
    print("===OpenAI models===")
    # OpeAI has an API to retrieve models
    async for model in await openai_client.models.list():
        print(f"- {model.id}")
    # Anthropic does not have an API to retrieve models
    print("\n===Anthropic models===")
    for model in ANTHROPIC_MODELS:
        print(f"- {model}")


# Saves selected model to config file
async def select_model(model):
    openai_models = [model.id async for model in await openai_client.models.list()]
    if model in openai_models:
        config["provider"] = "openai"
        config["model"] = model
    elif model in ANTHROPIC_MODELS:
        config["provider"] = "anthropic"
        config["model"] = model
    else:
        print(f"Error: Unknown model '{model}'")
        return
    save_config(config)
    print(f"Selected model: {model}")


async def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Usage:")
        print("  ai <prompt>                            Send a prompt to external LLM")
        print("  ai --list-models                       List available LLM models")
        print("  ai --select-model <model_name>         Select an LLM model to use")
        print("  ai --info                              Display current configuration")
        print("  ai --help                              Show this help message")
        print("  <command> | ai [additional instructions]  Pipe command output to LLM")
        print("  ai \"$(command)\" [additional instructions]  Use command output as input")
        print("\nOptions:")
        print("  --list-models    List all available models from OpenAI and Anthropic")
        print("  --select-model   Choose a specific model to use for LLM interactions")
        print("  --info           Show the current LLM provider and model being used")
        print("  --help, -h       Display this help message")
        return
    if "--list-models" in args:
        await list_models()
        return
    if "--select-model" in args:
        index = args.index("--select-model")
        if index + 1 < len(args):
            await select_model(args[index + 1])
        else:
            print("Error: No model specified after --select-model")
        return
    if "--info" in args:
        print("Current configuration")
        print(f"--Provider: {config['provider']}")
        print(f"--Model: {config['model']}")
        return
    # Check for input from a pipe
    piped_input = sys.stdin.read() if not sys.stdin.isatty() else ""
    if piped_input:
        # Use piped input as as command output
        command_output = piped_input
        # Use all args as additional instructions
        additional_instructions = ' '.join(args)
        prompt = f"{command_output}\n\n{additional_instructions}".strip()
    else:
        # If no piped input treat all arguments as the prompt
        prompt = ' '.join(args)
    if not prompt:
        print("Usage: ai <prompt>")
        print("   or: <command> | ai [additional instructions]")
        print("   or: ai \"$(command)\" [additional instructions]")
        print("   or: ai --list-models")
        print("   or: ai --select-model <model_name>")
        print("   or: ai --info")
        print("   or: ai --help")
        return
    await stream_llm_response(prompt)



# c'mon do magic
if __name__ == "__main__":
    asyncio.run(main())