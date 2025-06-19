from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from nmdc_api_utilities import data_object_search, minter, biosample_search, data_generation_search, functional_search, lat_long_filters
import logging 
logging.basicConfig(level=logging.INFO)
# Initialize FastMCP server
mcp = FastMCP("nmdc")

# Constants
NMDC_API_BASE = "https://api.microbiomedata.org/.gov"
USER_AGENT = "nmdc-app/1.0"

async def make_nmdc_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NMDC API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

@mcp.tool()
async def get_data_objects() -> str:
    """Get data objects from NMDC API."""
    do = data_object_search.DataObjectSearch()
    results = do.get_records()
    return results

# @mcp.tool()
# async def get_minted_ids(nmdc_type:str) -> str:
#     """Get minted IDs from NMDC API."""
#     from dotenv import load_dotenv

#     import os
#     load_dotenv()
#     client_id = os.getenv("NMDC_CLIENT_ID")
#     client_secret = os.getenv("NMDC_CLIENT_SECRET")
#     mint = minter.Minter()
#     results = mint.mint(nmdc_type=nmdc_type, client_id=client_id, client_secret=client_secret)
#     return results

@mcp.tool()
async def get_biosamples() -> str:
    """Get biosamples from NMDC API."""
    bs = biosample_search.BiosampleSearch()
    results = bs.get_records()
    return results

@mcp.tool()
async def get_data_generation() -> str:
    """Get data generation records from NMDC API."""
    dgs = data_generation_search.DataGenerationSearch()
    results = dgs.get_records()
    return results

@mcp.tool()
async def get_functional_data() -> str:
    """Get functional data from NMDC API."""
    fs = functional_search.FunctionalSearch()
    results = fs.get_records()
    return results

@mcp.tool()
async def get_biosample_by_lat_long_data(lat_comparison:str, lon_comparison:str, lat: float, long: float) -> str:
    """
    Get a record from the NMDC API by latitude and longitude comparison.
        params:
            lat_comparison: str
                The comparison to use to query the record for latitude. MUST BE ONE OF THE FOLLOWING:
                    eq    - Matches values that are equal to the given value.
                    gt    - Matches if values are greater than the given value.
                    lt    - Matches if values are less than the given value.
                    gte    - Matches if values are greater or equal to the given value.
                    lte - Matches if values are less or equal to the given value.
            long_comparison: str
                The comparison to use to query the record for longitude. MUST BE ONE OF THE FOLLOWING:
                    eq    - Matches values that are equal to the given value.
                    gt    - Matches if values are greater than the given value.
                    lt    - Matches if values are less than the given value.
                    gte    - Matches if values are greater or equal to the given value.
                    lte - Matches if values are less or equal to the given value.
            latitude: float
                The latitude of the record to query.
    """
    bs = biosample_search.BiosampleSearch()
    results = bs.get_record_by_lat_long(lat_comparison=lat_comparison, lon_comparison=lon_comparison, latitude=lat, longitude=long)
    return results

# here is what i have, imagine this, and how and who can we connect with to bring this more to life
# this tool has the capability to give semantic search, anbd we can use this to further api searches, as well as develop it to help users build api queries. 

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')


