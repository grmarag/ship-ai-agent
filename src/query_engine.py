import logging
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryEngine:
    def __init__(self, vector_store, retriever, temperature: float = 0.0, top_k: int = 3):
        """
        Initializes the QueryEngine with a vector store, retriever, and conversation memory.
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=temperature,
            openai_api_key=Config.OPENAI_API_KEY,
            model='gpt-4-turbo-preview'
        )
        self.retriever = retriever
        self.top_k = top_k

        # Initialize conversation memory. Set return_messages=True so that the memory
        # keeps a list of message objects.
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Prompt template that includes PDF context and the conversation history.
        qa_prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=Config.PROMPT_TEMPLATE
        )

        # Conversational retrieval chain that uses our LLM, retriever, and memory.
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        logger.info("QueryEngine initialized.")

    def query(self, question: str) -> str:
        logger.info("Processing query: %s", question)
        chat_history_messages = self.memory.chat_memory.messages
        chat_history = "\n".join([msg.content for msg in chat_history_messages])
        
        result = self.qa_chain.invoke({
            "question": question,
            "chat_history": chat_history
        })
        logger.info("LLM response obtained.")
        return result['answer']