import os
from dotenv import load_dotenv
from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.local.agent_memory import DemoAgentMemory

load_dotenv()

# 1. User Resolver: Identifies every request as coming from a default 'admin' user
class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(id="admin", username="admin", permissions=["admin"])

def get_agent():
    # 2. LLM Service (Using Google Gemini)
    llm = GeminiLlmService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash"
    )

    # 3. Database Runner
    runner = SqliteRunner(database_path="clinic.db")

    # 4. Tool Registry: Register core SQL and Visualization tools
    registry = ToolRegistry()
    registry.register(RunSqlTool(sql_runner=runner))
    registry.register(VisualizeDataTool())
    registry.register(SaveQuestionToolArgsTool())
    registry.register(SearchSavedCorrectToolUsesTool())

    # 5. Initialize Agent with Memory
    agent = Agent(
        llm_service=llm,
        tool_registry=registry,
        user_resolver=SimpleUserResolver(),
        agent_memory=DemoAgentMemory(), # Learns from interactions
        config=AgentConfig(stream_responses=False)
    )
    return agent