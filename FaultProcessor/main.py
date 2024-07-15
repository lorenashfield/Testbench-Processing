import serial
import time


def read_uart(port, baudrate, output_file):
    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=0)
        print(f"Connected to {port} at {baudrate} baud rate")

        with open(output_file, 'w') as file:
            while True:
                if ser.in_waiting > 0:
                    # Read data from UART
                    data = ser.readline().decode('utf-8').strip()
                    if data:
                        # Print data to console (optional)
                        print(data)
                        # Write data to file
                        file.write(data + '\n')
                        # Flush the file to ensure data is written
                        file.flush()

                # Sleep for a short while to avoid high CPU usage
                time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Interrupted by user")


if __name__ == "__main__":
    # Define UART parameters
    port = '/dev/tty.usbmodem103'  # Replace with your port name
    baudrate = 115200
    output_file = 'uart_data.txt'  # Output file to store UART data

    read_uart(port, baudrate, output_file)
