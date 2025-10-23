from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.exceptions import AgentRunError, UsageLimitExceeded, UnexpectedModelBehavior
from loguru import logger

from src.models import ParsedTransactions


class ModelServiceException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ModelService:
    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        instructions: str,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.instructions = instructions

    @property
    def agent(self) -> Agent:
        settings = GoogleModelSettings(
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
        )
        provider = GoogleProvider(api_key=self.api_key)
        model = GoogleModel(model_name=self.model_name, provider=provider)
        return Agent(
            model=model,
            model_settings=settings,
            instructions=self.instructions,
            output_type=ParsedTransactions,
        )

    async def parse_transactions(self, statement: str) -> ParsedTransactions:
        try:
            result = await self.agent.run(user_prompt=statement)
            return result.output
        except UsageLimitExceeded as e:
            logger.warning(f"Usage limit exceeded: {str(e)}")
            raise ModelServiceException(f"Usage limit exceeded: {str(e)}") from e
        except UnexpectedModelBehavior as e:
            logger.warning(f"Unexpected model behavior: {str(e)}")
            raise ModelServiceException(f"Unexpected model behavior: {str(e)}") from e
        except AgentRunError as e:
            logger.warning(f"Agent run error: {str(e)}")
            raise ModelServiceException(f"Agent run error: {str(e)}") from e
