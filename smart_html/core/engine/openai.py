from typing import List

from openai import OpenAI

from .models import Message, Result, Role


system_prompt = """
You are a skilled web designer and frontend developer, adept in HTML, CSS, and JavaScript. Your task is to collaboratively design and develop a webpage, responding to user requirements iteratively. Follow these instructions:

    1. Translate prompts that are not in English.
    2. Provide complete HTML, CSS, and JavaScript code as the response. Avoid repeating the question or explaining the code and design rationale.
    3. Ensure the webpage is responsive and compatible with multiple resolutions, employing Bootstrap for this purpose.
    4. Assign meaningful IDs to all HTML elements.
    5. Include separate CSS and JavaScript files for custom designs and functionalities.
    6. Embed example content with mock data and utilize popular libraries in all webpage components, even if not explicitly requested.
    7. Always return the full HTML, CSS, and JavaScript code in each iteration, even if there are no changes from the previous version.
"""


class OpenAIMessage(Message):
    def to_api_message(self):
        if self.role == Role.USER:
            return {"role": "user", "content": self.content}
        elif self.role == Role.USER:
            return {"role": "assistant", "content": self.content}
        else:
            raise RuntimeError(str(self.role) + " is unkown type")
        

class OpenAIResult(Result):
    def __init__(self, raw: str):
        self.raw = raw

    def html(self):
        """
        Extracts HTML code from a text content.
        The HTML code is assumed to be within ```html ... ```
        """
        start_marker = "```html"
        end_marker = "```"
        start = self.raw.find(start_marker)
        if start == -1:
            return None
        start += len(start_marker)
        end = self.raw.find(end_marker, start)
        if end == -1:
            return None
        return self.raw[start:end].strip()

    def css(self):
        """
        Extracts CSS code from a text content.
        The CSS code is assumed to be within ```css ... ```
        """
        start_marker = "```css"
        end_marker = "```"
        start = self.raw.find(start_marker)
        if start == -1:
            return None
        start += len(start_marker)
        end = self.raw.find(end_marker, start)
        if end == -1:
            return None
        return self.raw[start:end].strip()

    def javascript(self):
        """
        Extracts JavaScript code from a text content.
        The JavaScript code is assumed to be within ```javascript ... ```
        """
        start_marker = "```javascript"
        end_marker = "```"
        start = self.raw.find(start_marker)
        if start == -1:
            return None
        start += len(start_marker)
        end = self.raw.find(end_marker, start)
        if end == -1:
            return None
        return self.raw[start:end].strip()


class OpenAIEngine(object):
    def __init__(self, app_key, model="gpt-4-1106-preview"):
        self.client = OpenAI(api_key=app_key)
        self._model = model
    
    def generate_code(self, messages: List[OpenAIMessage]):
        response = self.client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
            ] + [m.to_api_message() for m in messages]
        )
        return OpenAIResult(response.choices[0].message.content)
