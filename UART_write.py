import serial
import time

def enviarMovimiento(movimiento):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

        data = str(movimiento)
        ser.write(data.encode('utf-8'))
        time.sleep(10)
            
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').strip()
            print(received_data)
            return(0)
        else:
            print("No acknowledgment received.")
            return(400)
            
        time.sleep(1)  # Adjust the delay based on your requirements
            
    except:
        ser.close()
    print("Serial port closed.")
