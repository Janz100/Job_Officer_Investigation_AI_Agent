from reflection.reflection_agent import ReflectionAgent
from memory.reflection_memory import ReflectionMemory

reflection_agent = ReflectionAgent()
reflection_memory = ReflectionMemory()

print("\n========== GENERATING REFLECTION ==========")

result = reflection_agent.reflect_on_investigation(1)
print(result)

print("\n========== RETRIEVING SAVED REFLECTION ==========")

reflections = reflection_memory.get_reflections(1)

for item in reflections:
    print("Reflection ID:", item["id"])
    print("Investigation ID:", item["investigation_id"])
    print("Reflection:", item["reflection"][:300])
    print("Created:", item["created_at"])
    print("-----------------------------------")