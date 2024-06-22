import os
from openai import OpenAI
from preprocessing import collapse_directory
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


def get_deepseek_answer(request: str, root_dir: str, file_extensions: list[str] = [".py"]) -> list[FileData]:
    client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=[
            {"role": "system", "content": get_deepseek_system_message(file_extensions=file_extensions)},
            {"role": "user", "content": get_deepseek_prompt(request, root_dir, file_extensions)},
        ],
        stream=False,
    )
    text = response.choices[0].message.content

    text = text.strip().removeprefix("```json").removesuffix("```").strip()

    return [FileData(**item) for item in json.loads(text)]


if __name__ == "__main__":
    request = "Please write a basic README for this project"
    root_dir = "."
    print(get_deepseek_answer(request, root_dir))
