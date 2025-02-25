# Este arquivo cuida da lógica principal do chatbot. Escolhi o DialoGPT-medium porque é bom o suficiente para conversas simples, teste
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from models.chat_message import ChatMessage, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

# Configurar conexão com o banco de dados
# Usei SQLite porque é fácil para protótipos e não preciso de um servidor de banco de dados separado no momento.
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

class ChatService:
    """Gerencia a lógica do chatbot, incluindo IA e CRUD"""

    @staticmethod
    def generate_response(user_input):
        """Gera uma resposta usando o modelo DialoGPT. Nota: Testei isso localmente e as respostas estão legais para um protótipo."""
        input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

    @staticmethod
    def save_message(user_message, bot_response=None):
        """Salva uma mensagem e resposta no banco de dados. Nota: Coloquei um try/finally para garantir que a sessão feche, mesmo se der erro."""
        session = Session()
        try:
            message = ChatMessage(user_message=user_message, bot_response=bot_response)
            session.add(message)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def get_messages():
        """Recupera todas as mensagens do banco de dados. Decisão: Ordenei por data para mostrar as mensagens em sequência cronológica."""
        session = Session()
        try:
            messages = session.query(ChatMessage).order_by(ChatMessage.created_at).all()
            return messages
        finally:
            session.close()

    @staticmethod
    def update_message(message_id, bot_response):
        """Atualiza a resposta de uma mensagem existente. Nota: Isso pode ser útil se eu quiser corrigir respostas do bot mais tarde."""
        session = Session()
        try:
            message = session.query(ChatMessage).filter_by(id=message_id).first()
            if message:
                message.bot_response = bot_response
                session.commit()
        finally:
            session.close()

    @staticmethod
    def delete_message(message_id):
        """Remove uma mensagem do banco de dados. Decisão: Adicionei isso para caso eu queira limpar conversas antigas."""
        session = Session()
        try:
            message = session.query(ChatMessage).filter_by(id=message_id).first()
            if message:
                session.delete(message)
                session.commit()
        finally:
            session.close()