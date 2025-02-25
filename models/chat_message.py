from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatMessage(Base):
    """Modelo para mensagens de chat (usuário e respostas do bot)"""
    __tablename__ = "messagensChat"

    id = Column(Integer, primary_key=True)
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatMessage(user_message='{self.user_message}', bot_response='{self.bot_response}')>"