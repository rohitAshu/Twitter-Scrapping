import os
import random
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from django.http import JsonResponse
from typing import Optional, Dict
from rest_framework import status
import json
# List of user credentials
USER_CREDENTIALS = [
    {"username": "ExoticaLtd", "password": "S5Us3/)pT$.H#yy"},
    {"username": "kR4285512683720", "password": "Kr@200020"},
    # {"username": "RakeshVerma", "password": "RakeshVerma@123"},
    # Add more user credentials as needed
]


def twitterLogin_auth(driver):
    """
       Perform Twitter login authentication.
       Returns:NoSuchElementException
           tuple: A tuple containing a boolean indicating success or failure of the login attempt,
                  and a string with a message indicating the outcome.
                  :rtype: object
       """
    # Select a random set of credentials
    credentials = random.choice(USER_CREDENTIALS)
    username_value = credentials['username']
    password_value = credentials['password']

    driver.get('https://twitter.com/i/flow/login')
    sleep(10)
    try:
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys(username_value)
        print("Username element found and value sent successfully.")

        pass
    except NoSuchElementException:
        return False, "username E    Profile_name = serializers.CharField(required=True)lement not found"
    try:
        next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
        next_button.click()
        print("Next button element found and clicked successfully.")
        sleep(5)
        pass
    except NoSuchElementException:
        return False, "next_button Element not found"
    try:
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys(password_value)
        print("Password element found and value sent successfully.")
    except NoSuchElementException:
        return False, "password Element not found"
    try:
        log_in = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
        log_in.click()
        print("Log in button found and clicked successfully.")
    except NoSuchElementException:
        return False, "log_injson_dumps_params={'indent': 2} Element not found"
    return True, "Twitter Login Successfully"


def save_data_in_directory(folder_name, file_name , json_data: dict):
    """
    Saves JSON data in a specified directory with the provided file name.

    If the specified directory does not exist, it creates the directory.

    Parameters:
    - folder_name (str): The name of the directory where the data will be saved.
    - file_name (str): The name of the file to be created (without the extension).
    - json_data (dict): The JSON data to be saved.

    Returns:
    - None

    Example:
    ```
    json_data = {"key": "value"}
    save_data_in_directory("my_folder", "my_file", json_data)
    ```

    This will create a file named "my_file.json" inside the "my_folder" directory and save the JSON data in it.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, f"{file_name}.json")
    print(file_path)
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return True

def message_json_response(code: int, error_type: str, error_message: str, data: Optional[Dict] = None) -> JsonResponse:
    """
    Create a JSON response with the provided code, error type, error message, and optional data.

    Parameters:
    - code (int): The HTTP status code to be returned.
    - error_type (str): The type of error.
    - error_message (str): The error message.
    - data (dict, optional): Additional data to include in the response.

    Returns:
    - JsonResponse: A JSON response containing the provided data and status code.
    """
    response_data = {
        "code": code,
        "type": error_type,
        "message": error_message,
    }
    if data:
        response_data["data"] = data

    return JsonResponse(response_data, status=code, json_dumps_params=dict(indent=2))
