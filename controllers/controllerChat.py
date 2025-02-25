# controllers/chat_controller.py
# Nota: Este arquivo cuida das rotas da API. Gostei de usar blueprints porque organiza melhor as coisas do que ter tudo no app.py.
from flask import Blueprint, request, jsonify
from services.servicesChat import ChatService

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def handle_chat():
    """Recebe uma mensagem do usuário, gera uma resposta e salva no banco. Decisão: Retorno um JSON simples para manter compatibilidade com o frontend."""
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem enviada'}), 400

    # Gerar resposta do bot
    bot_response = ChatService.generate_response(user_message)
    
    # Salvar mensagem e resposta
    ChatService.save_message(user_message, bot_response)
    
    return jsonify({'response': bot_response})

@chat_bp.route('/messages', methods=['GET'])
def get_all_messages():
    """Recupera todas as mensagens salvas. Nota: Testei isso e funciona bem para mostrar o histórico no frontend."""
    messages = ChatService.get_messages()
    return jsonify([{
        'id': msg.id,
        'user_message': msg.user_message,
        'bot_response': msg.bot_response,
        'created_at': msg.created_at.isoformat()
    } for msg in messages])

@chat_bp.route('/message/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    """Atualiza a resposta de uma mensagem específica. Decisão: Só permito atualização se houver uma resposta nova, pra evitar erros."""
    data = request.json
    bot_response = data.get('bot_response')
    if not bot_response:
        return jsonify({'error': 'Resposta não fornecida'}), 400
    
    ChatService.update_message(message_id, bot_response)
    return jsonify({'message': 'Mensagem atualizada com sucesso'})

@chat_bp.route('/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Remove uma mensagem específica. Nota: Adicionei isso mais por segurança, caso eu precise limpar dados antigos."""
    ChatService.delete_message(message_id)
    return jsonify({'message': 'Mensagem removida com sucesso'})