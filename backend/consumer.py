import redis
import logging

# notifications.log
r = redis.Redis(host='localhost', port=6379, db=0)


def subscribe_notifications():
    logging.basicConfig(filename='notification.log', level=logging.INFO, 
                        format='%(asctime)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    pubsub = r.pubsub()
    pubsub.subscribe('notifications')
  
    for message in pubsub.listen():
        if message['type'] == 'message':
            notification = message['data'].decode('utf-8')
            print(f"Received notification: {notification}")
            logger.info(f"Received notification: {notification}")

if __name__ == '__main__':
    subscribe_notifications()

