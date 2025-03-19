from openai import OpenAI
from .printer import Printer
from .constants import Constants


class LLMFactory:
    """
    Factory class for creating LLM client instances.
    """

    @staticmethod
    def get_openai_client(
        api_key: str, base_url=None, verbose=Constants.DEFAULT_VERBOSE_ENABLED
    ) -> OpenAI:
        """Get OpenAI client instance.

        Args:
            api_key (str): OpenAI API key

        Returns:
            OpenAI: OpenAI client instance
        """
        try:
            if base_url:
                return OpenAI(api_key=api_key, base_url=base_url)
            return OpenAI(api_key=api_key)
        except Exception as e:
            Printer.verbose_logger(
                verbose,
                Printer.print_red_message,
                f"Failed to create OpenAI client instance: {e}",
            )
            return None
