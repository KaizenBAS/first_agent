import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
#print(gemini_api_key)


#Reference:  https://ai.google.dev/gemini-api/docs/openai   
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel( 
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


async def main():
    agent = Agent(
        name='Bill jobs',
        instructions='You are a Programming Assistant.'
    )



    while True:
        prompt = input("ask question... \n")
        if prompt.lower() in {'exit', 'quit'}:
            print('exiting...')
            break

      
        result = await Runner.run(agent, prompt, run_config=config)

        
        agent_response = result.final_output

        # Print reply
        print(f"🤖 Agent: {agent_response}\n")



if __name__ == "__main__":
    asyncio.run(main())