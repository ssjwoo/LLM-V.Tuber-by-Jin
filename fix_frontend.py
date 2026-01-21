
import os

file_path = "frontend/assets/main-nu7uwxNJ.js"

# 1. 엉망이 된 부분 찾기 (작은따옴표가 들어간 문자열)
bad_ws = "ws://'+window.location.host+'/client-ws"
bad_http = "http://'+window.location.host"

# 2. 이쁘게 고칠 내용 (큰따옴표로 감싼 정상 코드)
correct_ws = 'ws://"+window.location.host+"/client-ws'
correct_http = 'http://"+window.location.host'

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 3. 교체 수술 집도
    new_content = content.replace(bad_ws, correct_ws)
    new_content = new_content.replace(bad_http, correct_http)

    # 4. 혹시 몰라 원본(127.0.0.1)도 같이 처리
    new_content = new_content.replace("ws://127.0.0.1:12393/client-ws", correct_ws)
    new_content = new_content.replace("http://127.0.0.1:12393", correct_http)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ 프론트엔드 수리 완료! (Successfully patched)")
    else:
        print("⚠️ 변경된 내용이 없습니다. (이미 수정되었거나, 찾지 못함)")
        # 디버깅을 위해 일부 내용 출력
        print("현재 파일 내용 일부:", content[:500] if len(content) > 500 else content)

except FileNotFoundError:
    print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    print("현재 경로:", os.getcwd())
    print("파일 목록:", os.listdir("."))
