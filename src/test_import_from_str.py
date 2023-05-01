import asyncio
import importlib.util
import sys

# Define the source code as a string
module_code = """
async def hello_world():
    print("Hello world!")
"""

# Create a new module and add the code
module = importlib.util.module_from_spec(
    importlib.util.spec_from_loader("my_module", loader=None)
)
exec(module_code, module.__dict__)
sys.modules["my_module"] = module

# Import the module and call the function
import my_module

asyncio.run(my_module.hello_world())
