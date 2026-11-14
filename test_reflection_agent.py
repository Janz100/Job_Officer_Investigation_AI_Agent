from reflection.reflection_agent import ReflectionAgent

print("\n========== TESTING UPDATED REFLECTION AGENT ==========\n")

agent = ReflectionAgent()

reflection = agent.reflect_on_investigation(1)

print("\n========== NEW REFLECTION ==========\n")
print(reflection)

print("\n========== TEST COMPLETED ==========")