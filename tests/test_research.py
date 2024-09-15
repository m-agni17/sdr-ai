import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def mock_serper_search(query: str):
    """
    Mock function to simulate Serper search results.
    """
    return {
        "results": [
            {
                "title": "Mock Company Overview",
                "snippet": "Mock snippet of company overview.",
                "link": "http://example.com"
            }
        ]
    }

def mock_perform_research(prospect_name: str, company_name: str):
    """
    Mock function to simulate perform_research function.
    """
    return {
        "research_report": "Mock research report content for testing."
    }

# Override the actual function with the mock function
@app.post("/research")
async def research(request: ResearchRequest):
    search_results = mock_serper_search(f"{request.prospect_name} {request.company_name}")
    task_description = f"Research and summarize information about {request.company_name} based on search results."
    crew_result = mock_perform_research(
        prospect_name=request.prospect_name,
        company_name=request.company_name
    )
    return crew_result

def test_research_success():
    response = client.post("/research", json={
        "prospect_name": "John Doe",
        "company_name": "Acme Corp",
        "additional_info": "Additional context here"
    })
    
    assert response.status_code == 200
    assert response.json() == {
        "research_report": "Mock research report content for testing."
    }

def test_research_missing_fields():
    response = client.post("/research", json={
        "prospect_name": "",
        "company_name": "Acme Corp",
        "additional_info": "Additional context here"
    })

    assert response.status_code == 422  # Unprocessable Entity error for missing required fields

def test_research_internal_server_error():
    # Simulate an internal server error by making the mock function raise an exception
    def faulty_perform_research(prospect_name: str, company_name: str):
        raise Exception("Simulated internal server error")

    global perform_research
    perform_research = faulty_perform_research

    response = client.post("/research", json={
        "prospect_name": "John Doe",
        "company_name": "Acme Corp",
        "additional_info": "Additional context here"
    })

    assert response.status_code == 500
    assert response.json() == {"detail": "Error performing research: Simulated internal server error"}

    # Restore the original function
    perform_research = mock_perform_research
