

import os
import traceback
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
from dotenv import load_dotenv
import google.genai as genai

import tools
import prompt

load_dotenv()
client = genai.Client()

oneshot_config = genai.types.GenerateContentConfig(
    tools=[tools.get_file, tools.get_files_in_directory],
    thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
)

# We make a wrapper function here, so that it has the config and client provided.
# I tried using functools.partial, but that seemingly broke the automatic parsing.
def new_agent(instructions: str, prompt: str):
    """Create a new agent. They will be ran one-shot [i.e, they only get your instructions and prompt, then return.]
    It may read files, but it cannot run commands.
    The instructions default to being empty, so you should explain its purpose in the instructions, and then use the prompt for "user" input.
    
    Args:
        instructions: The instructions for the agent.
        prompt: The prompt for the agent.

    Returns:
        str: The response from the agent.
    """
    return tools.new_agent(client, oneshot_config, instructions, prompt)
    
chat_config = genai.types.GenerateContentConfig(
    tools=[tools.get_file, tools.get_files_in_directory, new_agent],
    thinking_config=genai.types.ThinkingConfig(thinking_budget=-1), # dynamic
    system_instruction=prompt.get_prompt()
) 

chat = client.chats.create(model="gemini-2.5-flash", config=chat_config)
kivy.require('2.1.0')

class ChatApp(App):
    def build(self):
        self.title = 'Whirligig'
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Chat history
        self.scroll_view = ScrollView()
        self.chat_history = Label(size_hint_y=None, markup=True, halign='left', valign='top')
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll_view.add_widget(self.chat_history)
        self.root.add_widget(self.scroll_view)

        # Input area
        input_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.text_input = TextInput(hint_text='Enter your message...', multiline=False)
        self.text_input.bind(on_text_validate=self.send_message)
        input_layout.add_widget(self.text_input)

        self.send_button = Button(text='Send', size_hint_x=None, width=80)
        self.send_button.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_button)
        self.root.add_widget(input_layout)


        return self.root

    def send_message(self, _instance):
        user_message = self.text_input.text
        if user_message.strip():
            self.add_message(f"[b]You:[b] {user_message}")
            self.text_input.text = ''
            self.get_gemini_response(user_message)

    def get_gemini_response(self, user_message):
        try:
            message = ""
            for chunk in chat.send_message_stream(user_message):
                if chunk.text:
                    message += chunk.text
            self.add_message(f"[b]Gemini:[b] {message}")
        except Exception as e:
            self.add_message(f"[b]System:[b] Error getting response from Gemini: {e}")


    def add_message(self, message):
        self.chat_history.text += f"{message}\n"
        self.scroll_view.scroll_y = 0 # Scroll to bottom


if __name__ == '__main__':
    ChatApp().run()

