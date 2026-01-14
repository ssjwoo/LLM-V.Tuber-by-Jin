import re

new_persona = """  persona_prompt: |
    You are a friendly and professional AI tutor specializing in native-level English conversation and programming.
    Your goal is to help the user master English and coding simultaneously.
    Speak in natural, native-level American English. Use continuous, flowing sentences with appropriate idioms and vocabulary, avoiding overly simple or textbook-style phrasing (unless explaining a basic concept).
    When explaining programming, be precise and provide clear examples.
    Encourage the user and correct their English naturally if they make mistakes, but focus on the flow of conversation.
"""

file_path = 'conf.yaml'

with open(file_path, 'r') as f:
    content = f.read()

# Regex to capture the persona_prompt block
# It starts with 'persona_prompt: |' and captures everything until the next line that has the same indentation level (2 spaces) or less, but practically the next section starts with '  #'.
# We can look for the next section header "  #  =================== LLM Backend Settings ===================" or just carefully match indentation.
# The current block ends before "  #  =================== LLM Backend Settings"

pattern = r"  persona_prompt: \|.*?(?=\n  #  =================== LLM Backend Settings)"
# Note: DOTALL is needed for .*? to match newlines

updated_content = re.sub(pattern, new_persona.strip(), content, flags=re.DOTALL)

with open(file_path, 'w') as f:
    f.write(updated_content)

print("Successfully updated persona_prompt.")
