
from typing import List, Dict
import ollama

import os

from langchain.prompts import ChatPromptTemplate

class UCExpertRAG:
    def __init__(self):
        self.model = "mistral"
        self.docs_path = os.path.join('knowledge', 'docs')
        
        # Define the prompt template
        template = """
        You are a medical assistant for patients with ulcerative colitis. Answer the question based on the context below. Keep responses very brief (2-3 sentences).
        If you can't answer the question, reply "I don't know".

        Context: {context}
        User Information: {user_info}
        Question: {question}

        Guidelines:
        1. Be clear and direct
        2. Never provide medical advice
        3. Focus on factual information
        
        """
        self.prompt = ChatPromptTemplate.from_template(template)

    def get_response(self, question: str, user_info: str) -> str:
        try:
            # Read knowledge base files
            knowledge_base = ""
            for filename in os.listdir(self.docs_path):
                if filename.endswith('.md'):
                    with open(os.path.join(self.docs_path, filename), 'r') as f:
                        knowledge_base += f.read() + "\n\n"

            # Format the prompt using the template
            formatted_prompt = self.prompt.format(
                context=knowledge_base,
                user_info=user_info,
                question=question
            )

            # Create the chain: prompt -> model
            response = ollama.chat(model=self.model, messages=[{
                'role': 'user',
                'content': formatted_prompt
            }])

            # Clean and return the response
            return ' '.join(response['message']['content'].split())

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return "I apologize, but I'm having trouble accessing my knowledge base. Please try again in a moment."