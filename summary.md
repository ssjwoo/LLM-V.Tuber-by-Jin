# Open-LLM-VTuber Configuration Handover

## 1. Core Configuration (`conf.yaml`)
- **LLM Provider**: `vertex_ai_llm` (Project ID: `gen-lang-client-0121173096`, Model: `gemini-2.0-flash`)
- **TTS Provider**: `edge_tts` (Voice: `en-US-AnaNeural`)
- **System Language**: Reverted to default multilingual handling (Japanese/Korean specific phonetics removed).
- **Disabled Modules**: `filesystem` MCP server (package missing on PyPI).

## 2. Key Code Fixes
- **Vertex AI LLM Implementation**:
  - Implemented missing `chat_completion` method in `src/open_llm_vtuber/agent/stateless_llm/vertex_ai_llm.py`.
  - Fixed `ValueError` by enabling strict `Content` object usage for history.
  - Fixed `TypeError` by correcting attribute access (`.parts[0].text` instead of dict access).
- **Config Validation**:
  - Added `vertex_ai_llm` to allowed `Literal` types in `agent.py` config model.

## 3. Operational Guide
- **Start Server**: `uv run run_server.py`
- **Address**: `http://localhost:12393`
- **Troubleshooting**:
  - If "Undefined model" error persists: Clear browser LocalStorage or use Incognito mode.
  - If TTS fails: Ensure `ffmpeg` is installed (`sudo apt install ffmpeg`).

## 4. Pending/Known Issues
- **Frontend Submodule**: Fetch failed due to network, but runtime initialization succeeded.
- **MCP Filesystem**: Disabled in `conf.yaml` to prevent startup crash.
