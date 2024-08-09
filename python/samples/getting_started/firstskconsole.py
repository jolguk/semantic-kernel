import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

# Initialize the kernel
kernel = Kernel()

# Add Azure OpenAI chat completion
kernel.add_service(AzureChatCompletion(
    deployment_name="jolgukwestus",
    api_key="2b0c0f7f9fa842f19bd5c462f13a8074",
    base_url="https://jolgukwestus.openai.azure.com/",
))

import logging

# Set the logging level for  semantic_kernel.kernel to DEBUG.
logging.basicConfig(
    format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("kernel").setLevel(logging.DEBUG)

chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

from typing import Annotated
from semantic_kernel.functions import kernel_function

class LightsPlugin:
    lights = [
        {"id": 1, "name": "Table Lamp", "is_on": False},
        {"id": 2, "name": "Porch light", "is_on": False},
        {"id": 3, "name": "Chandelier", "is_on": True},
    ]

    @kernel_function(
        name="get_lights",
        description="Gets a list of lights and their current state",
    )
    def get_state(
        self,
    ) -> Annotated[str, "the output is a string"]:
        """Gets a list of lights and their current state."""
        return self.lights

    @kernel_function(
        name="change_state",
        description="Changes the state of the light",
    )
    def change_state(
        self,
        id: int,
        is_on: bool,
    ) -> Annotated[str, "the output is a string"]:
        """Changes the state of the light."""
        for light in self.lights:
            if light["id"] == id:
                light["is_on"] = is_on
                return light
        return None
    
    # Add the plugin to the kernel
kernel.add_plugin(
    LightsPlugin(),
    plugin_name="Lights",
)

execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})

# Create a history of the conversation
history = ChatHistory()

# Get the response from the AI
async def main():
    try:
        result = (await chat_completion.get_chat_message_contents(
        chat_history=history,
        settings=execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    ))[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error or log more details here

# Call the async function

asyncio.run(main())


