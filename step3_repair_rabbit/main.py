import pika
import random
import time
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='repair')


def callback(ch, method, properties, body):
    """
    Обработка чтения из очереди
    """
    phone = body
    # процесс ремонта
    repair_time = random.randint(3, 40)
    time.sleep(repair_time)
    # После окончания отправляется запрос на обновление статуса заказа
    requests.post('http://orders_flask:5000/change/',
                  data={'phone': phone, 'status': 'DONE'})


channel.basic_consume(queue='repair', on_message_callback=callback)

print('start')
channel.start_consuming()
