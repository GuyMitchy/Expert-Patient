from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Conversation, Message
from knowledge.rag_setup import UCExpertRAG

# Initialize RAG system
rag_system = UCExpertRAG()

class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'chat/list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

class ConversationCreateView(LoginRequiredMixin, CreateView):
    model = Conversation
    template_name = 'chat/new.html'
    fields = []  # No fields needed as we'll just create an empty conversation

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.title = "New Conversation"  # Default title
        response = super().form_valid(form)
        
        # Add initial bot message
        Message.objects.create(
            conversation=self.object,
            content=(
                "Hello! I'm your UC Expert assistant. While I can provide information "
                "about Ulcerative Colitis, please remember that I'm not a substitute "
                "for professional medical advice. How can I help you today?"
            ),
            is_bot=True
        )
        
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'chat/detail.html'
    context_object_name = 'conversation'

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.message_set.all()
        return context

@login_required
def send_message(request, conversation_id):
    if request.method != 'POST':
        return HttpResponse('Method not allowed', status=405)

    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    user_message = request.POST.get('message', '').strip()

    if not user_message:
        return HttpResponse('Message is required', status=400)

    # Save user message
    Message.objects.create(
        conversation=conversation,
        content=user_message,
        is_bot=False
    )

    try:
        # Initialize user context
        user_context = "User Context:\n"
        
        # Try to get symptoms if they exist
        try:
            recent_symptoms = request.user.symptom_set.all()[:5]
            if recent_symptoms:
                user_context += "\nRecent Symptoms:\n"
                for symptom in recent_symptoms:
                    user_context += f"- {symptom.description} (Severity: {symptom.severity})\n"
        except AttributeError:
            user_context += "\nNo symptoms recorded.\n"

        # Try to get medications if they exist
        try:
            if hasattr(request.user, 'current_medications'):
                user_context += f"\nCurrent Medications:\n{request.user.current_medications}\n"
        except AttributeError:
            user_context += "\nNo medications recorded.\n"

        # Get response using RAG system
        response = rag_system.get_response(
            question=user_message,
            user_info=user_context
        )

        # Clean up the response
        cleaned_response = ' '.join(response.split())

        # Save bot message
        bot_message = Message.objects.create(
            conversation=conversation,
            content=cleaned_response,
            is_bot=True
        )

        # Return just the rendered HTML
        return render(request, 'chat/message.html', {'message': bot_message})

    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)