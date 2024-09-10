import importlib.util
import asyncio
import os

def main():
    # Get the path to ai_script.py and load it
    ai_script_path = os.path.join(os.path.dirname(__file__), 'ai_script.py')
    spec = importlib.util.spec_from_file_location("ai_script", ai_script_path)
    ai_script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ai_script)
    asyncio.run(ai_script.main())



if __name__ == "__main__":
    main()