import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.responses.create(
    model="gpt-5.2",
    instructions="You are a helpful assistant.",
    input="In one short sentence, hello are you there?",
)

print(response.output_text)
