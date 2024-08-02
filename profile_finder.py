from profile_finder.linkedin import \
    LinkedInProfileFinder, scrape_linkedin_profile, get_summary_chain, Summary


if __name__ == '__main__':

    #name = 'Harrison Chase'
    name = 'Andrew Ng'

    linked_in_profile_finder = LinkedInProfileFinder(name_to_look=name)
    linked_in_profile_finder.acquire_user_url()
    url = linked_in_profile_finder.get_user_url()

    profile_data = scrape_linkedin_profile(linkedin_profile_url=url)
    summary_chain = get_summary_chain()
    summary_and_facts: Summary = summary_chain.invoke(
        input={"information": profile_data}
    )
    print(summary_and_facts.summary)
    print(summary_and_facts.facts[0])
    print(summary_and_facts.facts[1])

