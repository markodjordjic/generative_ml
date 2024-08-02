import requests
from typing import List, Dict, Any
from langchain.prompts.prompt import PromptTemplate
from utilities.general import environment_reader
from profile_finder.agents import LinkedInAgent
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI


ENVIRONMENT = environment_reader(env_file='./.env')

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}

summary_parser = PydanticOutputParser(pydantic_object=Summary)


class GenericProfileFinder:

    def __init__(self, name_to_look: str = None) -> None:
        self.name_to_look = name_to_look
        self._agent = None

class LinkedInProfileFinder(GenericProfileFinder) :

    def __init__(self, name_to_look: str = None) -> None:
        super().__init__(name_to_look)
        self.name_to_look = name_to_look

    def _instantiate_agent(self):
        assert self.name_to_look is not None, 'Name to look not provided.'
        self._agent = LinkedInAgent(name_to_look=self.name_to_look)

    def acquire_user_url(self):
        self._instantiate_agent()
        self._agent.execute()

    def get_user_url(self):

        return self._agent.get_profile()

def scrape_linkedin_profile(linkedin_profile_url: str):
    PROXYCURL_API_KEY = ENVIRONMENT['PROXYCURL_API_KEY']

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    header_dic = {"Authorization": f'Bearer {PROXYCURL_API_KEY}'}

    response = requests.get(
        api_endpoint,
        params={"url": linkedin_profile_url},
        headers=header_dic,
        timeout=10
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

def get_summary_chain() -> RunnableSequence:
    summary_template = """
         given the information about a person from linkedin {information}:
         1. a short summary
         2. two interesting facts about them
         \n{format_instructions}
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    return summary_prompt_template | llm | summary_parser
