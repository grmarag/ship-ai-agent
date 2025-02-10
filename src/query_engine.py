from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from src.config import Config
import os

class QueryEngine:
    def __init__(self, vector_store, retriever, temperature: float = 0.2, top_k: int = 3):
        """
        Initializes the QueryEngine with a vector store, retriever, and conversation memory.
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            temperature=temperature,
            openai_api_key=Config.OPENAI_API_KEY,
            model='gpt-4o-mini'
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

    def query(self, question: str) -> str:
        """
        Processes the user's question by:
          1. Extracting the current chat history from memory.
          2. Invoking the conversational chain with the question and formatted chat history.
          3. Optionally, appending source information if PDF-related documents are found.
        """
        # Extract the conversation messages (a list) from the memory and join their content.
        chat_history_messages = self.memory.chat_memory.messages
        chat_history = "\n".join([msg.content for msg in chat_history_messages])

        # Call the conversational retrieval chain with both the question and the chat history.
        result = self.qa_chain.invoke({
            "question": question,
            "chat_history": chat_history
        })

        # If the question seems to be PDF-related, fetch relevant sources.
        similarity_results = self.vector_store.db.similarity_search_with_relevance_scores(question, k=self.top_k)
        if similarity_results and similarity_results[0][1] > 0.8:
            sources = []
            for doc, score in similarity_results:
                full_source = doc.metadata.get("source", "Unknown PDF")
                source_name = os.path.basename(full_source)
                page = doc.metadata.get("page", "Unknown Page")
                sources.append(f"{source_name} (Page {page})")
            formatted_sources = "\n".join(f"- {source}" for source in sources)
            return f"{result['answer']}\n\nSources:\n{formatted_sources}"
        else:
            return result['answer']