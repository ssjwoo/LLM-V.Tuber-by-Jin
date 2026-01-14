from typing import AsyncGenerator, List, Dict, Any, AsyncIterator
from loguru import logger
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Content, Part

from .stateless_llm_interface import StatelessLLMInterface


class VertexAILLM(StatelessLLMInterface):
    """
    LLM provider for Google Cloud Vertex AI (Gemini).
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        model: str,
        max_output_tokens: int | None = None,
        temperature: float = 1.0,
        safety_settings: dict | None = None,
        system_prompt: str | None = None,
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.system = system_prompt
        
        # Configure safety settings
        if safety_settings:
            self.safety_settings = [
                SafetySetting(
                    category=getattr(SafetySetting.HarmCategory, k),
                    threshold=getattr(SafetySetting.HarmBlockThreshold, v),
                )
                for k, v in safety_settings.items()
            ]
        else:
            self.safety_settings = None

        # Initialize Vertex AI
        try:
            vertexai.init(project=project_id, location=location)
            self._init_model()
            logger.info(f"Vertex AI initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI: {e}")
            raise e

    def _init_model(self):
        """Helper to initialize the GenerativeModel instance."""
        self.model = GenerativeModel(
            model_name=self.model_name,
            system_instruction=[self.system] if self.system else None,
            safety_settings=self.safety_settings
        )

    def set_system_prompt(self, system_prompt: str):
        if system_prompt != self.system:
            self.system = system_prompt
            self._init_model()

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        system: str = None,
        tools: List[Dict[str, Any]] = None,
    ) -> AsyncIterator[str]:
        """
        Generates a chat completion asynchronously.
        """
        # handling system prompt
        if system and system != self.system:
            self.set_system_prompt(system)

        # Convert messages to Vertex AI format
        history = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            if not content:
                continue

            if role == "system":
                # System prompt is handled via system_instruction/set_system_prompt
                # Ignoring inline system messages effectively as they are usually duplicate
                pass
            elif role == "user":
                history.append(
                    Content(role="user", parts=[Part.from_text(str(content))])
                )
            elif role == "assistant":
                # Model responses must have role "model"
                history.append(
                    Content(role="model", parts=[Part.from_text(str(content))])
                )

        if not history:
            yield ""
            return

        # Vertex AI start_chat expects history of previous turns. 
        # The last message is the trigger for the new response.
        last_message = history.pop()
        
        # Ensure last message is from user interaction flow. 
        # If the history ended with model, start_chat might get confused or we just send empty?
        # Standard chat completion assumes user sends a message.
        if last_message.role != "user":
            # If for some reason last message is model (e.g. continue), we might need to handle differently.
            # But for VTuber use case, it's usually user input.
            # We will just put it back for now if logic requires, but start_chat needs history.
            pass

        chat_session = self.model.start_chat(history=history)
        
        generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
        }

        try:
            response_stream = await chat_session.send_message_async(
                last_message.parts[0].text,
                generation_config=generation_config,
                # safety_settings are already in model init, but can be overridden here
                stream=True
            )

            async for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error in Vertex AI generation: {e}")
            yield f"[Error: {e}]"
