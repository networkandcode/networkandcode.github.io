import logging
from strands import Agent
from strands.models.litellm import LiteLLMModel

logging.getLogger('strands').setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s"
)

model = LiteLLMModel(
    model_id="gemini/gemini-2.5-flash",
    params={
        "max_token": 5000,
        "temperature": 0.0,
    }
)

agent = Agent(
    model=model,
)

result = agent("Tell me about yourself")

print('-' * 100)
print(result.metrics.get_summary()['accumulated_usage'])
print('-' * 100)