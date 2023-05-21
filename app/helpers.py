import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

async def fetch_summary(model, transcript, prompt, is_internal):
    completion_prompt = prompt.format(transcript)
    prompt_type = "internal" if is_internal else "external"
    print(f"Starting fetch_summary for {prompt_type} prompt")
    try:
        result = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": completion_prompt}],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        print(f"Completed fetch_summary for {prompt_type} prompt")
        return result.choices[0].message.content
    except openai.error.OpenAIError as e:
        error_message = str(e)
        print(f"OpenAIError occurred in fetch_summary for {prompt_type} prompt: {error_message}")
    except Exception as e:
        error_message = str(e)
        print(f"Error occurred in fetch_summary for {prompt_type} prompt: {error_message}")