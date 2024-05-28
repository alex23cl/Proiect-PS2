from flask import Flask, render_template, request, redirect, url_for, session
import serial
import time

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
arduino = serial.Serial('COM4', 9600)  # Inițializarea portului serial

# Lista pentru a stoca ultimele 10 mesaje
recent_messages = []
MAX_MESSAGES = 10

def read_messages_from_eeprom():
    messages = []
    for address in range(MAX_MESSAGES):
        message = ""
        for i in range(32): # Lungimea maximă a unui mesaj este 32 de caractere
            char = chr(arduino.read())
            if char == '\0':
                break
            message += char
        if message:
            messages.append(message)
    return messages

@app.route('/')
def index():
    # Citirea stării LED-ului și temperaturii de la Arduino
    temperature = arduino.readline().decode().strip()
    led_state = session.get('led_state', None)
    return render_template('interface.html', led_state=led_state, temperature=temperature)

@app.route('/control', methods=['POST'])
def control():
    # Controlul LED-ului în funcție de comanda primită
    command = request.form['command']
    if command == 'ON':
        arduino.write(b'A')  # Trimite comanda pentru a aprinde LED-ul
        session['led_state'] = 'Aprins'
    elif command == 'OFF':
        arduino.write(b'S')  # Trimite comanda pentru a stinge LED-ul
        session['led_state'] = 'Stins'
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    arduino.write(message.encode())
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    recent_messages.insert(0, f"{timestamp} {message}")
    if len(recent_messages) > MAX_MESSAGES:
        recent_messages.pop()
    return render_template('interface.html', recent_messages=recent_messages, led_state=session.get('led_state', None), temperature=arduino.readline().decode().strip())


if __name__ == '__main__':
    time.sleep(2)  # Așteaptă stabilirea conexiunii
    app.run()
