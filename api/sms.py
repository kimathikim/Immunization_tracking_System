#!/usr/bin/env python3
import africastalking

# Initialize Africa's Talking

africastalking.initialize(
    username='ImmunSys',
    api_key="91a098b314aeda715976967be01d9127f00d619fedd515ijijijijijijijiji7385977c4ijijij185d4061e"
)

class SendSMS:
    def sending(self):
        recipients = ["+254796699969", "+254787353102"]
        message = "Hello mavin. Welcome to immunization tracking system.\nWe value the health of your Child!"
        sender = 796699969
        print(sender, recipients, message)
        try:
            sms = africastalking.SMS
            print(sms)
            response = sms.send(message, recipients,)
            print(response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')

sms_instance = SendSMS()
sms_instance.sending()
