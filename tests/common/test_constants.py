from auxknow.common.constants import Constants, AUXKNOW_INTELLIGENCE_CONSTANT, SupportedAIModel


def test_constants_initialization():
    assert Constants is not None
    assert AUXKNOW_INTELLIGENCE_CONSTANT == 4


def test_api_constants():
    assert Constants.PERPLEXITY_BASE_URL == "https://api.perplexity.ai"
    assert Constants.PERPLEXITY_API_BASE_URL == "https://api.perplexity.ai"
    assert Constants.ENV_PERPLEXITY_API_KEY == "PERPLEXITY_API_KEY"
    assert Constants.ENV_OPENAI_API_KEY == "OPENAI_API_KEY"
    assert Constants.ENV_FILE == ".env"


def test_error_constants():
    assert (
        Constants.ERROR_DEFAULT
        == "Sorry, AuxKnow can't provide an answer right now. Please try again later!"
    )
    assert Constants.ERROR_CITATIONS("test") == "Error while getting citations: test"
    assert (
        Constants.ERROR_CLEAN_ANSWER("test")
        == "Error while cleaning answer, returning original answer as it is: test"
    )
    assert Constants.ERROR_ASK_QUESTION("test") == "Error while asking question: test."
    assert (
        Constants.ERROR_INVALID_MODEL("model1", "model2")
        == "Invalid model name 'model1' received from model router. Defaulting to 'model2'."
    )
    assert (
        Constants.ERROR_CLOSED_SESSION == "Cannot ask a question on a closed session."
    )


def test_feature_constants():
    assert isinstance(Constants.DEFAULT_AUTO_MODEL_ROUTING_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_AUTO_PROMPT_AUGMENT, bool)
    assert isinstance(Constants.DEFAULT_ENABLE_UNBIASED_REASONING, bool)
    assert isinstance(Constants.DEFAULT_DEEP_RESEARCH_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_FAST_MODE_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_SEARCH_VERBOSE, bool)


def test_format_constants():
    assert Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS == 3
    assert Constants.DEFAULT_LINES_PER_PARAGRAPH == 5
    assert Constants.MAX_ANSWER_LENGTH_PARAGRAPHS == 8
    assert Constants.MAX_LINES_PER_PARAGRAPH == 10
    assert (
        Constants.DEFAULT_ANSWER_LENGTH_PARAGRAPHS
        < Constants.MAX_ANSWER_LENGTH_PARAGRAPHS
    )
    assert Constants.DEFAULT_LINES_PER_PARAGRAPH < Constants.MAX_LINES_PER_PARAGRAPH


def test_key_constants():
    assert Constants.KEY_ROLE == "role"
    assert Constants.KEY_CONTENT == "content"
    assert Constants.KEY_CHOICES == "choices"
    assert Constants.KEY_MESSAGE == "message"
    assert Constants.KEY_CITATIONS == "citations"


def test_memory_constants():
    assert Constants.EMPTY_CONTEXT == ""
    assert Constants.MAX_CONTEXT_TOKENS == 4096
    assert Constants.MAX_RECENT_CONTEXT_PAIRS == 10
    assert Constants.OPTIMIZATION_CONSTANT == 4
    assert isinstance(Constants.PROMPT_AUGMENTATION_FACTOR, float)

    # Test memory packet template
    memory_packet = Constants.MEMORY_PACKET_TEMPLATE(
        "123", "question", "answer", "citations"
    )
    assert "Memory Packet ID: 123" in memory_packet
    assert "Question: question" in memory_packet
    assert "Answer: answer" in memory_packet
    assert "Citations: citations" in memory_packet


def test_model_constants():
    assert Constants.MODEL_SONAR == "sonar"
    assert Constants.MODEL_SONAR_PRO == "sonar-pro"
    assert Constants.MODEL_R1_1776 == "r1-1776"
    assert Constants.MODEL_GPT4O_MINI == "gpt-4o-mini"
    assert Constants.MODEL_SONAR_DEEP_RESEARCH == "sonar-deep-research"

    # Test default models dictionary
    assert "standard" in Constants.DEFAULT_MODELS
    assert "perplexity" in Constants.DEFAULT_MODELS
    assert "deep_research" in Constants.DEFAULT_MODELS
    assert "prompt_augmentation" in Constants.DEFAULT_MODELS
    assert "fast_mode" in Constants.DEFAULT_MODELS


def test_path_constants():
    assert Constants.CWD_PATH == "."
    assert Constants.FILE_ENV == ".env"
    assert Constants.FILE_ENV_TEST == ".env.test"
    assert Constants.FILE_CWD == "."


