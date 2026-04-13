import os
from dotenv import load_dotenv
from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.google import GeminiLlmService
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.core.user import UserResolver, User, RequestContext

# Load environment variables
load_dotenv(dotenv_path=r"C:\Users\Anita sukre\OneDrive\Desktop\intern_assignment\.env")

class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(id="admin", username="admin")

def get_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key: 
        raise ValueError("GOOGLE_API_KEY is missing!")

    llm = GeminiLlmService(api_key=api_key, model="gemini-2.5-flash")
    runner = SqliteRunner(database_path="clinic.db")
    
    # 1. Initialize an empty registry
    registry = ToolRegistry()

    # 2. Define the tools
    run_sql = RunSqlTool(sql_runner=runner)
    viz_tool = VisualizeDataTool()
    save_tool = SaveQuestionToolArgsTool()
    search_tool = SearchSavedCorrectToolUsesTool()

 
    registry.tools = [run_sql, viz_tool, save_tool, search_tool]

    # 4. Initialize Agent

    agent = Agent(
        registry,
        llm,
        user_resolver=SimpleUserResolver(),
        agent_memory=DemoAgentMemory(),
        config=AgentConfig(stream_responses=False)
    )
    
    return agent
