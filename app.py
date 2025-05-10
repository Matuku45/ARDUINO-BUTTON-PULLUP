from flask import Flask, render_template_string
import serial
import serial.tools.list_ports

app = Flask(__name__)
ser = None
counter = 0

# List all available ports
print("[INFO] Available COM Ports:")
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(f" - {port.device}")

# Try to connect to the first available COM port
if ports:
    try:
        ser = serial.Serial("COM6", 9600, timeout=1)
        print(f"[INFO] Connected to {ser.port}")
    except serial.SerialException as e:
        print(f"[ERROR] Could not open COM port: {e}")
    except PermissionError as e:
        print(f"[ERROR] Access denied to COM port: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
else:
    print("[WARNING] No COM ports found.")

@app.route('/')
def index():
    return render_template_string("""
        <h1>Button Press Count: {{ count }}</h1>
        <p><a href="/update">Refresh Count</a></p>
    """, count=counter)

@app.route('/update')
def update():
    global counter
    if ser and ser.in_waiting:
        try:
            data = ser.readline().decode().strip()
            if data.isdigit():
                counter = int(data)
        except Exception as e:
            print(f"[ERROR] Failed to read from serial: {e}")
    return render_template_string("""
        <h1>Updated Count: {{ count }}</h1>
        <p><a href="/">Back to Home</a></p>
    """, count=counter)

@app.route('/ports')
def show_ports():
    ports = serial.tools.list_ports.comports()
    return render_template_string("""
        <h2>Available COM Ports:</h2>
        <ul>
        {% for p in ports %}
            <li>{{ p.device }} - {{ p.description }}</li>
        {% endfor %}
        </ul>
        <p><a href="/">Back to Home</a></p>
    """, ports=ports)

if __name__ == '__main__':
    app.run(debug=True)
