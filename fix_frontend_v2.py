
import os
import re

file_path = "frontend/assets/main-nu7uwxNJ.js"

if not os.path.exists(file_path):
    print(f"❌ Error: {file_path} not found.")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read {len(content)} bytes.")

# Regex patterns to simulate what 'sed' might have done or '127.0.0.1' variants
# We simply want to match the whole assignment if possible to be safe
# Pattern 1: Match the current (likely broken) WebSocket URL assignment
# It looks like: DEFAULT_WS_URL="ws://'+window.location.host+'/client-ws"
# or similar variations.
# We will just look for the literal broken string sequence using regex escaping

# This regex matches: ws:// ' + window.location.host + ' /client-ws
# Handling potential spaces or quote variations
bad_ws_pattern = r"ws://'\+window\.location\.host\+'/client-ws"
bad_http_pattern = r"http://'\+window\.location\.host"

# Replacement: ws://"+window.location.host+"/client-ws
# We use double quotes for the string concatenation in JS
correct_ws = 'ws://"+window.location.host+"/client-ws'
correct_http = 'http://"+window.location.host'

# Perform regex substitution
new_content, n_ws = re.subn(bad_ws_pattern, correct_ws, content)
new_content, n_http = re.subn(bad_http_pattern, correct_http, new_content)

print(f"Found and replaced {n_ws} WebSocket URL instances.")
print(f"Found and replaced {n_http} Base URL instances.")

# Fallback: if regex didn't match, maybe it's still local host?
if n_ws == 0 and n_http == 0:
    print("⚠️  No regex matches for broken code. Checking for '127.0.0.1'...")
    new_content = new_content.replace("ws://127.0.0.1:12393/client-ws", correct_ws)
    new_content = new_content.replace("http://127.0.0.1:12393", correct_http)

if new_content != content:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ 프론트엔드 수리 완료! (Successfully patched)")
    # Print the context around the change to verify
    idx = new_content.find('DEFAULT_WS_URL')
    if idx != -1:
        print("Verifying patch result:")
        print(new_content[idx:idx+150])
else:
    print("❌ 변경된 내용이 없습니다. 이미 수정되었거나 패턴을 찾지 못했습니다.")
    # Show what is actually there
    idx = content.find('DEFAULT_WS_URL')
    if idx != -1:
        print("현재 파일 상태 (debugging):")
        print(content[idx:idx+150])
