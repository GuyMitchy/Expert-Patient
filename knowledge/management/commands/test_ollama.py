from django.core.management.base import BaseCommand
from knowledge.utils import test_ollama_connection

class Command(BaseCommand):
    help = 'Test Ollama connection and RAG setup'

    def handle(self, *args, **kwargs):
        success, response = test_ollama_connection()
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('Successfully connected to Ollama')
            )
            self.stdout.write(f"Test response: {response}")
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to connect to Ollama: {response}')
            ) 