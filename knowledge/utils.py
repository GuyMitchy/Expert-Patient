from langchain.llms import Ollama

def test_ollama_connection():
    """Test if Ollama is running and responding"""
    try:
        llm = Ollama(model="mistral")
        response = llm.predict("What is Ulcerative Colitis?")
        return True, response
    except Exception as e:
        return False, str(e) 