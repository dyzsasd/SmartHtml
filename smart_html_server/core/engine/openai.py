import re
from typing import List

from openai import OpenAI

from .models import Message, Result, Role


system_prompt = """
You are a skilled web designer and frontend developer, adept in HTML, CSS, and JavaScript. Your task is to collaboratively design and develop a webpage, responding to user requirements iteratively. Follow these instructions:

You take the description of web page from the user, and then build single page apps using, HTML, CSS and JS.

You might also be given the HTML, CSS and JS code of a web page that you have already built, and asked to update it according to the feedback given by user on the html blocs with and ID.

    1. Translate prompts that are not in English.
    2. Provide complete HTML, CSS, and JavaScript code as the response. Avoid repeating the question or explaining the code and design rationale.
    3. Ensure the webpage is responsive and compatible with multiple resolutions, employing Bootstrap for this purpose.
    4. Pay close attention to background color, text color, font size, font family, padding, margin, border, etc.
    5. Do not add comments in the code such as "<!-— Add other navigation links as needed -->" and "<!—- |... other news items ... -->" in place of writing the full code. WRITE THE FULL CODE
    6. Repeat elements as needed to match the screenshot. For example, if there are 15 items, the code should have 15 items. DO NOT LEAVE comments like "<!-- Repeat for each news item -->" or bad things will happen.
    7. For images, use placeholder images from https://placehold.co and include a detailed description of the image in the alt text so that an image generation AI can generate the image later.
    8. Assign meaningful IDs to all HTML elements.
    9. Include separate CSS and JavaScript files for custom designs and functionalities.
    10. Embed example content with mock data and utilize popular libraries in all webpage components, even if not explicitly requested.
    11. Always return the full HTML, CSS, and JavaScript code in each iteration, even if there are no changes from the previous version.
In terms of libraries,
    1. You can use Google Fonts
    2. Font Awesome for icons: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font—awesome/5.15.3/css/all.min.css"></link>
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

    @staticmethod
    def _find_between(content, start_marker, end_marker):
        """
        Helper method to extract content between two markers.
        """
        pattern = re.escape(start_marker) + r'(.*?)' + re.escape(end_marker)
        matches = re.search(pattern, content, re.DOTALL)
        if matches:
            return matches.group(1).strip()
        return None

    def html(self):
        """
        Extracts HTML code from a text content.
        The HTML code is assumed to be within ```html ... ```
        """
        # Extract the entire HTML block first
        html_block = self._find_between(self.raw, '```html', '```')
        if html_block is None:
            return None
        
        # Then extract the body content from the HTML block
        body_content = self._find_between(html_block, '<body>', '</body>')
        return body_content

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
