import redis
from flask import Flask, jsonify, request
import json

# setup logging, notification.log
app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)


# Get all users in chat
@app.route('/users', methods=['GET'])
def get_users():
    users = r.smembers('chat-users')
    return jsonify({"users": [user.decode('utf-8') for user in users]})

# Add user into chat redis set
@app.route('/join-chat/<string:nickname>', methods=['GET'])
def join_chat(nickname):
    if not nickname or len(nickname) > 20:
        return jsonify({"message": "Invalid nickname"})
    
    if r.sismember('chat-users', nickname):
        return jsonify({"message": f"{nickname} already in chat"})
    
    r.sadd('chat-users', nickname)
    return jsonify({"message": f"{nickname} joined the chat"})
    
# Send a message to chat
@app.route('/send-message/<string:nickname>/', methods=['GET'])
def send_message(nickname):
    if not nickname or len(nickname) > 20:
        return jsonify({"message": "Invalid nickname"})
    
    message = request.args.get('message')
    if not message:
        return jsonify({"message": "Message cannot be empty"})
    
    if not r.sismember('chat-users', nickname):
        return jsonify({"message": f"{nickname} is not in chat"})
    
    message_data = {
        "nickname": nickname,
        "message": message,
    }
        
    r.rpush('chat-messages', jsonify(message_data))
    return jsonify({"message": "Message sent"})

# Get unread messages from the user
@app.route('/get-messages/<string:nickname>', methods=['GET'])
def get_unread_messages(nickname):
    messages = r.lrange('chat-messages', 0, -1)
    return jsonify({"messages": [json.loads(message.decode('utf-8')) for message in messages]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

