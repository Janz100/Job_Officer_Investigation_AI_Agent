
from llm import get_llm

llm = get_llm()

response = llm.invoke(
    "Explain what a job scam is in simple English. Give three examples."
)

print("\n========== RESPONSE CONTENT ==========")
print(repr(response.content))

print("\n========== RESPONSE METADATA ==========")
print(response.response_metadata)

print("\n========== ADDITIONAL INFORMATION ==========")
print(response.additional_kwargs)
