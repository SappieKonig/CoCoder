import os
from openai import OpenAI
from .preprocessing import collapse_directory
import json
from dataclasses import dataclass


@dataclass
class FileData:
    filepath: str
    content: str


DEEPSEEK_SYSTEM_MESSAGE = "You are an assistant that helps to write pull requests. As input you get JSON's containing "
"the location of files and their corresponding content. "


def get_deepseek_system_message(file_extensions):
    return (f"You are an assistant that helps to write pull requests. As input you get JSON's containing "
            f"the location of files and their corresponding content. Only files with the extension {file_extensions} "
            f"are expanded. As output, you will return a JSON of the format "
            f"```json[{{filepath:<fp>, content: <content>}}]```, containing file names and content "
            f"for every file that must be changed or added for the requested change. You can create files whose "
            f"extensions are not included in {file_extensions}.")


def get_deepseek_prompt(request: str, root_dir: str, file_extensions: list[str]) -> str:
    prompt = collapse_directory(root_dir, file_extensions)
    prompt += "\n\n"
    prompt += request
    return prompt


def get_deepseek_answer(request: str, root_dir: str, file_extensions: list[str]) -> list[FileData]:
    client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

    system_message = get_deepseek_system_message(file_extensions)
    prompt = get_deepseek_prompt(request, root_dir, file_extensions)
    for _ in range(3):
        try:
            response = client.chat.completions.create(
                model="deepseek-coder",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
            text = response.choices[0].message.content

            text = text.strip().removeprefix("```json").removesuffix("```").strip()

            return [FileData(**item) for item in json.loads(text)]
        except Exception as e:
            print(f"Error parsing LLM content: {e}. Retrying...")

    print("Failed to get valid output after 3 retries.")
    return []
