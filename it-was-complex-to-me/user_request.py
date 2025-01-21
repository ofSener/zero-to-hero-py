import os
from datetime import datetime
import requests

def timeout_input():
    while True:
        try:
            timeout = int(input("Enter the timeout: "))
            if timeout <= 0:
                print("Error: Timeout must be greater than 0")
                continue
            return timeout  # Geçerli bir değer olduğunda döndür
        except ValueError:
            print("Error: Timeout must be an integer")
            # Tekrar soracak, döngüye geri dönecek
    

def request_response(user_url, timeout):
   
    try:
        print("Requesting...")
        response = requests.get(user_url, timeout=timeout)
        print("status code: ", response.status_code)
        #create a folder named "response" if it exists ,do nothing
        if not os.path.exists("user_request_urls"):  
            os.makedirs("user_request_urls")
        #create a file with the name of the url and date and time
        with open(os.path.join("user_request_urls", user_url.split("/")[-1] + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "w") as file:
            file.write(response.text)

        print("response body: ", response.text[:100])


        token = input("type q to quit or press any key to continue \n")
        if token == 'q':
            return 'q'

    except requests.exceptions.Timeout:
        print("Error: Timeout")

    except requests.exceptions.ConnectionError:
        print("Error: No connection  ")

    except requests.exceptions.RequestException as e:
        print("Error: ", e)

def get_valid_url():    
    while True:
        user_url = input("Enter the url: ")

        if user_url.strip() == '':
            print("Error: URL cannot be empty")
            continue
        if "localhost" in user_url :
            return user_url
        else:
            if "." not in user_url:
                print("Error: URL must contain '.' or be 'localhost'")
            else:
                return user_url
            
def add_protocol_if_needed(url):
    
    if url.startswith("http://") or url.startswith("https://"):
        return url
    
    choice = input("Press 'y' to use HTTPS, 'n' to use HTTP")
    if choice.lower() == 'y':
        return "https://" + url
    else:
        return "http://" + url


def main():
    while True:
        user_url = get_valid_url()
        if user_url is None:
            print("Error: URL cannot be empty")


        user_url = add_protocol_if_needed(user_url)

        timeout = timeout_input()

        token = request_response(user_url, timeout)
        if token == 'q':
            return False

if __name__ == "__main__":
    main()


