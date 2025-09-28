from gemini_client import ask_gemini, stream_gemini
from helpers import print_section

print_section("BASIC")
Question = input("Ask Gemini something: ")
print(ask_gemini(Question))
# print(ask_gemini("Give me 2 lines on why Python is good for AI."))

# print_section("STREAM")
# for text in stream_gemini("List 3 fun Python libraries with one-line descriptions."):
#     print(text, end="", flush=True)
print("\nDone ✅")
