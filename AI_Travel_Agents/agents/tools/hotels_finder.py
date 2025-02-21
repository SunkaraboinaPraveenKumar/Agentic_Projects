import os
from typing import Optional
from duckduckgo_search import DDGS
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class HotelsInput(BaseModel):
    q: str = Field(description='Location of the hotel')
    check_in_date: str = Field(description='Check-in date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    check_out_date: str = Field(description='Check-out date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    sort_by: Optional[str] = Field(8,
                                   description='Parameter is used for sorting the results. Default is sort by highest rating')
    adults: Optional[int] = Field(1, description='Number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Number of children. Default to 0.')
    rooms: Optional[int] = Field(1, description='Number of rooms. Default to 1.')
    hotel_class: Optional[str] = Field(
        None, description='Include only hotels of a certain class (e.g. 2,3,4 stars)')


class HotelsInputSchema(BaseModel):
    params: HotelsInput


@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    '''
    Find hotels using DuckDuckGo search.

    Returns:
        list: A list of search results related to hotels in the specified location.
    '''
    # Construct a query string from input parameters
    query = f"hotels in {params.q} check-in {params.check_in_date} check-out {params.check_out_date}"
    query += f" for {params.adults} adult(s)"
    if params.children:
        query += f" and {params.children} child(ren)"
    if params.rooms and params.rooms > 1:
        query += f" in {params.rooms} rooms"
    if params.hotel_class:
        query += f" with {params.hotel_class}-star hotels"
    if params.sort_by:
        query += " sorted by rating"

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=10)
    except Exception as e:
        results = str(e)

    # Return top 5 results if available
    if isinstance(results, list):
        return results[:5]
    return results
