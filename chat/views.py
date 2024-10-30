from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from knowledge.rag_setup import UCExpertRAG
from symptoms.models import Symptom

class ChatView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/chat.html')
    
    def post(self, request):
        question = request.POST.get('question')
        
        # Get recent symptoms for context
        recent_symptoms = Symptom.objects.filter(
            patient=request.user
        ).order_by('-date')[:5]
        
        symptom_context = "\n".join([f"{s.date}: {s.description} ({s.location})" for s in recent_symptoms])
        
        # Initialize RAG
        rag = UCExpertRAG()
        response = rag.get_response(question, symptom_context)
        
        return JsonResponse({'response': response})