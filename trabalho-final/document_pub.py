#!/usr/bin/env python
import pika
import json
import time


#connection = pika.BlockingConnection(
#    pika.ConnectionParameters(host='localhost', port=5671))
#channel = connection.channel()
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# data = {"id": 1, "nome": "Pedro Silva", "endereco": "Rua X, 333"}
# print(json.dumps(data).encode())
# print(json.dumps(data))

channel.queue_declare(queue='pdfprocess')

#channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
i = 1
while(True):
    data = {"id": i, "nome": "Pedro Silva", "endereco": "Rua X, 333"}
    print(json.dumps(data).encode())
    print(json.dumps(data))
    channel.basic_publish(exchange='', routing_key='pdfprocess',
                      body=json.dumps(data).encode())
    print("[x] Message sent to consumer")
    time.sleep(5)  # delays for 5 seconds
    i = i + 1

connection.close()