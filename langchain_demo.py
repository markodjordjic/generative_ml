# %% [markdown]
# # Text Summarization with Local Version of LLAMA
# 
# In the field of Generative AI, it is possible to observe two distinct 
# modes of utilization of LLMs, with the respect to their source. While
# LLMs are readily available via APIs, which would be the main mode
# of their utilization, it is also possible for some of them to
# install them locally and interface to them without going the API 
# route.
# The objective of this demo is to investigate the usage of locally
# available LLM for the purposes of summarizing a piece of text. The 
# LLM of choice is LLAMA3 and the demo also consists of usage of
# langchain to interface with the underlying locally available LLM.
# Firstly, let us make the necessary imports.
# %% 
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
# %% [markdown]
# Let us make a simple template for the summarization of the piece of 
# text that will go into the LLM. We will ask for a short summary, and
# two facts within limited number of characters.
# %% 
template = """
Given the information {information} about the person I want you to create
1. A short summary (no longer than 256 characters)
2. Two facts about that person (no longer than 64 characters)
"""
# %% [markdown]
# Now let us make a chain of thought via interfaces provided by the
# `langchain`, and attach to it `StrOutputParser` so it would be 
# possible to get a clear output in a more convenient way.
# %% 
prompt_template = PromptTemplate(
    input_variables="information",
    template=template
)
llm = ChatOllama(temperature=0, model='llama3')
chain = prompt_template | llm | StrOutputParser()
# %% [markdown]
# Finally, here is an excerpt from information available on Wikipeda
# about a famous actor. The piece of text is 1500 characters long, 
# without counting the spaces.
# %%
information = r"""
Humphrey DeForest Bogart (1] December 25, 1899 – January 14, 1957), 
colloquially nicknamed Bogie, was an American actor. His 
performances in classic Hollywood cinema films made him an American 
cultural icon.[2] In 1999, the American Film Institute selected Bogart 
as the greatest male star of classic American cinema.[3]
Bogart began acting in Broadway shows. Debuting in film in The Dancing 
Town (1928), he appeared in supporting roles for more than a 
decade, regularly portraying gangsters. He was praised for his work as 
Duke Mantee in The Petrified Forest (1936). Bogart also received 
positive reviews for his performance as gangster Hugh "Baby Face" 
Martin, in Dead End (1937), directed by William Wyler.
His breakthrough came in High Sierra (1941), and he catapulted to 
stardom as the lead in John Huston's The Maltese Falcon (1941), 
considered one of the first great noir films.[4] Bogart's private 
detectives, Sam Spade (in The Maltese Falcon) and Philip Marlowe 
(in 1946's The Big Sleep), became the models for detectives in other 
noir films. In 1947, he played a war hero in another "noir" film, Dead 
Reckoning, tangled in a dangerous web of brutality and violence as 
he investigates his friend's murder, co-starring Lizabeth Scott. His 
first romantic lead role was a memorable one, as Rick Blaine, paired 
with Ingrid Bergman in Casablanca (1942), which earned him his first 
nomination for the Academy Award for Best Actor. Blaine was ranked 
as the fourth greatest hero of American cinema by the American Film 
Institute and his and Ingrid Bergman's character's relationship the 
greatest love story in American cinema, also by the American Film 
Institute. Raymond Chandler, in a 1946 letter, wrote that "Like 
Edward G. Robinson when he was younger, all he has to do to dominate a 
scene is to enter it."[5]
"""
# %% [markdown]
# All that is left is to run the chain and get the output.
# %%
result = chain.invoke(input={"information": information})
# %% [markdown]
# Let us take a look at the parsed output.
# %%
print(result)
# %% [markdown]
# It it important to note that local utilization of the LLAMA3 might be
# slower, depending on the hardware available. Yet, again the mode of
# utilization is dependant on the actual requirements, and constraints.