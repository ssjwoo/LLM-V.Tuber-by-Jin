import re
import os

FILE_PATH = "frontend/assets/main-nu7uwxNJ.js"

if not os.path.exists(FILE_PATH):
    print(f"Error: File not found at {FILE_PATH}")
    exit(1)

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find the specific assignments. 
# We look for the exact string literals seen in the file, which use single quotes inside double quotes.
# Current incorrect state seen in grep: DEFAULT_WS_URL="ws://'+window.location.host+'/client-ws"
# We want to change it to: DEFAULT_WS_URL="ws://"+window.location.host+"/client-ws"

# Note: The greedy match should be careful.
# Let's target the exact string pattern from the grep output 
old_ws = 'DEFAULT_WS_URL="ws://\'+\\window.location.host+\'/client-ws"'
new_ws = 'DEFAULT_WS_URL="ws://"+window.location.host+"/client-ws"'

old_base = 'DEFAULT_BASE_URL="http://\'+\\window.location.host+\'"'
# Wait, grep output for base was: DEFAULT_BASE_URL="http://'+window.location.host"
# Let's adjust the regex to be flexible about the exact quoting but targeting the content.

# Better approach: Regex substitution
# We want to turn "ws://'+window.location.host+'/client-ws"  -> "ws://"+window.location.host+"/client-ws"
# The difference is the quote type surrounding the + signs.

# Pattern 1: Find the WS definition
pattern_ws = r'DEFAULT_WS_URL="ws://\'\+window\.location\.host\+\'/client-ws"'
replacement_ws = 'DEFAULT_WS_URL="ws://"+window.location.host+"/client-ws"'

# Pattern 2: Find the Base definition
pattern_base = r'DEFAULT_BASE_URL="http://\'\+window\.location\.host\+\'"' 
# Actually grep said: DEFAULT_BASE_URL="http://'+window.location.host" (quote at end might be missing in grep output or it's implicitly closed?)
# Let's regex for the start and assume it closes.
pattern_base_loose = r'DEFAULT_BASE_URL="http://\'\+window\.location\.host(\'?)\"'
replacement_base = 'DEFAULT_BASE_URL="http://"+window.location.host'

new_content, count_ws = re.subn(pattern_ws, replacement_ws, content)
new_content, count_base = re.subn(pattern_base_loose, replacement_base, new_content)

print(f"WS URL replacements made: {count_ws}")
print(f"Base URL replacements made: {count_base}")

if count_ws == 0 and count_base == 0:
    print("WARNING: No replacements made. Trying alternative SEARCH pattern...")
    # Maybe it's already fixed but with single quotes?
    # Or maybe the grep output was slightly misleading on escaping.
    
    # Let's try to find ANY version of DEFAULT_WS_URL assignment
    check_match = re.search(r'DEFAULT_WS_URL=.*?".*?"', content)
    if check_match:
        print(f"Found current value: {check_match.group(0)}")
    else:
        print("Could not find DEFAULT_WS_URL in file.")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print("File write complete.")
