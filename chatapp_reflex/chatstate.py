from dotenv import load_dotenv
import openai
import reflex as rx
import os
from openai import OpenAI

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


class ChatState(rx.State):
    # Current question being asked.
    question: str

    # Keep track of chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    def answer(self):
        client = OpenAI()
        session = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": self.question
                }
            ],
            stop=None,
            temperature=0.7,
            stream=True,
        )

        # As the chatbot responds it will add to the answer.
        answer = ""
        self.chat_history.append((self.question, answer))

        # Clears question input box.
        self.question = ""
        # Yield clears the frontend input before continuing,
        yield

        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    # presence of 'None' indicates the end of the response
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (self.chat_history[-1][0], answer)
                yield
