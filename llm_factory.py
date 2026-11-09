import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiLLM:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def invoke(self, messages):
        """
        Accepts either:
        - string prompt
        - list of LangChain messages
        """

        # If already string
        if isinstance(messages, str):
            prompt = messages

        # If list of messages (HumanMessage etc.)
        elif isinstance(messages, list):
            prompt = "\n".join(m.content for m in messages)

        else:
            raise ValueError("Unsupported input type for LLM")

        response = self.model.generate_content(prompt)
        return response.text


def get_llm():
    return GeminiLLM()