def test_think_block_constants():
    assert Constants.THINK_BLOCK_START == "<think>"
    assert Constants.THINK_BLOCK_END == "</think>"
    assert Constants.THINK_BLOCK_END_LENGTH == 8
    assert Constants.THINK_BLOCK_PATTERN == r"<think>.*?</think>"
    assert Constants.MULTIPLE_NEWLINES_PATTERN == r"\n{3,}"
    assert Constants.NEWLINE_REPLACEMENT == "\n\n"


def test_prompt_templates():
    # Test citation query prompt
    citation_prompt = Constants.PROMPT_CITATION_QUERY("test query", "test response")
    assert "test query" in citation_prompt
    assert "test response" in citation_prompt

    # Test query restructure prompt
    restructure_prompt = Constants.PROMPT_QUERY_RESTRUCTURE("test query")
    assert "test query" in restructure_prompt

    # Test user ask prompt with various combinations
    user_ask_normal = Constants.PROMPT_USER_ASK("test", 3, 5, False, "")
    assert "test" in user_ask_normal
    assert "3 paragraphs" in user_ask_normal
    assert "5 lines" in user_ask_normal

    user_ask_deep = Constants.PROMPT_USER_ASK("test", 3, 5, True, "context")
    assert "deep research" in user_ask_deep
    assert "Context: context" in user_ask_deep

    # Add tests for the missing prompt templates
    model_router_prompt = Constants.DEFAULT_AUXKNOW_MODEL_ROUTER_USER_PROMPT(
        "test query", [SupportedAIModel(model="model1", description="test description"), SupportedAIModel(model="model2", description="test description 2")], True
    )
    assert "test query" in model_router_prompt
    assert "model1" in model_router_prompt
    assert "model2" in model_router_prompt

    augment_prompt = Constants.PROMPT_AUGMENT_USER_TEMPLATE(
        "test question", "test context"
    )
    assert "test question" in augment_prompt
    assert "test context" in augment_prompt

    combined_prompt = Constants.PROMPT_AUGMENT_COMBINED("user prompt", "augment")
    assert "user prompt" in combined_prompt
    assert "augment" in combined_prompt


def test_performance_constants():
    perf_log = Constants.PERFORMANCE_LOG_MESSAGE("test_func", 1.23, "s")
    assert "test_func" in perf_log
    assert "1.23s" in perf_log


def test_stream_processing_constants():
    assert Constants.STREAM_BLOCK_START == "<think>"
    assert Constants.STREAM_BLOCK_END == "</think>"
    assert Constants.STREAM_DEFAULT_BUFFER_CONTENT == ""
    assert isinstance(Constants.STREAM_DEFAULT_IS_IN_THINK_BLOCK, bool)
    assert Constants.STREAM_DEFAULT_FULL_ANSWER == ""
    assert isinstance(Constants.STREAM_DEFAULT_CITATIONS, list)
    assert len(Constants.STREAM_DEFAULT_CITATIONS) == 0


def test_callable_error_messages():
    # Test various error message templates with different argument types
    assert isinstance(Constants.ERROR_CITATIONS("test"), str)
    assert isinstance(Constants.ERROR_CLEAN_ANSWER(Exception("test")), str)
    assert isinstance(Constants.ERROR_ASK_QUESTION(ValueError("test")), str)
    assert isinstance(Constants.ERROR_INVALID_MODEL("model1", "model2"), str)
    assert isinstance(Constants.ERROR_ROUTING(Exception("test")), str)


def test_message_templates():
    # Test various message templates
    assert isinstance(Constants.MESSAGE_ENV_LOADING_PATH_TEMPLATE("/path"), str)
    assert isinstance(Constants.MESSAGE_LLM_INIT_SUCCESS("Test"), str)
    assert isinstance(Constants.MESSAGE_AUTO_MODEL_ROUTING_ENABLED(True), str)
    assert isinstance(Constants.MESSAGE_PERFORMANCE_LOGGING(False), str)
    assert isinstance(Constants.MESSAGE_API_KEY_NOT_FOUND("key"), str)


def test_config_error_messages():
    # Test configuration error messages
    length_error = Constants.CONFIG_ERROR_ANSWER_LENGTH(10, 5)
    assert "10" in length_error
    assert "5" in length_error

    lines_error = Constants.CONFIG_ERROR_LINES_PER_PARAGRAPH(10, 5)
    assert "10" in lines_error
    assert "5" in lines_error


def test_additional_feature_constants():
    assert isinstance(Constants.DEFAULT_ANSWER_MODE_FOR_CITATIONS_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_PERFORMANCE_LOGGING_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_TEST_MODE_ENABLED, bool)


