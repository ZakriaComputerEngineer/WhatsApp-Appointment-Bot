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
- **Public Exposure Using ngrok:**  
  Exposes the local Flask app to the internet using `ngrok` for seamless integration with Twilio Webhooks.

---

## **Installation and Setup**  
### **1. Clone the repository**
   ```bash
   git clone https://github.com/yourusername/WhatsApp-Appointment-Bot.git
   cd WhatsApp-Appointment-Bot
   ```

### **2. Install dependencies**
   ```bash
   pip install Flask twilio
   ```

### **3. Set up the database**
   ```bash
   python Appointment_bot.py
   ```
   This creates a `salon.db` file for customer data.

### **4. Run the Flask app locally**
   ```bash
   python Appointment_bot.py
   ```

### **5. Install and Start ngrok**
   Download and install `ngrok` from [https://ngrok.com/download](https://ngrok.com/download).

   Start `ngrok` with the following command:
   ```bash
   ngrok http 5000
   ```
   Copy the public URL provided by `ngrok` (e.g., `https://your-ngrok-url.ngrok.io`).

### **6. Set Twilio Webhook**
   Go to your Twilio Console and set the Webhook URL for incoming messages to:
   ```
   https://your-ngrok-url.ngrok.io/webhook
   ```

### **7. Replace placeholders in the code**
   - `account_sid = 'ENTER YOUR TWILIO ACCOUNT SID HERE'`
   - `auth_token = 'ENTER YOUR TWILIO AUTH TOKEN HERE'`
   - Replace template IDs in the `send_template_message()` function with your Twilio template IDs.

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

### **Exposing Flask App with ngrok**
```bash
ngrok http 5000
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

---

## **Future Motivation**  
The goal is to offer a fully automated appointment booking service across multiple messaging platforms (e.g., WhatsApp, Telegram). This will provide users with a convenient and flexible system to manage appointments without needing to visit a website or call reception.

---

## **Call for Collaboration**  
I'm a student working on this project and currently lack the resources to scale it. If you're interested in supporting or collaborating, please reach out to help bring this idea to life!

---
