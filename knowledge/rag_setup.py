from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA

class UCExpertRAG:
    def __init__(self):
        # Initialize Ollama with the Mistral model
        self.llm = Ollama(model="mistral")
        self.embeddings = OllamaEmbeddings(model="mistral")
        self.vector_store = None
        self.qa_chain = None
        
    def initialize_knowledge_base(self):
        """Initialize the knowledge base with medical documents"""
        # Load medical documents from a directory
        loader = DirectoryLoader('knowledge/docs/', glob="*.md")
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # Create and persist the vector store
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory="knowledge/db"
        )
        
        # Initialize the QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
    
    def get_response(self, question: str, context: str = "") -> str:
        """Get a response from the RAG system"""
        if not self.qa_chain:
            self.initialize_knowledge_base()
        
        # Create a medical-focused prompt
        prompt = f"""
        Context: {context}
        Question: {question}
        
        Please provide accurate medical information based on the context and question.
        Focus on Ulcerative Colitis related information and always remind the user
        to consult healthcare professionals for medical advice.
        """
        
        try:
            return self.qa_chain.run(prompt)
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def get_medication_analysis(self, medications: list, symptoms: list) -> str:
        """Analyze medication effectiveness based on symptoms"""
        prompt = f"""
        Analyze these medications and symptoms:
        Medications: {medications}
        Recent Symptoms: {symptoms}
        
        Please provide:
        1. Potential correlations between medications and symptoms
        2. Suggestions for discussion with healthcare provider
        3. General observations about medication effectiveness
        """
        
        try:
            return self.llm.predict(prompt)
        except Exception as e:
            return f"Error analyzing medications: {str(e)}" 