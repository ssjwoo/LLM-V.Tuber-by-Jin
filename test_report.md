# Open-LLM-VTuber System Test Report
**Date:** 2026-01-13
**Status:** ✅ operational

## 1. System Configuration
| Component | Setting | Details |
| :--- | :--- | :--- |
| **LLM Provider** | `vertex_ai_llm` | **Model**: `gemini-2.0-flash`<br>**Project ID**: `gen-lang-client-0121173096`<br>**Location**: `us-central1` |
| **TTS Engine** | `edge_tts` | **Voice**: `en-US-AnaNeural` |
| **Config File** | `conf.yaml` | Validated & Cleaned (Unused providers removed) |

## 2. Modular Prompt System
Two new prompt modules have been implemented in `prompts/utils/`:
- `cot_prompt.txt`: Chain of Thought template.
- `scenario_prompt.txt`: Scenario/Roleplay template.

**Status**: Files exist. Currently **disabled** (commented out) in `conf.yaml`.
**To Enable**: Uncomment `cot_prompt` or `scenario_prompt` in the `tool_prompts` section of `conf.yaml`.

## 3. Verification & Fixes
### Verification Script (`verify_setup.py`)Result
- **Config Load**: ✅ Passed
- **LLM Connection**: ✅ Verified `vertex_ai_llm` active
- **TTS Configuration**: ✅ Verified `en-US-AnaNeural`
- **File Integrity**: ✅ Prompt files found
- **Server Run**: ✅ Manual run confirmed; connection and output 정상

### Applied Fixes
- **Issue**: `ValidationError` when loading config with `vertex_ai_llm`.
- **Root Cause**: `src/open_llm_vtuber/config_manager/agent.py` was missing `vertex_ai_llm` in the `Literal` type definition for `llm_provider`.
- **Fix**: Added `vertex_ai_llm` to the allowed list in `BasicMemoryAgentConfig`.

## 4. Next Steps
To run the server:
```bash
python run_server.py
```
 
## 5. Known Issues
- Frontend submodule fetch may fail in restricted networks (GitHub unreachable); backend config verification can still pass.
- `uv run` may hit cache permission errors for MCP tool startup; set `UV_CACHE_DIR` to a writable path if needed.
