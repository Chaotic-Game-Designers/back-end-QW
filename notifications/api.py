from django.http import HttpResponse
from .models import DeviceToken
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('./qw-test.json')
firebase_admin.initialize_app(cred)


def send_notification(request):
    #change query
    tokens = DeviceToken.objects.get(user__email='t@t.ir')

    # Create a notification message
    message = messaging.Message(
        notification=messaging.Notification(
            title="Your Notification Title",
            body="Your Notification Body"
        ),
        token=tokens.token
    )

    # Send the notification
    response = messaging.send(message)

    return HttpResponse("Notification sent successfully!")


