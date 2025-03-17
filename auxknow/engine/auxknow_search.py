"""
AuxKnow Search: A simple Search Engine to enhance the capabilities of AuxKnow.

This module provides a Search Engine to help build custom search capabilities for AuxKnow.

Author: Aditya Patange (AdiPat)
Copyright (c) 2025 The Hackers Playbook
License: AGPLv3
"""

import traceback
from typing import Union
from langchain_community.tools import DuckDuckGoSearchResults
from ..common.models import AuxKnowSearchItem, AuxKnowSearchResults
from ..common.printer import Printer
from ..common.constants import Constants


class AuxKnowSearch:
    """
    AuxKnowSearch: A simple Search Engine to enhance the capabilities of AuxKnow.
    """

    def __init__(self, verbose=Constants.DEFAULT_VERBOSE_ENABLED):
        """
        Initializes the AuxKnow Search Engine.

        Args:
            verbose (bool, optional): Whether to print verbose messages. Defaults to DEFAULT_AUXKNOW_SEARCH_VERBOSE.
        """
        self.verbose = verbose
        Printer.verbose_logger(
            self.verbose,
            Printer.print_blue_message,
            Constants.SEARCH_ENGINE_INIT_MESSAGE,
        )
        self.search = DuckDuckGoSearchResults(
            output_format=Constants.SEARCH_ENGINE_OUTPUT_FORMAT
        )
        Printer.verbose_logger(
            self.verbose,
            Printer.print_green_message,
            Constants.SEARCH_ENGINE_INIT_SUCCESS,
        )

    def query(self, query: str) -> tuple[Union[AuxKnowSearchResults, None], str]:
        """
        Queries the AuxKnow Search Engine.

        Args:
            query (str): The query to search for.

        Returns:
            tuple[Union[AuxKnowSearchResults, None], str]: The search results and the error message.
        """
        try:
            Printer.verbose_logger(
                self.verbose,
                Printer.print_yellow_message,
                Constants.SEARCH_ENGINE_QUERY_MESSAGE(query),
            )
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
            Printer.verbose_logger(
                self.verbose,
                Printer.print_green_message,
                Constants.SEARCH_ENGINE_RESULTS_MESSAGE(len(results)),
            )
            return AuxKnowSearchResults(results=results), ""
        except Exception as e:
            error_msg = Constants.SEARCH_ENGINE_ERROR_MESSAGE(e)
            Printer.verbose_logger(self.verbose, Printer.print_red_message, error_msg)
            if self.verbose:
                traceback.print_exc()
            return None, str(e)
