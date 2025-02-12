from flask import Flask, request
import sqlite3
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Database setup
def setup_database():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Get customer name by phone
def get_customer_name(phone):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM customers WHERE phone = ?", (phone,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Save customer to database
def save_customer(phone, name):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO customers (phone, name) VALUES (?, ?)", (phone, name))
    conn.commit()
    conn.close()

# Template message sender
def send_template_message(to_number, template_ssid, content_variables):
    from twilio.rest import Client

    account_sid = "Please enter you sid here"
    auth_token = "Please enter your auth token here"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        content_sid=template_ssid,
        content_variables=content_variables,
        to=f'whatsapp:{to_number}'
    )
    print("Message sent with SID:", message.sid)

# State tracking (for simplicity)
user_states = {}



@app.route('/webhook', methods=['POST'])
def webhook():
    
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').replace('whatsapp:', '')

    # Check if customer exists
    customer_name = get_customer_name(from_number)

    # Check state for the user
    #state = user_states.get(from_number, 'start')
    
     # Check state for the user
    state_info = user_states.get(from_number, {'state': 'start'})  # Default to start state if not set
    state = state_info['state']

    
    
    # Handle new customer
    if state == 'start':
        
        if customer_name:
            # Known customer        
            response = MessagingResponse()
            response.message(f"Hi {customer_name}")
            # Send brand image
            send_template_message(
                to_number=from_number,
                template_ssid='HX17c635d6563b33e0031ddd6e94103c99',
                content_variables='{}'
            )
            # Send thank-you message
            send_template_message(
                to_number=from_number,
                template_ssid='HX761c1ee805f6eeec120a744e89a1fd69',
                content_variables='{}'
            )
            #user_states[from_number] = 'response 1'
            user_states[from_number] = {'state': 'response 1'}
            return str(response)
        else:
            # Send greeting and ask for name
            send_template_message(
                to_number=from_number,
                template_ssid='HX9dee2d0d2cd34989a9c966a67da560b3',
                content_variables='{}'
            )
            user_states[from_number] = {'state': 'awaiting_name'}
            #user_states[from_number] = 'awaiting_name'
            response = MessagingResponse()
            response.message("")
            return str(response)


    elif state == 'awaiting_name':
        # Capture name and ask for confirmation
        user_states[from_number] = {'state': 'confirming_name'}
        #user_states[from_number] = 'confirming_name'
        user_states[f"{from_number}_name"] = incoming_msg
        response = MessagingResponse()
        response.message(f"Got it! Is your name '{incoming_msg}'")
        # Send Yes/No button
        send_template_message(
            to_number=from_number,
            template_ssid='HXaebfd939caf2b4e8e7d5be31887b735b',
            content_variables='{}'
        )
        return str(response)
    


    elif state == 'confirming_name':
        
        if incoming_msg.lower() == 'yes':
            # Save name in the database
            name = user_states.pop(f"{from_number}_name", 'Guest')
            save_customer(from_number, name)
            user_states[from_number] = {'state': 'response 1'}
            #user_states[from_number] = 'response 1'
            send_template_message(
            to_number=from_number,
            template_ssid='HX761c1ee805f6eeec120a744e89a1fd69',
            content_variables='{}'
            )
            response = MessagingResponse()
            response.message(f"Thank you, {name}! You are now registered with us. How can we help you today?")
            return str(response)
        
        elif incoming_msg.lower() == 'no':
            # Ask for the correct name
            #user_states[from_number] = 'awaiting_name'
            user_states[from_number] = {'state': 'awaiting_name'}
            response = MessagingResponse()
            response.message("Oh, please share your name again.")
            return str(response)
        
        else:
            # Invalid response
            response = MessagingResponse()
            response.message("Please reply with 'yes' or 'no' to confirm your name.")
            return str(response)
    
    
    
    elif state == 'response 1':
        
        if incoming_msg.lower() == 'about us':
            response = MessagingResponse()
            response.message("💇‍♂️\n\nWelcome to *[Your Salon Name]*! We’re your go-to destination for beauty and relaxation. Our professional team offers a variety of services, including hair styling, skin treatments, manicures, pedicures, and much more.✨\n\nWe pride ourselves on exceptional service and making every visit a luxurious experience. 💖\n\nLet us know how we can assist you today!")
            # Send options (services/book)
            send_template_message(
                to_number=from_number,
                template_ssid='HXe5d68dfc9de1bd47de7cf6b03310e6a1',
                content_variables='{}'
            )
            return str(response)
        elif incoming_msg.lower() == 'main menu':
            # Send options (services/book)
            send_template_message(
                to_number=from_number,
                template_ssid='HXe5d68dfc9de1bd47de7cf6b03310e6a1',
                content_variables='{}'
            )
            # Send options (call/visti website)
            send_template_message(
                to_number=from_number,
                template_ssid='HX4f4cba6f5f6929ab6782a41d0c3866a9',
                content_variables='{}'
            )
            user_states[from_number] = {'state': 'response 2'}
            #user_states[from_number] = 'response 2'
            response = MessagingResponse()
            response.message("")
            return str(response)
        
        response = MessagingResponse()
        response.message("")    
        return str(response)
    
    
    
    elif state == 'response 2':
        
        if incoming_msg.lower() == 'services & prices':
            response = MessagingResponse()
            response.message("🌟 Welcome to [Your Salon Name]! 🌟\n\n💇‍♀️ **Hair Services:**\n- Haircut (Ladies) – $25\n- Haircut (Men) – $15\n- Hair Color – Starting at $50\n- Blow-Dry & Styling – $30\n\n💅 **Nail Services:**\n- Manicure – $20\n- Pedicure – $25\n- Nail Extensions – $40\n\n💆‍♀️ **Skin & Spa:**\n- Facial – $35\n- Body Massage – $60\n- Waxing – Starting at $15\n\n✨ **Special Packages:**\n- Bridal Package – $150\n- Party Glam – $90\n\n📞 Call us at **[Your Phone Number]** or 📍 visit us at **[Your Location]** to book your appointment today!\n\nWe’re here to make you feel fabulous! 💖")
            print(str(response))
            return str(response)
        elif incoming_msg.lower() == 'offers & promotions':
            response = MessagingResponse()
            response.message("🎉 **Exciting Offers & Promotions!** 🎉\n\n💇‍♀️ Get a **free haircut** with any hair color service!\n💅 Enjoy a **20% discount** on all nail services every Monday!\n💆‍♀️ Book a facial and get a **complimentary massage**!\n\n🌟 Limited time only! Don’t miss out – visit us or call now to avail these amazing deals! 💖")
            return str(response)
        elif incoming_msg.lower() == 'book an appointment':
            # Send Schedule
            send_template_message(
                to_number=from_number,
                template_ssid='HXa51a6f4af0a17e8210f60c13a6caca81',
                content_variables='{}'
            )
            user_states[from_number] = {'state': 'response 3'}
            #user_states[from_number] = 'response 3'
        response = MessagingResponse()
        response.message("")
        return str(response)
    
    
    
    elif state == 'response 3':
        
        if 1<=int(incoming_msg)<=10:
            number = int(incoming_msg)
            if number == 1:
                user_states[from_number]['Booking_time'] = '10:00 - 11:00 AM'
            elif number == 2:
                user_states[from_number]['Booking_time'] = '11:00 - 12:00 PM'
            elif number == 3:
                user_states[from_number]['Booking_time'] = '12:00 - 1:00 PM'
            elif number == 4:
                user_states[from_number]['Booking_time'] = '1:00 - 2:00 PM'
            elif number == 5:
                user_states[from_number]['Booking_time'] = '2:00 - 3:00 PM'
            elif number == 6:
                user_states[from_number]['Booking_time'] = '3:00 - 4:00 PM'
            elif number == 7:
                user_states[from_number]['Booking_time'] = '4:00 - 5:00 PM'
            elif number == 8:
                user_states[from_number]['Booking_time'] = '5:00 - 6:00 PM'
            elif number == 9:
                user_states[from_number]['Booking_time'] = '6:00 - 7:00 PM'
            elif number == 10:
                user_states[from_number]['Booking_time'] = '7:00 - 8:00 PM'
            # Send Days options
            send_template_message(
                to_number=from_number,
                template_ssid='HXcddb9e061952bbdfbfb5ef76ae67b053',
                content_variables='{}'
            )
            #user_states[from_number] = 'response 4'
            user_states[from_number]['state'] = 'response 4'
            response = MessagingResponse()
            response.message("")
            return str(response)
        
        response = MessagingResponse()
        response.message("")
        return str(response)
    
    
    
    elif state == 'response 4':
        
        if "today" in incoming_msg.lower() or "tomorrow" in incoming_msg.lower() or "day after tomorrow" in incoming_msg.lower():
            
            Booking_day = incoming_msg
            # Save Booking_day in user state
            user_states[from_number]['Booking_day'] = Booking_day
            response = MessagingResponse()
            response.message(f'Your appointment is confirmed {customer_name} at {user_states[from_number]["Booking_time"]} for {Booking_day}. We look forward to seeing you soon! 😊')
            user_states[from_number]['state'] = 'idle'
            return str(response)
        
        response = MessagingResponse()
        response.message("")
        return str(response)
    
    
    
    elif state == 'idle':
        
        response = MessagingResponse()
        response.message("")
        return str(response)



    # Default response for unknown state
    response = MessagingResponse()
    response.message("")
    user_states[from_number] = 'start'
    return str(response)

if __name__ == '__main__':
    setup_database()
    app.run(port=5000)
