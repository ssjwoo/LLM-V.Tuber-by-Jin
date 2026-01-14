import sys
import os
import asyncio

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from open_llm_vtuber.agent.stateless_llm.vertex_ai_llm import VertexAILLM
    print("✅ Successfully imported VertexAILLM")
except ImportError as e:
    print(f"❌ Failed to import VertexAILLM: {e}")
    sys.exit(1)

async def test():
    print("Attempting to instantiate VertexAILLM...")
    try:
        # Using dummy values. This might fail at vertexai.init if auth is missing, 
        # but we want to see if the class itself is valid (no abstract methods missing).
        llm = VertexAILLM(
            project_id="test-project",
            location="us-central1",
            model="gemini-pro"
        )
        print("✅ Successfully instantiated VertexAILLM")
        
        # Test chat_completion method existence
        if hasattr(llm, "chat_completion"):
             print("✅ client has chat_completion method")
        else:
             print("❌ client MISSING chat_completion method")

    except Exception as e:
        print(f"⚠️ Instantiation failed (expected if no auth): {e}")
        # Check if the error is related to Abstract methods
        if "Can't instantiate abstract class" in str(e):
             print("\n❌ CRITICAL: Abstract Method Error still present!")
        else:
             print("ℹ️ Likely auth error, which means class structure is OK.")

if __name__ == "__main__":
    asyncio.run(test())
