from langchain_community.tools import DuckDuckGoSearchResults
import traceback
from pydantic import BaseModel
from .printer import Printer
from typing import Union
from .constants import DEFAULT_AUXKNOW_SEARCH_VERBOSE


class AuxKnowSearchItem(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    title: str
    content: str
    url: str


class AuxKnowSearchResults(BaseModel):
    """
    AuxKnowSearchResults: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    results: list[AuxKnowSearchItem]


class CitationQueryGenerationResponse(BaseModel):
    """
    CitationQueryGenerationResponse: A simple Search Engine to enhance the capabilities of AuxKnow.
    """


class AuxKnowSearch:
    """
    AuxKnowSearch: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    def __init__(self, verbose=DEFAULT_AUXKNOW_SEARCH_VERBOSE):
        """
        Initializes the AuxKnow Search Engine.

        Args:
            verbose (bool, optional): Whether to print verbose messages. Defaults to DEFAULT_AUXKNOW_SEARCH_VERBOSE.
        """
        self.verbose = verbose
        if self.verbose:
            Printer.print_blue_message("🔦 Initializing the AuxKnow Search Engine...")
        self.search = DuckDuckGoSearchResults(output_format="list")
        if self.verbose:
            Printer.print_green_message("🔦 Initialized the AuxKnow Search Engine! 🚀")

    def query(self, query: str) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """
        Queries the AuxKnow Search Engine.

        Args:
            query (str): The query to search for.

        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: The search results and the error message.
        """
        try:
            results = self.search.invoke(query)
            results = []
            for result in results:
                results.append(
                    AuxKnowSearchItem(
                        title=result["title"],
                        content=result["snippet"],
                        url=result["url"],
                    )
                )
            return AuxKnowSearchResults(results=results), ""
        except Exception as e:
            if self.verbose:
                Printer.print_red_message(
                    f"Error while querying the AuxKnow Search Engine: {e}"
                )
                traceback.print_exc()
            return None, str(e)
