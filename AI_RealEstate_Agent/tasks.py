from agents import property_researcher_agent, property_analyst_agent

def research_task(topic: str) -> str:
    prompt = f"""
    Conduct a comprehensive market analysis of the {topic}.
    Focus on identifying current trends, emerging property hotspots, pricing patterns, infrastructure developments,
    and regulatory influences.
    Your report should detail key investment opportunities, market risks, and potential growth areas.
    Provide a thorough narrative supported by data from multiple credible sources.
    """
    return property_researcher_agent.run(prompt)

def write_task(topic: str, research_data: str) -> str:
    prompt = f"""
    Based on the detailed research provided below, compose a compelling market analysis article on the {topic}.
    The article should:
    1. Summarize the research findings.
    2. Clearly highlight market trends, investment opportunities, and risks.
    3. Offer insights for both investors and potential homebuyers.
    4. Be engaging, informative, and easy to understand.
    Format the article in markdown with 4 well-structured paragraphs.

    Research Data:
    {research_data}
    """
    return property_analyst_agent.run(prompt)