def test_library_constants():
    assert isinstance(Constants.ARBITRARY_TYPES_ALLOWED, bool)
    assert isinstance(Constants.DEFAULT_AUTO_MODEL_ROUTING_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_AUTO_QUERY_RESTRUCTURING_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_VERBOSE_ENABLED, bool)
    assert isinstance(Constants.DEFAULT_EXIT_ON_LLM_INIT_FAILURE, bool)
    assert isinstance(Constants.DEFAULT_EXIT_ON_LLM_API_KEY_FAILURE, bool)
    assert isinstance(Constants.DEFAULT_OVERRIDE_CONTEXT, bool)
    assert isinstance(Constants.DEFAULT_PREFER_EXISTING_CONTEXT, bool)
    assert isinstance(Constants.DEFAULT_GET_CONTEXT_PREFERENCE, bool)
    assert isinstance(Constants.DEFAULT_EXISTING_CONTEXT_PREFERENCE, bool)
    assert Constants.ROLE_SYSTEM == "system"
    assert Constants.ROLE_USER == "user"
    assert isinstance(Constants.DEFAULT_PROMPT_AUGMENTATION_TEMPERATURE, float)
    assert isinstance(Constants.INITIAL_ANSWER_IS_FINAL_ENABLED, bool)


def test_additional_memory_constants():
    assert isinstance(Constants.DEFAULT_SESSION_CLOSED_STATUS, bool)
    assert Constants.DEFAULT_MEMORY_RETRIEVAL_COUNT == 5


def test_memory_module_messages():
    assert "Session ID" in Constants.MEMORY_MODULE_INIT_MESSAGE
    assert "Session ID" in Constants.MEMORY_MODULE_INIT_SUCCESS
    assert "tokens" in Constants.MEMORY_UPDATE_SUCCESS
    assert "tokens" in Constants.MEMORY_UPDATE_ERROR
    assert "Looking up memory" in Constants.MEMORY_LOOKUP_START
    assert "Error looking up memory" in Constants.MEMORY_LOOKUP_ERROR
    assert "OpenAI API key" in Constants.MEMORY_API_KEY_ERROR
    assert "OpenAI API key" in Constants.MEMORY_API_KEY_EXCEPTION


def test_additional_error_messages():
    assert "ping test failed" in Constants.ERROR_PING_TEST_FAILED("Test", "error")
    assert "ping test failed" in Constants.ERROR_PING_TEST_FAILED_WITH_EXCEPTION(
        "Test", "error"
    )
    assert "Error while augmenting prompt" in Constants.ERROR_AUGMENT_PROMPT("error")
    assert (
        "Error while getting prompt augmentation segment"
        in Constants.ERROR_PROMPT_SEGMENT("error")
    )


def test_message_constants():
    assert Constants.DEFAULT_AUXKNOW_SYSTEM_PROMPT.startswith("\n    You are AuxKnow")
    assert "Model Router" in Constants.AUXKNOW_MODEL_ROUTER_CUSTOM_INSTRUCTION
    assert Constants.MESSAGE_INIT == "🧠 Initializing AuxKnow API! 🤯"
    assert "AuxKnow API not initialized" in Constants.MESSAGE_API_NOT_INITIALIZED
    assert Constants.MESSAGE_NO_CITATIONS == "No citations available."
    assert (
        Constants.MESSAGE_EMPTY_ANSWER
        == "Sorry, no answer found for the given question."
    )


def test_ping_test_constants():
    assert (
        Constants.PING_TEST_SYSTEM_PROMPT
        == "You are a test system. Respond with 'pong' to verify connectivity."
    )
    assert Constants.PING_TEST_USER_PROMPT == "ping"
    assert Constants.PING_TEST_MAX_TOKENS == 10
    assert Constants.PING_TEST_SEARCH == "pong"
    assert "Ping Test Response" in Constants.PING_TEST_RESPONSE("test", "response")


def test_search_engine_constants():
    assert (
        Constants.SEARCH_ENGINE_INIT_MESSAGE
        == "🔦 Initializing the AuxKnow Search Engine..."
    )
    assert (
        Constants.SEARCH_ENGINE_INIT_SUCCESS
        == "🔦 Initialized the AuxKnow Search Engine! 🚀"
    )
    assert "Searching for" in Constants.SEARCH_ENGINE_QUERY_MESSAGE("test")
    assert "Found" in Constants.SEARCH_ENGINE_RESULTS_MESSAGE(5)
    assert "Error while querying" in Constants.SEARCH_ENGINE_ERROR_MESSAGE("error")
    assert Constants.SEARCH_ENGINE_OUTPUT_FORMAT == "list"


def test_stream_processor_constants():
    assert isinstance(Constants.STREAM_PROCESSOR_ERROR_MSG(Exception("test")), str)
    assert (
        Constants.STREAM_PROCESSOR_MODULE_DOC
        == "Stream processor module for handling streaming responses from the API."
    )
    assert Constants.STREAM_BUFFER_CLASS_DOC == "Container for stream processing state."
    assert (
        Constants.STREAM_PROCESSOR_CLASS_DOC
        == "Handles processing of streamed response chunks."
    )


