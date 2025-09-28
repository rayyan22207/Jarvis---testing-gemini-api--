# # main.py
# from typing import Generator
# from helpers import print_section
# from gemini_client import ask_gemini, ask_gemini_text
# from speak import speak  # list_voices if you want to inspect voices

# def print_or_stream(result):
#     """Print a string or stream (generator) cleanly."""
#     if isinstance(result, str):
#         print(result)
#         return result
#     elif isinstance(result, Generator):
#         collected = []
#         for chunk in result:
#             print(chunk, end="", flush=True)
#             collected.append(chunk)
#         print()  # newline after streaming
#         return "".join(collected)
#     else:
#         print(result)  # fallback
#         return str(result)

# def main():
#     print_section("AUTO (prompt → auto stream if long)")
#     prompt = input("Ask Gemini something: ").strip()
#     if not prompt:
#         print("No prompt given. Exiting.")
#         return

#     # Auto mode: short → non-stream, long → stream
#     result = ask_gemini(prompt)  # returns str OR generator[str]
#     full_text = print_or_stream(result)

#     # Speak the reply (comment out if you don't want audio)
#     try:
#         speak(full_text)
#     except Exception as e:
#         print(f"(TTS skipped: {e})")

#     # Optional: long demo
#     run_long = input("\nRun long-prompt demo? (y/N): ").strip().lower() == "y"
#     if run_long:
#         print_section("AUTO (long prompt → stream)")
#         long_prompt = ("Explain WebRTC, signaling, STUN/TURN, ICE, and sample flows.\n" * 50).strip()
#         result2 = ask_gemini(long_prompt)
#         print_or_stream(result2)

#         print_section("ALWAYS TEXT (buffers even if streamed)")
#         buffered = ask_gemini_text(long_prompt)  # always returns a single string
#         print(buffered)

#     print("\nDone ✅")

# if __name__ == "__main__":
#     main()


from image_gen import generate_image

prompt = input("Describe the image you want: ").strip()
files = generate_image(prompt, out_path="art.png")
print("Saved:", files)
