import africastalking

# Initialize Africa's Talking

africastalking.initialize(
    username='[sandbox]',
    api_key="[6000a4760274c433398eb2693f1430f834256f8c45c346c0ef1fadc782914633]"
)

class SendSMS:
    def sending(self):
        # Set the numbers in international format
        recipients = ["+254714205641"]
        # Set your message
        message = "Hey AT Ninja!"
        # Set your shortCode or senderId
        sender = "+25479669996"
        try:
            sms = africastalking.SMS
            print(sms)
            response = sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')

sms_instance = SendSMS()
sms_instance.sending()
