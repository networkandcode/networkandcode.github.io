import asyncio

from google.genai import types

from runner import runner
from session_service import session_service
from vars import (
    APP_NAME,
    SESSION_ID,
    USER_ID,
)


async def main():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    while True:
        user_message = input("User: ")
        content = types.Content(role="user", parts=[types.Part(text=user_message)])

        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if not part.thought:
                            print(part.text)
            else:
                print(event)


if __name__ == "__main__":
    asyncio.run(main())
