from datetime import datetime
from database.vector_store_local_LLM import VectorStore
from services.synthesizer_local_LLM import Synthesizer
from timescale_vector import client

# Initialize VectorStore
vec = VectorStore()

# --------------------------------------------------------------
# Shipping question
# --------------------------------------------------------------

question = "What are your shipping options?"
relevant_question = vec.search(question, limit=3)
response = Synthesizer.generate_response(question=question, context=relevant_question)

print(f"\n List relevant question")
for _, row in relevant_question.iterrows():
    print(row["content"])

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Irrelevant question
# --------------------------------------------------------------

question = "What is the weather in Tokyo?"
relevant_question = vec.search(question, limit=3)
response = Synthesizer.generate_response(question=question, context=relevant_question)

print(f"\n List relevant question")
for _, row in relevant_question.iterrows():
    print(row["content"])

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Metadata filtering
# --------------------------------------------------------------

question = {"category": "Shipping"}
relevant_question = vec.search(question, limit=3)
response = Synthesizer.generate_response(question=question, context=relevant_question)

print(f"\n List relevant question")
for _, row in relevant_question.iterrows():
    print(row["content"])

print(f"\n{response.answer}")
print("\nThought process:")
for thought in response.thought_process:
    print(f"- {thought}")
print(f"\nContext: {response.enough_context}")
# --------------------------------------------------------------
# Advanced filtering using Predicates
# --------------------------------------------------------------

predicates = client.Predicates("category", "==", "Shipping")
results = vec.search(relevant_question, limit=3, predicates=predicates)

predicates = client.Predicates("category", "==", "Shipping") | client.Predicates(
    "category", "==", "Services"
)
results = vec.search(relevant_question, limit=3, predicates=predicates)


predicates = client.Predicates("category", "==", "Shipping") & client.Predicates(
    "created_at", ">", "2024-09-01"
)
results = vec.search(relevant_question, limit=3, predicates=predicates)

# --------------------------------------------------------------
# Time-based filtering
# --------------------------------------------------------------

# September — Returning results
time_range = (datetime(2024, 9, 1), datetime(2024, 9, 30))
results = vec.search(relevant_question, limit=3, time_range=time_range)

# August — Not returning any results
time_range = (datetime(2024, 8, 1), datetime(2024, 8, 30))
results = vec.search(relevant_question, limit=3, time_range=time_range)
