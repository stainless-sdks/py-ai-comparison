import json
import os
import rich
from typing_extensions import Literal

from mistralai import Mistral
from mistralai.models import Function, Tool, UserMessage

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])


def get_weather(location: str, units: Literal["c", "f"]) -> str:
    """Lookup the weather for a given city in either celsius or fahrenheit

    Args:
        location: The city and state, e.g. San Francisco, CA
        units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
    Returns:
        A dictionary containing the location, temperature, and weather condition.
    """
    # Simulate a weather API call
    print(f"Fetching weather for {location} in {units}")

    # Here you would typically make an API call to a weather service
    # For demonstration, we return a mock response
    if units == "c":
        return json.dumps(
            {
                "location": location,
                "temperature": "20°C",
                "condition": "Sunny",
            }
        )
    else:
        return json.dumps(
            {
                "location": location,
                "temperature": "68°F",
                "condition": "Sunny",
            }
        )


def main() -> None:
    weather_tool = Tool(
        function=Function(
            name="get_weather",
            description="Lookup the weather for a given city in either celsius or fahrenheit",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "units": {
                        "type": "string",
                        "enum": ["c", "f"],
                        "description": "Unit for the output, either 'c' for celsius or 'f' for fahrenheit",
                    },
                },
                "required": ["location", "units"],
            },
        )
    )

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[UserMessage(content="What is the weather in SF?")],
        tools=[weather_tool],
    )

    while True:
        rich.print(f"Response: {response.choices[0].message.content}")

        if not response.choices or not response.choices[0].message.tool_calls:
            # no more messages
            break

        tool_results = []
        for tool_call in response.choices[0].message.tool_calls:
            if tool_call.function.name == "get_weather":
                # Parse the arguments
                args = json.loads(tool_call.function.arguments)

                # Call the function manually
                result = get_weather(**args)
                rich.print("Tool result:", result)

                tool_results.append(
                    {
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tool_call.id,
                    }
                )
            else:
                raise ValueError(f'unknown tool {tool_call.function.name}')

        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                UserMessage(content="What is the weather in SF?"),
                response.choices[0].message,
                *tool_results,
            ],
            tools=[weather_tool],
        )
        rich.print("Final response:", response.choices[0].message.content)


if __name__ == "__main__":
    main()
