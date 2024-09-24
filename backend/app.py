import redis
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# setup logging, notification.log
app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*")
# Adjust origins as needed
   
r = redis.Redis(host='localhost', port=6379, db=0)

redis_keys = ['chat-users', 'chat-messages', 'message-counter']

# Get all users in chat - Done
@app.route('/users', methods=['GET'])
def get_users():
    users = r.smembers('chat-users')
    users = [user.decode('utf-8') for user in users]
    return jsonify({"users": users})

# Add user into chat redis set - Done
@app.route('/join-chat/<string:nickname>', methods=['GET'])
def join_chat(nickname):
    if not nickname or len(nickname) > 20:
        return jsonify({"message": "Invalid nickname"})
    
    if r.sismember('chat-users', nickname):
        return jsonify({"message": f"{nickname} already in chat"})
    
    r.sadd('chat-users', nickname)
    return jsonify({"message": f"{nickname} joined the chat"})
    
# Send a message to chat - Done
@app.route('/send-message/<string:nickname>', methods=['POST'])
def send_message(nickname):
    
    print("A send message request is made")
    if not nickname or len(nickname) > 20:
        return jsonify({"message": "Invalid nickname"})
    
    # message from post
    message = request.json.get('message')

    if not message:
        return jsonify({"message": "Message cannot be empty"})
    
    if not r.sismember('chat-users', nickname):
        return jsonify({"message": f"{nickname} is not in chat"})

    next_id = r.incr('message-counter')
    
    message_data = {
        "id": next_id,
        "nickname": nickname,
        "message": message,
    }
        
    r.rpush('chat-messages', json.dumps(message_data))
    return jsonify({"message": "Message sent"})

# Get unread messages from the user - Done
@app.route('/get-messages/<string:nickname>', methods=['GET'])
def get_unread_messages(nickname):
    last_message_id = r.get(f'{nickname}-last-message-id')
    if not last_message_id:
        last_message_id = 0
    
    messages = r.lrange('chat-messages', last_message_id, -1)
    messages = [json.loads(message.decode('utf-8')) for message in messages]\
    
    if not messages:
        return jsonify([])
    
    last_message_id = messages[-1]['id']
    
    r.set(f'{nickname}-last-message-id', last_message_id)
    
    return jsonify(messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

