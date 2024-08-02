import os
from utilities.general import environment_reader, to_single_line
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from tools.tools import get_profile_url_tavily

ENVIRONMENT = environment_reader(env_file='./.env')


class GenericAgent:
    """Base class with common methods fro all agents
    
    """

    OPENAI_API_KEY = ENVIRONMENT['OPENAI_API_KEY']

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=OPENAI_API_KEY,
    )

    def __init__(self, name_to_look: str = None) -> None:
        self.name_to_look = name_to_look


class LinkedInAgent(GenericAgent):
    """Agent for extraction of LinkedIn profile URL
    
    """
    
    prompt_text = to_single_line("""
I will provide you with a first name and last name of the person. Take
these names and provide me with an Hyperlink to their profile on
www.linkedin.com web-site. In your answer do not provide any other
information except the link to their profile. Here is the first and the 
last name of the person {first_and_last_name}. 
""")
    
    react_prompt = hub.pull("hwchase17/react")

    def __init__(self, name_to_look: str = None) -> None:
        super().__init__(name_to_look)
        self.name_to_look = name_to_look
        self.prompt = PromptTemplate(
            template=self.prompt_text, input_variables=self.name_to_look
        )
        self._tools = [Tool()]        
        self._agent = None
        self._agent_executor = None
        self._raw_result = None

    def _create_agent(self) -> None:
        self._agent = create_react_agent(
            llm=self.llm, 
            tools=self._tools, 
            prompt=self.react_prompt
        )

    def _execute(self):
        assert self._agent, 'No agent.'

        self._agent_executor = AgentExecutor(
            agent=self._agent,
            tools=self._tools, 
            verbose=True
        )

    def _get_raw_resut(self):
        self._raw_result = self._agent_executor.invoke(input={
            "input": self.prompt.format_prompt(
                name_of_person=self.name_to_look
            )
        })
    
    def execute(self):
        self._create_agent()
        self._execute()

    def get_profile(self):

        assert self._raw_result, "No results."

        return self._raw_result["output"]




    