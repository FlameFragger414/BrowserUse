import asyncio

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, ChatOpenAI


async def main() -> None:
    llm = ChatOpenAI(model="gpt-5-nano")
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
