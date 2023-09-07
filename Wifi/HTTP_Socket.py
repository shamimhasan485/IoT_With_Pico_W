import network
import socket

# Function to connect to a Wi-Fi network
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected.")
    print("Network config:", wlan.ifconfig())

# Function to make an HTTP request
def http_get_request(host, port, path="/"):
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
        request = f"GET {path} HTTP/1.0\r\n\r\n"
        s.send(request.encode())
        response = s.recv(1024)  # Adjust the buffer size as needed
        return response
    finally:
        s.close()

def main():
    ssid = 'Astra_Net'  # Replace with your Wi-Fi SSID
    password = 'astra2929'  # Replace with your Wi-Fi password
    host = "google.com"
    port = 80

    connect_to_wifi(ssid, password)

    # Make an HTTP GET request to google.com
    response = http_get_request(host, port)

    # Print the response
    print("HTTP Response:")
    print(response.decode())  # Decode bytes to a string

if __name__ == "__main__":
    main()
