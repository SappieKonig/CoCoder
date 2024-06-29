import os
import openai
from .preprocessing import collapse_directory
import json
from dataclasses import dataclass


@dataclass
class FileData:
    filepath: str
    content: str


DEEPSEEK_SYSTEM_MESSAGE = "You are an assistant that helps to write pull requests. As input you get JSON's containing "
"the location of files and their corresponding content. "


def get_deepseek_system_message():
    return (f"You are coco (short for CoCoder), an assistant that helps to write pull requests. As input you get JSON's containing "
            f"the location of files and their corresponding content. As output, you will return a JSON of the format "
            f"```json[{{filepath:<fp>, content: <content>}}]```, containing file names and content "
            f"for every file that must be changed or added for the requested change. You can create files who do not yet exit. "
            f"Also, it might not always apply, but where it does, "
            f"remember to update README's and docs as well.")


def get_deepseek_prompt(request: str, root_dir: str) -> str:
    prompt = collapse_directory(root_dir)
    prompt += "\n\n"
    prompt += request
    return prompt


def text_preprocessing(txt):
    """Preprocess text given to the LLM"""
    # replace " with \", so the json that the LLM returns works well
    return txt.replace(r'"', r'\"')


def get_deepseek_answer(request: str, root_dir: str) -> list[FileData]:
    client = openai.OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")

    system_message = get_deepseek_system_message()
    system_message = text_preprocessing(system_message)
    prompt = get_deepseek_prompt(request, root_dir)
    prompt = text_preprocessing(prompt)
    temp = 1.0
    for _ in range(3):
        try:
            response = client.chat.completions.create(
                model="deepseek-coder",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
                temperature=temp,
            )
            text = response.choices[0].message.content
        except openai.APIStatusError as e:
            print(system_message, prompt)
            print(f"#chars in system message: {len(system_message)}")
            print(f"#chars in prompt: {len(prompt)}")
            raise e

        try:
            text = text.strip().removeprefix("```json").removesuffix("```").strip().replace(r"\'", r"'")

            return [FileData(**item) for item in json.loads(text)]
        except Exception as e:
            print(text)
            print(f"Error parsing LLM content: {e}. Retrying...")
            temp += 0.01  # small change, hopefully to break determinism
            break

    print("Failed to get valid output after 3 retries.")
    return []
