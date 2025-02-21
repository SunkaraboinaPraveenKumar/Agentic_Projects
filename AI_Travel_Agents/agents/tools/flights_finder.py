import os
from typing import Optional

from duckduckgo_search import DDGS
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class FlightsInput(BaseModel):
    departure_airport: Optional[str] = Field(description='Departure airport code (IATA)')
    arrival_airport: Optional[str] = Field(description='Arrival airport code (IATA)')
    outbound_date: Optional[str] = Field(description='Outbound date in YYYY-MM-DD format (e.g. 2024-06-22)')
    return_date: Optional[str] = Field(description='Return date in YYYY-MM-DD format (e.g. 2024-06-28)')
    adults: Optional[int] = Field(1, description='Number of adults (default: 1)')
    children: Optional[int] = Field(0, description='Number of children (default: 0)')
    infants_in_seat: Optional[int] = Field(0, description='Number of infants in seat (default: 0)')
    infants_on_lap: Optional[int] = Field(0, description='Number of infants on lap (default: 0)')


class FlightsInputSchema(BaseModel):
    params: FlightsInput


@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
    '''
    Find flights using the DuckDuckGo search engine.

    Returns:
        list: A list of search results related to the flight query.
    '''
    # Construct a query string from input parameters
    query = f"flights from {params.departure_airport} to {params.arrival_airport}"
    if params.outbound_date:
        query += f" departing on {params.outbound_date}"
    if params.return_date:
        query += f" returning on {params.return_date}"
    if params.adults:
        query += f" for {params.adults} adult(s)"
    if params.children:
        query += f", {params.children} child(ren)"
    if params.infants_in_seat:
        query += f", {params.infants_in_seat} infants in seat"
    if params.infants_on_lap:
        query += f", {params.infants_on_lap} infants on lap"

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=10)
    except Exception as e:
        results = str(e)

    return results
