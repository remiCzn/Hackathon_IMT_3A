# Server imports
import json
import time
import requests
from uuid import uuid4
from flask import Flask, jsonify, make_response, request
#Flask app
app = Flask(__name__)

# ------------------------------ ENV variables ------------------------------

#.env imports
from dotenv import load_dotenv
from pathlib import Path
import os

#Getting env variables
dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

#Assign env variables

PORT_CHAT = os.getenv('PORT_CHAT')
HOST = os.getenv('HOST')

# ------------------------------ MODELS ------------------------------

from models import Message, Chat

# ------------------------------ VARIABLES ------------------------------

PORT = PORT_CHAT

with open('{}/db/chat.json'.format("."), "r") as jsf:
   chat_dict = json.load(jsf)["chat"]
   chat:list[Chat] = Chat.schema().load(chat_dict, many=True) 


def generateId():
   return str(uuid4().int)

# ------------------------------ GET & SET FUNCTIONS ------------------------------

def getChatById(chatid):
   for c in chat :
      if c.uuid == chatid :
         return c
   return None

# ------------------------------ ERRORS FUNCTIONS ------------------------------
def notFound(name):
   return make_response(jsonify({'error': f'{name} not found'}),400)


# ------------------------------ ENDPOINTS ------------------------------
@app.route("/", methods=['GET'])
def home():
   return make_response(jsonify({'message':'chat service api root'}))

@app.route("/chats", methods=['GET'])
def get_chat():
   return make_response(Chat.schema().dumps(chat, many=True),200)

@app.route("/chats/<chatid>",methods=['GET'])
def get_chat_by_id(chatid):
   c = getChatById(chatid)
   if c : return make_response(c.to_json(),200)
   return notFound("chat")

@app.route("/chats/<chatid>/messages",methods=['POST'])
def send_message(chatid):
   body = request.json
   try :
      message = Message.from_dict(body)
   except :
      sample_request = Message("bob","sample text").to_dict()
      return make_response(jsonify({
         'error': "incorrect request",
         "sample-request-body":sample_request,
         "your-request-body": body
         }),400)

   c = getChatById(chatid)
   if not(c) : return notFound("chat")
   c.messages.append(message)
   return make_response(jsonify({'success': 'message sent',"message":message.to_dict()}),200)

@app.route("/chats",methods=['POST'])
def create_chat():
   try :
      body = request.json
   except :
      return make_response(jsonify({
         'error': "empty or incorrect body request"}),400)
   try :
      usernames = body["usernames"]
   except :
      sample_request = {"usernames":["caleb","bob"]}
      return make_response(jsonify({
         'error': "incorrect request",
         "sample-request-body":sample_request,
         "your-request-body": body
         }),400)

   new_chat = Chat(generateId(),usernames,messages=[])
   chat.append(new_chat)
   return make_response(jsonify({'success': 'chat added',"chat":new_chat.to_dict()}),200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
