# terminAI

Boost your productivity with **terminAI** a terminal-based LLM wrapper that streamlines tasks, answers questions, reads piped input, saves time, and keeps you focused on what matters most, shipping!

## Features

- Interact with OpenAI and Anthropic language models
- Stream responses in real-time
- Pipe command outputs directly to the LLM
- List available models and select your preferred one
- Easy configuration management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/misirov/terminAI.git
   cd terminAI
   ```

2. Install the package:
   ```
   pip install .
   ```

3. Set up your API keys:
   - Create a `.terminai` directory in your home folder if not created by script:
     ```
     mkdir ~/.terminai
     ```
   - Create a `.env` file in the `.terminai` directory:
     ```
     touch ~/.terminai/.env
     ```
   - Add your API keys to the `.env` file:
     ```
     OPENAI_API_KEY="your_openai_api_key_here"
     ANTHROPIC_API_KEY="your_anthropic_api_key_here"
     ```

## Uninstall

- Uninstall `terminai`. Remember to delete the data left in `~/.terminai`
```python
pip uninstall terminai
```


## Usage

After installation, you can use the `ai` command in your terminal.

### Prompt examples

1. `ai "how can i find the function selector of a solidity function with foundry? provide only command."`
2. `ai "what is the USDC address on ethereum mainnet? provide link to etherscan"`
3. `ai "nmap command to scan hosts in my internal network without pings"`
4. `ai "create command line regex to find name Sarah inside a file. provide only the command."`


### Pipe command outputs

1. `python -c "print('my password is 12345')" | ai "what is my password?"`
2. `cat contracts/src/Counter.sol | ai "how many functions does this solidity contract have? only name them"`
3.`ai "$(ls -la)" Where is the terminai configuration file?`
4. `solc --help | ai "how to compile via IR? respond with command only"`
5. `cat file.json | ai "convert file to XML format" > file.xml`

### -- flags
- List available models:
  ```
  ai --list-models
  ```

- Select a specific model:
  ```
  ai --select-model gpt-4
  ```

- Display current configuration:
  ```
  ai --info
  ```

- Show help message:
  ```
  ai --help
  ```

## Configuration

terminAI automatically manages its configuration in `~/.terminai/ai_config.json`. You can change the model or provider by using the `--select-model` command.



## License

This project is licensed under the MIT License.

