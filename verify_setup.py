import sys
import os

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from open_llm_vtuber.config_manager import read_yaml, validate_config
    
    print("Loading conf.yaml...")
    config_data = read_yaml("conf.yaml")
    config = validate_config(config_data)
    
    print("\n--- Configuration Validation ---")
    print(f"✅ Config Load Success")
    
    # Check LLM
    agent_settings = config.character_config.agent_config.agent_settings
    llm_provider = agent_settings.basic_memory_agent.llm_provider
    print(f"ℹ️ Active LLM Provider: {llm_provider}")
    
    if llm_provider == 'vertex_ai_llm':
        print("✅ Vertex AI is selected.")
    else:
        print(f"❌ Warning: Vertex AI is NOT selected. Current: {llm_provider}")

    # Check TTS
    tts_model = config.character_config.tts_config.tts_model
    print(f"ℹ️ Active TTS Model: {tts_model}")
    if tts_model == 'edge_tts':
        voice = config.character_config.tts_config.edge_tts.voice
        print(f"   Voice: {voice}")
        if voice == 'en-US-AnaNeural':
             print("✅ Edge TTS (Ana) is correctly configured.")
        else:
             print("⚠️ Edge TTS voice might not be Ana.")
    else:
        print(f"⚠️ Warning: TTS is not Edge TTS.")

    # Check Modular Prompts
    print("\n--- Prompt File Verification ---")
    prompts_to_check = ['prompts/utils/cot_prompt.txt', 'prompts/utils/scenario_prompt.txt']
    for p in prompts_to_check:
        if os.path.exists(p):
            print(f"✅ Found {p}")
            with open(p, 'r') as f:
                content = f.read().strip()
                print(f"   Preview: {content[:50]}...")
        else:
            print(f"❌ Missing {p}")

    # Check Prompt Generation Logic (Simulated)
    print("\n--- Prompt Integration Check ---")
    tool_prompts = config.system_config.tool_prompts
    print(f"ℹ️ Registered Tool Prompts in config: {list(tool_prompts.keys())}")
    
    if 'cot_prompt' in tool_prompts:
        print("✅ 'cot_prompt' is enabled in config.")
    else:
        print("ℹ️ 'cot_prompt' is strictly NOT commented out? (Wait, config parser skips comments)")
        # If it's commented out in yaml, it won't appear here.
        print("ℹ️ 'cot_prompt' is not currently active (commented out or missing).")

    if 'scenario_prompt' in tool_prompts:
        print("✅ 'scenario_prompt' is enabled in config.")
    else:
        print("ℹ️ 'scenario_prompt' is not currently active.")


except Exception as e:
    print(f"\n❌ Validation Failed: {e}")
    import traceback
    traceback.print_exc()
