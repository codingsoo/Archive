# Virtual Girlfriend Chatbot

It is a web app which allows you talk to your imaginary girlfriend. There are 2 types of girlfriends - friendly and softy concepts. The bot can read documents and act like a human being through machine learning.

## News

We've got 3rd prize in OpenHack Korea 2017 (https://sigoss.github.io/hackathon2017/index.html)!

## Dependencies

- Python2
- Tensorflow
- Flask

## Getting Started

### Friendly Concept

```
cd virtual-girlfriend/chatbot   
python server.py
```

You can test it through http://0.0.0.0:5230 .

### Softy Concept

Chage chat_chun.log and chat_chun.voc files to chat.log and chat.voc files. Then, you can run with the same way as friendly concept.

## Add new model

```
cd virtual-girlfriend/chatbot
python dialog.py --voc_build
python train.py --train
```

Warning : chat.voc file should be exactly 164 lines.

## Team

- Machine Learning: Myeongsoo Kim
- Web: Seojin Park
- Planner: Joonsoo Lee
- Dataset: Hyung Geun Jung and Yi Jung Kim
