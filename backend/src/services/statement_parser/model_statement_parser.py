from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.exceptions import AgentRunError, UsageLimitExceeded, UnexpectedModelBehavior
from loguru import logger

from src.models import ParsedTransaction, Transaction


class ModelStatementParserException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ModelStatementParser:
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
            output_type=list[ParsedTransaction],
        )

    async def parse_transactions(self, bank_name: str, statement: str) -> list[Transaction]:
        try:
            result = await self.agent.run(user_prompt=statement)
            parsed_transactions: list[ParsedTransaction] = result.output
            return [
                Transaction.from_parsed_transaction(bank_name=bank_name, parsed_transaction=transaction)
                for transaction in parsed_transactions
            ]
        except UsageLimitExceeded as e:
            logger.warning(f"Usage limit exceeded: {str(e)}")
            raise ModelStatementParserException(f"Usage limit exceeded: {str(e)}") from e
        except UnexpectedModelBehavior as e:
            logger.warning(f"Unexpected model behavior: {str(e)}")
            raise ModelStatementParserException(f"Unexpected model behavior: {str(e)}") from e
        except AgentRunError as e:
            logger.warning(f"Agent run error: {str(e)}")
            raise ModelStatementParserException(f"Agent run error: {str(e)}") from e
