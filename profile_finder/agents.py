from utilities.general import environment_reader
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

ENVIRONMENT = environment_reader(env_file='./.env')


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    
    return res[0]["url"]

class GenericAgent:
    """Base class with common methods fro all agents
    
    """

    OPENAI_API_KEY = ENVIRONMENT['OPENAI_API_KEY']

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=OPENAI_API_KEY
    )

    def __init__(self, name_to_look: str = None) -> None:
        self.name_to_look = name_to_look


class LinkedInAgent(GenericAgent):
    """Agent for extraction of LinkedIn profile URL
    
    """
    
    prompt_text = """You are a search assistant. Your job is to find
    LinkedIn profile of a person. I will provide you with a full name of 
    a person. Take this full name and find the profile of this person
    www.linkedin.com web-site. When you find the person reply back to me.
    Do not provide any other information except the link to their 
    profile. Do not provide links like this: 
    https://www.linkedin.com/pub/dir/ or https://www.linkedin.com/posts/.
    The profile of the person should start like this: 
    https://www.linkedin.com/in/. Search for the Linkedin profile of this 
    person {full_name}."""
    
    react_prompt = hub.pull("hwchase17/react")

    def __init__(self, name_to_look: str = None) -> None:
        super().__init__(name_to_look)
        self.name_to_look = name_to_look
        self.prompt = PromptTemplate(
            template=self.prompt_text, input_variables=self.name_to_look
        )
        self._tools = [Tool(
            name="Search Google for URL of LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )]        
        self._agent = None
        self._agent_executor = None
        self._raw_result = None

    def _create_agent(self) -> None:
        self._agent = create_react_agent(
            llm=self.llm, 
            tools=self._tools, 
            prompt=self.react_prompt
        )

    def _create_executor(self) -> None:
        assert self._agent is not None, 'No agent.'

        self._agent_executor = AgentExecutor(
            agent=self._agent,
            tools=self._tools, 
            verbose=False
        )

    def _get_raw_result(self) -> None:
        self._raw_result = self._agent_executor.invoke(input={
            "input": self.prompt.format_prompt(
                full_name=self.name_to_look
            )
        })
    
    def execute(self) -> None:
        self._create_agent()
        self._create_executor()
        self._get_raw_result()

    def get_profile(self) -> str:

        assert self._raw_result is not None, "No results."

        return self._raw_result["output"]




    