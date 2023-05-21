import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

# We are using dotenv to provide our enviornment vribles (see README to set yours), isolating it to where its needed and MAKING SURE OUR KEY IS HIDDEN
# fetch_summary() utilizes the OpenAI Chat Completion API to generate summaries in response to an internal and external prompt.
# Errors are handled separately for OpenAI-specific errors and general exceptions, providing more informative error messages.

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