def test_additional_message_constants():
    # Test initialization messages
    assert Constants.MESSAGE_ENV_LOADING == "🔄 Loading environment variables..."
    assert (
        Constants.MESSAGE_ENV_LOADED == "✅ Environment variables loaded successfully!"
    )
    assert (
        Constants.MESSAGE_ENV_NOT_LOADED == "❌ Failed to load environment variables."
    )
    assert (
        Constants.MESSAGE_MEMORY_NOT_INITIALIZED
        == "AuxKnow Memory not initialized. Cannot load context."
    )
    assert Constants.MESSAGE_AUXKNOW_PING_TEST == "🚀 AuxKnow ping test passed."
    assert (
        Constants.MESSAGE_AUXKNOW_INITIALIZED
        == "🚀 AuxKnow API initialized successfully!"
    )
    assert Constants.MESSAGE_VERBOSE_ON == "🗣️  Verbose: ON."
    assert (
        Constants.MESSAGE_FAST_MODE_OVERRIDE
        == "Fast mode and deep research / reasoning mode cannot be enabled at the same time. Defaulting to fast mode."
    )
    assert (
        Constants.LOG_CONTEXT_OVERRIDE
        == "Context and get context callback both provided, overriding context with new context."
    )
    assert (
        Constants.LOG_CONTEXT_EXISTING
        == "Context and get context callback both provided but prefer_existing_context flag set to true, defaulting to existing context."
    )
    assert (
        Constants.LOG_CITATIONS_MODE
        == " Running for_citations (citations-specific) mode."
    )
    assert (
        Constants.MESSAGE_LLM_INIT_FAIL("test")
        == "🌴 Failed to initialize test API. Please check your API key and try again."
    )
    assert (
        Constants.MESSAGE_MEMORY_ERROR("test")
        == "Error loading context from AuxKnow Memory for question['test']. Cannot load context."
    )
    assert (
        Constants.MESSAGE_MEMORY_UPDATE_ERROR("test")
        == "Error updating context in AuxKnow Memory for question['test']. Cannot update context."
    )
    assert (
        Constants.MESSAGE_AUTO_MODEL_ROUTING_OVERRIDE("test")
        == "test and auto model routing are both enabled at the same time. Overriding to test."
    )
    assert Constants.MESSAGE_LOG_AUGMENTED_PROMPT("test") == "Augmented prompt: 'test' "
    assert (
        Constants.MESSAGE_LOG_RESTRUCTURED_PROMPT("test")
        == "Restructured prompt: 'test' "
    )
    assert (
        Constants.MESSAGE_ASK_QUESTION_LOG_TEMPLATE("q", "m")
        == "🧠 Asking question: 'q' with model: 'm'."
    )
    assert (
        Constants.MESSAGE_ASK_QUESTION_CITATIONS_MODE_LOG("q", "m")
        == "🧠 Asking question: 'q' with model: 'm' for citations."
    )
    assert (
        Constants.MESSAGE_UNINITIALIZED_ANSWER
        == "AuxKnow API not initialized. Cannot ask questions."
    )
    assert (
        Constants.MESSAGE_API_KEY_DEPRECATED
        == "The 'api_key' parameter is deprecated. Use 'perplexity_api_key' instead."
    )
    assert Constants.MESSAGE_TEST_MODE_ENABLED(True) == "🧪 Test Mode enabled!"
    assert Constants.MESSAGE_TEST_MODE_ENABLED(False) == "🧪 Test Mode disabled."


def test_templates():
    assert Constants.MESSAGES_TEMPLATE("role", "content") == {
        "role": "role",
        "content": "content",
    }
    assert (
        Constants.CONTENT_QUERY_RESTRUCTURER
        == "\nIn this instance, you will be acting as a 'Query Restructurer' to fine-tune the query for better results."
    )


def test_model_router_system_prompt():
    assert (
        Constants.MODEL_ROUTER_SYSTEM_PROMPT
        == "You are a model selection expert. Your task is to analyze queries and select the most appropriate model. Respond only with the model name, no additional text."
    )


def test_citations_error_log_template():
    assert (
        Constants.CITATIONS_ERROR_LOG_TEMPLATE("test")
        == "Error while getting citations: test"
    )


def test_memory_update_error_template():
    assert Constants.MEMORY_UPDATE_ERROR_TEMPLATE == "Error updating memory: {}."
    assert Constants.MEMORY_LOOKUP_ERROR_TEMPLATE == "Error looking up memory: {}."
