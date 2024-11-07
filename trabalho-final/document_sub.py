#!/usr/bin/env python
import pika
import sys
import os
import time
import json
from fpdf import FPDF


def pdf_process_function(msg):
    print(" PDF processing")
    print(" [x] Received " + str(msg))
    print(msg)
    data = msg.decode('utf-8')
    print(data)

    # Convertendo os dados em informação
    json_data = json.loads(data)
    print("ID --------> {0}".format(json_data['id']))
    print("Nome ------> {0}".format(json_data['nome']))
    print("Endereço --> {0}".format(json_data['endereco']))

    # Criando o arquivo pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(
        200, 10, txt="ID --------> {0}".format(json_data['id']), ln=1, align="C")
    pdf.cell(
        200, 20, txt="Nome ------> {0}".format(json_data['nome']), ln=2, align="C")
    pdf.cell(
        200, 30, txt="Endereço --> {0}".format(json_data['endereco']), ln=3, align="C")
    pdf.output("/home/marciocunha/ufu-pratica/asa/aula_mensageria/amqp/teste.pdf")

    #time.sleep(5)  # delays for 5 seconds
    print(" PDF processing finished")
    return


def main():
    #connection = pika.BlockingConnection(
    #    pika.ConnectionParameters(host='localhost'))
    #channel = connection.channel()
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='pdfprocess')

    def callback(ch, method, properties, body):
        pdf_process_function(body)

    channel.basic_consume(queue='pdfprocess',
                          on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)