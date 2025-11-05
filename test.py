from auxknow import AuxKnow
import json
from dotenv import load_dotenv
# Initialize the AuxKnow instance
auxknow = AuxKnow(
    verbose=True,  # Optional, default: False
    auto_prompt_augment=True,  # Optional, default: False
    auto_model_routing=False,  # Optional, default: True
    auto_query_restructuring=False,  # Optional, default: False
    enable_unibiased_reasoning=True,  # Optional, default: True
    performance_logging_enabled=False,  # Optional, default: False
    fast_mode=False,  # Optional, default: False
    enable_reasoning=False,
    config_file_path="auxknow_config.json"
)
load_dotenv()
# # Ask a question
response = auxknow.ask(
    question="Why is 2+2 4 and not 5",
    context="",  # Optional context
    deep_research=True,  # Optional, enables in-depth research mode
    fast_mode=True,  # Optional, prioritizes speed over quality
    enable_reasoning=False,  # Optional, enables reasoning mode
    for_citations=True  # Optional, enables citation extraction
)
print("=============\n", response, "\n=============")

print("Answer:", response.answer)
print("Citations:", response.citations)
# for response in auxknow.ask_stream("What is quantum computing?", enable_reasoning=True):
#     print(response.answer)
# print(response.citations)    