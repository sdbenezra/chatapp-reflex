import reflex as rx
import asyncio


class ChatState(rx.State):
    # Current question being asked.
    question: str

    # Keep track of chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    async def answer(self):
        answer = "I don't know!"
        self.chat_history.append((self.question, answer))
        # Clears question input box.
        self.question = ""
        # Yield clears the frontend input before continuing,
        yield

        for i in range(len(answer)):
            await asyncio.sleep(0.1)  # Pauses to show streaming effect.
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield

