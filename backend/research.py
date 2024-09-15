import requests
from crewai import Agent, Task, Crew
from langchain_ollama import ChatOllama
from typing import Dict, Any

SERPER_API_URL = "https://google.serper.dev/search"
SERPER_API_KEY = "a939292e37152b3d04a7e1539be304105c47eb98"



llm = ChatOllama(
    model="llama3.1",
    base_url="http://localhost:11434"  
)

research_agent = Agent(
    role="Research Assistant",
    goal="""Generate a detailed research report about a company prospect by analyzing retrieved search content, 
    including recent news, company overview, key contacts, and industry trends.""",
    backstory="You are an AI-powered research assistant skilled at extracting relevant information from search results.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
    max_tokens=200
)

def serper_search(query: str) -> Dict[str, Any]:
    """
    Search Google using Serper API.
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY
    }
    data = {
        "q": query
    }
    
    response = requests.post(SERPER_API_URL, json=data, headers=headers)
    print(response.json())
    response.raise_for_status()
    
    return response.json()

def perform_research(prospect_name: str, company_name: str) -> Dict[str, Any]:
    """
    Perform research using Serper search results and generate a detailed report using CrewAI.
    """
    search_query = f"{prospect_name} {company_name}"
    search_results = serper_search(search_query)
    
    task_description = f"Research and summarize information about {company_name} based on search results.Take the input data and generate a detailed research report.Don't generate any fake data."
    task = Task(
        description=task_description,
        agent=research_agent,
        expected_output="A detailed research report based on the search results.Should not be fake only genuine and data from input.",
        input_data=search_results
    )
    crew = Crew(
        agents=[research_agent],
        tasks=[task],
        verbose=True
    )
    crew_result = crew.kickoff()

    result={"research_report": crew_result}
    
    return result
