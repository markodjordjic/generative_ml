# %% [markdown]
# # Acquisition and Summarization of Profile Data from LinkedIn
# This demo will provide an insight how to use wide variety of 
# `langchain` classes to get an valid URL of the LinkedIn profile, 
# scrape the data from the LinkedIn profile, and summarize the scraped
# data.
# The implementation revolves around `PromptTemplate` which is utilized
# to formulate the prompt towards the agent, and `PydanticOutputParser`
# to conveniently format retrieved data, thus saving a lot of work.
# The scraping is performed via commercial API Proxicurl.
# The job to summarize the scraped data has been assigned to OpenAIs 
# GPT3.5-Turbo. Class hierarchy is displayed below.
# ![image info](classes.jpg)
# Firstly, let us make the necessary imports.
# %%
from profile_finder.linkedin import \
    LinkedInProfileFinder, LinkedInProfileScraper, Summarizer

# %% [markdown]
# We can start first with a successful example. The sucessfulness is 
# reflected in the ability to acquire the URL of the correct person.
# Assumption that multiple persons share the same name, is an obstacle
# in some cases.
# %%
name = 'Harrison Chase'
linked_in_profile_finder = LinkedInProfileFinder(name_to_look=name)
linked_in_profile_finder.acquire_user_url()
url = linked_in_profile_finder.get_user_url()
print(url)
# %% [md]
# While, it is reasonable to assume that most of the time the search 
# will produce a valid URL towards the profile on the LinkedIn network
# correctness will be revealed when summarizing data. Before that, the
# data needs to be scraped off the profile.
# %%
scraper = LinkedInProfileScraper(linkedin_profile_url=url)
scraper.scrape_linkedin_data()
data = scraper.get_scraped_data()
# %% [md]
# Now let us instantiate summarizer and see how good was the search.
# %%
summarizer = Summarizer(profile_data=data)
summarizer.make_summary()
summary = summarizer.get_summary()
# %% [md]
# Here is the summary
# %%
print(summary.summary)
# %% [md]
# And here are the two *interesting* facts.
# %%
print(summary.facts[0])
print(summary.facts[1])
# %% [md]
# In this case the search has been successful. By using the same classes
# and methods, let us examine our success with another of legend of 
# machine learning.
# %%
name = 'Andrew Ng'
linked_in_profile_finder = LinkedInProfileFinder(name_to_look=name)
linked_in_profile_finder.acquire_user_url()
url = linked_in_profile_finder.get_user_url()
print(url)
# %% [md]
# Acquired URL does not to seem to point in correct direction. Let us
# execute the rest of the pipeline.
# %%
scraper = LinkedInProfileScraper(linkedin_profile_url=url)
scraper.scrape_linkedin_data()
data = scraper.get_scraped_data()
summarizer = Summarizer(profile_data=data)
summarizer.make_summary()
summary = summarizer.get_summary()
# %% [markdown]
# Let us now see the results. Firstly, the summary.
# %%
print(summary.summary)
# %% [markdown]
# And now the facts.
# %%
print(summary.facts[0])
print(summary.facts[1])
# %% [md]
# This example was less successful and displays the challenges that
# might occur when performing these kinds of tasks. 