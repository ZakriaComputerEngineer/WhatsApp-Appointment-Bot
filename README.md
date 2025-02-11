# WhatsApp-Appointment-Bot

A WhatsApp bot that simplifies appointment booking using templated replies through Twilio API. The bot integrates with a business API to register appointments seamlessly, eliminating the need for website visits or calls to reception. It stores customer information in a database for personalized interactions.

---

## **Key Features**  
- **Appointment Registration:**  
  Automatically book appointments by sending customer data to the business API.  
- **Customer Information Management:**  
  Stores and retrieves user data, including names and phone numbers.  
- **Dynamic State Handling:**  
  Manages user states for seamless conversation flow, from greeting to appointment confirmation.  
- **Templated Replies:**  
  Utilizes Twilio's templated messages for a smooth user experience.  

---

## **Installation and Setup**  
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WhatsApp-Appointment-Bot.git
   cd WhatsApp-Appointment-Bot
   ```
2. Install dependencies:
   ```bash
   pip install Flask twilio
   ```
3. Set up the database:
   ```bash
   python Appointment_bot.py
   ```
   This creates a `salon.db` file for customer data.

4. Replace placeholders in the code:
   - `account_sid = 'ENTER YOUR TWILIO ACCOUNT SID HERE'`
   - `auth_token = 'ENTER YOUR TWILIO AUTH TOKEN HERE'`
   - Replace template IDs in the `send_template_message()` function with your Twilio template IDs.

5. Run the bot:
   ```bash
   python Appointment_bot.py
   ```

---

## **Key Code Snippets**  

### **API Integration for Appointment Booking**
```python
api_url = f"{branch_apis[str(business_id)]}add_appointment/"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "SKED-API-KEY": "PUT YOUR API KEY HERE"
}
response = requests.post(api_url, data=form_data, headers=headers)
```

### **Saving Customer Information**
```python
def save_customer(phone, name):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO customers (phone, name) VALUES (?, ?)", (phone, name))
    conn.commit()
    conn.close()
```

### **Templated Message Sending with Twilio**
```python
def send_template_message(to_number, template_ssid, content_variables):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        content_sid=template_ssid,
        content_variables=content_variables,
        to=f'whatsapp:{to_number}'
    )
```

## **Future Motivation**  
The goal is to offer a fully automated appointment booking service across multiple messaging platforms (e.g., WhatsApp, Telegram). This will provide users with a convenient and flexible system to manage appointments without needing to visit a website or call reception.

---

## **Call for Collaboration**  
I'm a student working on this project and currently lack the resources to scale it. If you're interested in supporting or collaborating, please reach out to help bring this idea to life!

---
