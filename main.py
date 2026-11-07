import argparse
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function


MAX_ITERATIONS = 20


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="A simple AI coding agent."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print function arguments and results",
    )
    parser.add_argument(
        "user_prompt",
        help="What should the agent do?",
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Final response:\n{message.content}")
            return

        for tool_call in message.tool_calls:
            result_message = call_function(
                tool_call,
                verbose=args.verbose,
            )

            if not result_message.get("content"):
                raise RuntimeError(
                    f"Function {tool_call.function.name} returned no content"
                )

            messages.append(result_message)

            if args.verbose:
                print(f"-> {result_message['content']}")

    print(
        f"Error: Maximum number of iterations "
        f"({MAX_ITERATIONS}) reached without a final response."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()

