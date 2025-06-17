import firebase_admin
from firebase_admin import messaging

# Initialize Firebase App if not already done
if not firebase_admin._apps:
    firebase_admin.initialize_app()

def send_push_notification(firebase_token, message):
    try:
        message_obj = messaging.Message(
            notification=messaging.Notification(
                title='Shared Expenses App',
                body=message
            ),
            token=firebase_token
        )
        response = messaging.send(message_obj)
        print(f'Notification sent: {response}')
    except Exception as e:
        print(f'Error sending notification: {str(e)}')
