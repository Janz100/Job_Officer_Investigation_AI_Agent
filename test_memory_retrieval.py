from agent import retrieve_previous_lessons

lessons = retrieve_previous_lessons()

print("\nMEMORY RETRIEVAL TEST")
print("=" * 65)
print("Retrieved characters:", len(lessons))
print("Contains Investigation 1:", "Investigation 1:" in lessons)
print("\nRetrieved lessons:")
print(lessons)
print("\n" + "=" * 65)
