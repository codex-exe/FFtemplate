import json

def load_prompt():
    '''Loading the pre defined prompt'''
    with open('static/prompt.json', 'r') as file:
        prmpt = json.load(file)
    return prmpt

def load_tools():
    '''Loading the predefined chatbot tools'''
    with open('static/tools.json', 'r') as file:
        tools = json.load(file)
    return tools

def new_chat():
    '''Creating a new chat session by resetting the chat history'''
    prompt = load_prompt()
    with open('cache/chat_history.json', 'w') as file:
        file.write(json.dumps(prompt, indent=4))
    return "New chat has been started."

def load_chat():
    '''Loading the chat history from cache'''
    with open('cache/chat_history.json', 'r') as file:
        chat = json.load(file)
    return chat

def update_chat(role, content, name=None):
    '''Updating the chat history with the given role and content'''
    with open('cache/chat_history.json', 'r') as file:
        temp = json.load(file)
    with open('cache/chat_history.json', 'w') as file:
        if name:
            temp.append(
                {
                    "role": role,
                    "name": name,
                    "content": content
                }
            )
        else:
            temp.append(
                {
                    "role": role,
                    "content": content
                }
            )
        file.write(json.dumps(temp, indent=4))
    return "Chat history updated!"