from dataclasses import dataclass
import requests
from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI
from utilities.general import environment_reader
from profile_finder.agents import LinkedInAgent


ENVIRONMENT = environment_reader(env_file='./.env')

class Summary(BaseModel):
    summary: str = Field(description="Summary")
    facts: list[str] = Field(description="Facts")

    def to_dict(self) -> dict[str, str]:
        
        return {"summary": self.summary, "facts": self.facts}


class GenericProfileFinder:

    def __init__(self, name_to_look: str = None) -> None:
        self.name_to_look = name_to_look
        self._agent = None

class LinkedInProfileFinder(GenericProfileFinder):

    def __init__(self, name_to_look: str = None) -> None:
        super().__init__(name_to_look)

    def _instantiate_agent(self):
        assert self.name_to_look is not None, 'Name to look not provided.'
        
        self._agent = LinkedInAgent(name_to_look=self.name_to_look)

    def acquire_user_url(self):
        self._instantiate_agent()
        self._agent.execute()

    def get_user_url(self):

        return self._agent.get_profile()
    

class LinkedInProfileScraper:

    PROXYCURL_API_KEY = ENVIRONMENT['PROXYCURL_API_KEY']

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    header = {"Authorization": f'Bearer {PROXYCURL_API_KEY}'}

    def __init__(self, linkedin_profile_url: str) -> None:
        self.linkedin_profile_url = linkedin_profile_url
        self._response = None
        self._data = None

    def _scrape_linkedin_profile(self):

        assert self.linkedin_profile_url is not None, 'No profile.'

        self._response = requests.get(
            self.api_endpoint,
            params={"url": self.linkedin_profile_url},
            headers=self.header,
            timeout=10
        )

    def _extract_data(self) -> None:

        assert self._response is not None, 'No response'

        data = self._response.json()
        data = {
            k: v
            for k, v in data.items()
            if (v not in ([], "", "", None))
            and (k not in ["people_also_viewed", "certifications"])
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        self._data = data

    def scrape_linkedin_data(self) -> None:
        self._scrape_linkedin_profile()
        self._extract_data()

    def get_scraped_data(self):

        assert self._data is not None, 'No extracted data'
        
        return self._data

class Summarizer:

    summary_template = """
        Buy taking into account this information {information} collected 
        about a person create:
            1. a summary about the person, and a list
            2. of two interesting facts about them.
        Do not exceed 384 characters in your response.
        Format your response according to the following instructions: 
        {format_instructions}
    """
      
    summary_parser = PydanticOutputParser(pydantic_object=Summary)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )

    def __init__(self, profile_data: dict) -> None:
        self.profile_data = profile_data
        self._chain: RunnableSequence = None
        self._summary: Summary = None   

    def _get_summary_chain(self):
        self._chain = \
            self.summary_prompt_template | self.llm | self.summary_parser
        
    def make_summary(self) -> None:

        assert self.profile_data is not None, 'No profile data'

        self._get_summary_chain()
        self._summary = self._chain.invoke(
            input={"information": self.profile_data}
        )

    def get_summary(self) -> Summary:

        return self._summary
