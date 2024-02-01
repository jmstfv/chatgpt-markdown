import json
import datetime
import os
import re

def json_to_markdown(data):
    title = data.get("title")
    chat_id = data.get("id")
    create_time = datetime.datetime.fromtimestamp(data.get("create_time")).strftime("%Y-%m-%d %H:%M:%S")
    update_time = datetime.datetime.fromtimestamp(data.get("update_time")).strftime("%Y-%m-%d %H:%M:%S")

    markdown_str = f"# {title}\n\n"
    markdown_str += f"ID: {chat_id}\n\n"
    markdown_str += f"Created on: {create_time}\n\n"
    if update_time is not None:
        markdown_str += f"Updated on: {update_time}\n\n"

    for key, value in data["mapping"].items():
        message_obj = value.get("message")
        if message_obj:
            role = message_obj["author"]["role"]
            content = message_obj["content"].get("parts", [""])[0] if "parts" in message_obj["content"] else ""
            if role == "user":
                markdown_str += f"**User**: {content}\n\n"
            elif role == "assistant":
                markdown_str += f"**Assistant**: {content}\n\n"

    return markdown_str

def title_to_filename(title):
    filename = re.sub(r"[^a-z0-9_]", "", title.lower().replace(" ", "_"))
    return f"{filename}.md"

# CHANGE THIS!
full_path_to_conversations = "conversations.json"
full_path_to_markdown = "/tmp/conversations"

os.makedirs(full_path_to_markdown)

with open(full_path_to_conversations, "r") as f:
    data = json.load(f)

for item in data:
    markdown_content = json_to_markdown(item)
    file_name = title_to_filename(item["title"])
    with open(os.path.join(full_path_to_markdown, file_name), "w") as md_file:
        md_file.write(markdown_content)

print(f"Conversations saved to {full_path_to_markdown} directory!")
