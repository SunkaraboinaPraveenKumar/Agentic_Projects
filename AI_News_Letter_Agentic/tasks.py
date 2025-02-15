from agents import researcher_agent, writer_agent, proof_reader_agent

def research_task(topic: str) -> str:
    prompt = f"""
    Identify the next big trend in the topic: {topic}.
    Focus on identifying pros and cons and the overall narrative.
    Your final report should clearly and explicitly articulate the key points,
    market opportunities, and potential risks associated with the given topic.
    """
    return researcher_agent.run(prompt)

def write_task(topic: str, research_data: str) -> str:
    prompt = f"""
    Compose an insightful article on the topic: {topic}.
    Focus on the latest trends and how they're impacting the industry.
    Please incorporate the following research data:
    {research_data}
    
    This article should be digestible, easy to understand, engaging, and positive.
    Format the output as markdown, and aim for a 4-paragraph structure.
    """
    return writer_agent.run(prompt)

def proof_read_task(topic: str, article: str) -> str:
    prompt = f"""
    Finalize the following article on the topic: {topic}.
    Ensure that the article is polished, accurate, and well-structured.
    Check for clarity, grammar, and factual accuracy. Cite sources where relevant,
    and include 3 additional sources for further study.
    
    Article to proofread:
    {article}
    """
    return proof_reader_agent.run(prompt)
