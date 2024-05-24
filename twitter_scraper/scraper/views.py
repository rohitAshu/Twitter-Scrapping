import json
from django.utils import timezone
from time import sleep
import time
import random
import threading

from rest_framework import status
from rest_framework.decorators import api_view
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from .serializers import TwitterProfileSerializers, TweetHashtagSerializer, TweetUrlSerializer
from .utils import twitterLogin_auth, message_json_response, save_data_in_directory, random_sleep
from .web_driver import initialize_driver

MAX_THREAD_COUNT=5
MAX_EXCEPTION_RETRIES = 2

def print_current_thread():
    current_thread = threading.current_thread()
    print("---------- Current Thread:", current_thread.name)

def retry_Exception(recalling_method_name,any_generic_parameter,retry_count,exception_name):
         # If tweet elements are not found, check if retry attempts are exhausted
                if retry_count < MAX_EXCEPTION_RETRIES:
                    retry_count=retry_count + 1
                    # Retry the function after a delay
                    print(f"******* Retrying attempt after ',{exception_name} in {recalling_method_name},' , Attempt #:' {retry_count}")
                    random_sleep  # Add a delay before retrying
                    return recalling_method_name(any_generic_parameter,retry_count)
                else:
                    # Return a JSON response with an error message if retry attempts are exhausted
                    print(f'!!!!!!!!!!!!! All the retry attempts exhausted. Throwing error now........')
                    return message_json_response(status.HTTP_404_NOT_FOUND, 'error', 'Element not found')
                

# Function to scrape tweets from a profile
def scrape_profile_tweets(profile_name,retry_count):
    print_current_thread()
    driver = initialize_driver()
    
    # Authenticate with Twitter
    success, message = twitterLogin_auth(driver)
    if not success:
        return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'Twitter Authentication Error')

    try:
        random_sleep()
        search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
        search_box.send_keys(profile_name)
        search_box.send_keys(Keys.ENTER)
        print(f'Search box data entered')
        random_sleep()
    
        people = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span")
        people.click()
        print(f'People clicked.')
        random_sleep()
    
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")))
        profile = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
        profile.click()
        print(f'Profile clicked.')
        random_sleep()
    

        data = []
        articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
    
        # Scrape tweets until the desired number is reached or no more tweets are available
        while True:
            for _ in articles:                
                user_tag = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]").text
                timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                reply = driver.find_element(By.XPATH, f'//*[@data-testid="reply"]').text
                retweet = driver.find_element(By.XPATH, '//button[@data-testid="retweet"]//span').text
                likes = driver.find_element(By.XPATH, '//button[@data-testid="like"]//span').text
                data.append({
                    "Name": profile_name,
                    "UserTag": user_tag,
                    "Timestamp": timestamp,
                    "TweetContent": tweet,
                    "Reply": reply,
                    "Retweet": retweet,
                    "Likes": likes
                })
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                if len(data) > 5:
                    break
            break

    except NoSuchElementException as e:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_profile_tweets,profile_name,retry_count,type(e).__name__)
    except StaleElementReferenceException as ex:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_profile_tweets,profile_name,retry_count,type(ex).__name__)

    # Save the scraped data to a directory
    save_data_in_directory(f"Json_Response/{timezone.now().date()}/", profile_name, data)
    if 'driver' in locals():
        driver.quit()
    return message_json_response(status.HTTP_200_OK, 'success', 'Tweets retrieved successfully', data=data)



@api_view(["POST"])
def get_Tweeted_via_profile_name(request):
    serializer = TwitterProfileSerializers(data=request.data)
    profile_name = request.data.get("Profile_name")
    if serializer.is_valid():
        # Use ThreadPoolExecutor to run the scrape_profile_tweets function in a separate thread
        with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
            future = executor.submit(scrape_profile_tweets, profile_name, 0)
            result = future.result()
        return result
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)


# Function to scrape tweets based on hashtags
def scrape_hashtag_tweets(hashtags,retry_count):
    print_current_thread()
    driver = initialize_driver()
    
    # Authenticate with Twitter
    success, message = twitterLogin_auth(driver)
    if not success:
        return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'Twitter Authentication Failed')

    try:
        random_sleep()
        search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
        search_box.send_keys(hashtags)
        search_box.send_keys(Keys.ENTER)
        random_sleep()
    
        data = []
    
        articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
    
        # Scrape tweets until the desired number is reached or no more tweets are available
        while True:
            for article in articles:
                timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                reply = driver.find_element(By.XPATH, f'//*[@data-testid="reply"]').text
                retweet = driver.find_element(By.XPATH, '//button[@data-testid="retweet"]//span').text
                likes = driver.find_element(By.XPATH, '//button[@data-testid="like"]//span').text
                data.append({
                    "Timestamp": timestamp,
                    "TweetContent": tweet,
                    "Reply": reply,
                    "Retweet": retweet,
                    "Likes": likes
                })
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                if len(data) > 5:
                    break
            break
    except NoSuchElementException as e:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_hashtag_tweets,hashtags,retry_count,type(e).__name__)
    except StaleElementReferenceException as ex:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_hashtag_tweets,hashtags,retry_count,type(ex).__name__)


    # Save the scraped data to a directory
    save_data_in_directory(f"Json_Response/{timezone.now().date()}/", hashtags, data)
    if 'driver' in locals():
        driver.quit()
    return message_json_response(status.HTTP_200_OK, 'success', 'Tweets retrieved successfully', data=data)
                

@api_view(["POST"])
def fetch_tweets_by_hash_tag(request):
    """
    Fetch tweets by hashtag.

    This endpoint accepts a POST request with hashtags in the request data, 
    validates the data using TweetHashtagSerializer, and uses a 
    ThreadPoolExecutor to run the scrape_hashtag_tweets function in a separate 
    thread to fetch tweets associated with the provided hashtags.

    Args:
        request: The HTTP request object containing the hashtags in the request data.

    Returns:
        A JSON response containing the result of the scrape_hashtag_tweets function 
        if the request data is valid, or an error message if the data is invalid.
    """
    serializer = TweetHashtagSerializer(data=request.data)
    hashtags = request.data.get("hashtags")
    if serializer.is_valid():
        # Use ThreadPoolExecutor to run the scrape_hashtag_tweets function in a separate thread
        with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
            future = executor.submit(scrape_hashtag_tweets, hashtags, 0)
            result = future.result()
        return result
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)



# Function to scrape trending hashtags
def scrape_trending_hashtags(request, retry_count):
    print_current_thread()
    driver = initialize_driver()
    
    # Authenticate with Twitter
    success, message = twitterLogin_auth(driver)
    if not success:
        return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'Twitter Authentication Failed')

    try:
        random_sleep()
        explore_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div/div[2]/span")
        explore_btn.click()
        random_sleep()

        trending_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span")
        trending_btn.click()
        random_sleep()

        # Scroll to the bottom of the page to load more content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep()
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


            trending_topics_elements = driver.find_elements(By.XPATH, '//*[@data-testid="cellInnerDiv"]')

    except NoSuchElementException as e:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_trending_hashtags,request,retry_count,type(e).__name__)
    except StaleElementReferenceException as ex:
        if 'driver' in locals():
            driver.quit()
        return retry_Exception(scrape_trending_hashtags,request,retry_count,type(ex).__name__)

    trending_topics = [element.text for element in trending_topics_elements]
    
    # Save the scraped data to a directory
    save_data_in_directory(f"Json_Response/{timezone.now().date()}/", "Trending", trending_topics)
    if 'driver' in locals():
        driver.quit()
    return message_json_response(status.HTTP_200_OK, 'success', 'Trending hashtags retrieved successfully', data=trending_topics)



@api_view(["GET"])
def get_trending_tweets(request):
    """
    Function to get trending tweets by scraping Twitter for trending hashtags.

    Args:
        request (HttpRequest): The HTTP request object containing the request data.

    Returns:
        JSONResponse: A JSON response containing the scraped trending tweets data or an error message.
    """
    
    # Use ThreadPoolExecutor to run the scrape_trending_hashtags function in a separate thread
    with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
        # Submit the scrape_trending_hashtags function with the request data as argument
        future = executor.submit(scrape_trending_hashtags, request, 0)
        
        # Get the result of the future task
        result = future.result()
    
    # Return the result as a JSON response
    return result



def scrape_comments_for_tweets(request,retry_count):
    """
    Function to scrape comments for tweets from Twitter.

    Args:
        request (HttpRequest): The HTTP request object containing the tweet data.

    Returns:
        JSONResponse: A JSON response containing the scraped comments data or error message.
    """

    # Validate the incoming request data using the TweetUrlSerializer
    serializer = TweetUrlSerializer(data=request.data)
    if serializer.is_valid():
        # Print the current working thread
        print_current_thread()
        
        # Initialize the WebDriver
        driver = initialize_driver()
        
        # Extract post IDs from the request data
        post_ids = request.data.get('post_ids')

        # Authenticate with Twitter
        success, message = twitterLogin_auth(driver)
        if success:
            # Add a random sleep for realistic behavior
            random_sleep()

        # Initialize an empty list to store the scraped data
        data = []

        # Iterate over each post ID
        for post_id in post_ids: 
            print(f'user_name=',request.data.get('user_name'))
            print(f'post_id=',post_id)   
            # Construct the URL of the tweet to scrape comments from
            twitter_url = f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            
            # Load the tweet URL in the browser
            driver.get(twitter_url)
            print(f'Twitter_url=',twitter_url)

            # Add another random sleep for realistic behavior
            random_sleep()
            
            try:
                # Find elements corresponding to tweets
                driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            
                # Extract relevant information from the tweet elements
                tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                image_url = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img').get_attribute('src')
                reply_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="reply"]').find_element(By.CSS_SELECTOR,
                                                                                                            'span[data-testid="app-text-transition-container"] span').text
                like_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]').find_element(By.CSS_SELECTOR,
                                                                                                            'span[data-testid="app-text-transition-container"] span').text
                repost_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="retweet"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text
                bookmark_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="bookmark"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                views_count = driver.find_element(By.CSS_SELECTOR, 'span.css-1jxf684').text
                
                # Append the extracted data to the list
                data.append({
                    "username": request.data.get('user_name'),
                    "TweetContent": tweet,
                    "views_count": views_count,
                    "timestamp": timestamp,
                    "content_image": image_url,
                    "reply_count": reply_count,
                    "like_count": like_count,
                    "repost_count": repost_count,
                    "bookmark_count": bookmark_count
                })

            except NoSuchElementException as e:
                if 'driver' in locals():
                    driver.quit()
                return retry_Exception(scrape_comments_for_tweets,request,retry_count,type(e).__name__)
                # return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'tweet_elements element not found')
            except StaleElementReferenceException as ex:
                if 'driver' in locals():
                    driver.quit()
                return retry_Exception(scrape_comments_for_tweets,request,retry_count,type(ex).__name__)
                # return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'tweet_elements stale element exception')
        
        # Save the scraped data in a directory
        save_data_in_directory(f"Json_Response/{timezone.now().date()}/", request.data.get('user_name'), data)
        
        if 'driver' in locals():
            driver.quit()

        # Return a success response with the scraped data
        return message_json_response(status.HTTP_200_OK, 'error', 'tweets get  successFully', data=data)
    
    # Return an error response if the request data is invalid
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)



@api_view(["POST"])
def get_comments_for_tweets(request):
    """
    Endpoint to asynchronously scrape comments for tweets from Twitter.

    Args:
        request (HttpRequest): The HTTP request object containing the tweet data.

    Returns:
        JSONResponse: A JSON response containing the scraped comments data or error message.
    """

    # Use ThreadPoolExecutor to run the scrape_comments_for_tweets function in a separate thread
    with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
        # Submit the scrape_comments_for_tweets function to the executor with the request object as argument
        future = executor.submit(scrape_comments_for_tweets, request, 0)
        
        # Wait for the function to complete and retrieve the result
        result = future.result()

    # Return the result obtained from scraping comments
    return result



def scrape_tweets_by_url(request,retry_count):
    """
    Endpoint to scrape tweets from Twitter based on provided post URLs.

    Args:
        request (HttpRequest): The HTTP request object containing the data to be scraped.

    Returns:
        JSONResponse: A JSON response containing the scraped tweet data or error message.
    """
    # Deserialize request data using TweetUrlSerializer
    serializer = TweetUrlSerializer(data=request.data)

    # Check if serializer data is valid
    if serializer.is_valid():
        # Print the current working thread
        print_current_thread()

        # Initialize the Selenium WebDriver
        driver = initialize_driver()

        # Extract post IDs from the request data
        post_ids = request.data.get('post_ids')

        # Authenticate with Twitter and check if authentication is successful
        success, message = twitterLogin_auth(driver)
        if success:
            # Introduce a random sleep to simulate human-like behavior
            random_sleep()

        # Initialize an empty list to store scraped tweet data
        data = []
        
        # Iterate over each post ID
        for post_id in post_ids:
            # Construct the Twitter URL for the post using the username and post ID
            twitter_url = f"https://x.com/{request.data.get('user_name')}/status/{post_id}"

            try:
                # Load the Twitter URL in the WebDriver
                driver.get(twitter_url)

                # Introduce a random sleep to simulate human-like behavior
                random_sleep()
                
                # Find tweet elements
                tweet_elements = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')

                # Extract various attributes of the tweet
                tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                image_url = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img').get_attribute('src')
                reply_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="reply"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text
                like_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text
                repost_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="retweet"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text
                bookmark_count = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="bookmark"]').find_element(
                    By.CSS_SELECTOR, 'span[data-testid="app-text-transition-container"] span').text

                # Scroll to the bottom of the page to load additional content
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

                # Extract timestamp and views count
                timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                views_count = driver.find_element(By.CSS_SELECTOR, 'span.css-1jxf684').text

                # Append scraped data to the list
                data.append({
                    "username": request.data.get('user_name'),
                    "TweetContent": tweet,
                    "views_count": views_count,
                    "timestamp": timestamp,
                    "content_image": image_url,
                    "reply_count": reply_count,
                    "like_count": like_count,
                    "repost_count": repost_count,
                    "bookmark_count": bookmark_count
                })

            except NoSuchElementException as e:
                if 'driver' in locals():
                    driver.quit()
                return retry_Exception(scrape_tweets_by_url,request,retry_count,type(e).__name__)
                # return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'tweet_elements element not found')
            except StaleElementReferenceException as ex:
                if 'driver' in locals():
                    driver.quit()
                return retry_Exception(scrape_tweets_by_url,request,retry_count,type(ex).__name__)
                # return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'tweet_elements stale element exception')

        # Save the scraped data to a directory
        save_data_in_directory(f"Json_Response/{timezone.now().date()}/", request.data.get('user_name'), data)
        
        if 'driver' in locals():
            driver.quit()
            
        # Return a JSON response with success message and scraped data
        return message_json_response(status.HTTP_200_OK, 'success', 'Tweets retrieved successfully', data=data)

    # If serializer data is not valid, return a JSON response with serializer errors
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)



@api_view(["POST"])
def get_tweets_by_url(request):
    """
    Endpoint to asynchronously scrape tweets from Twitter based on provided post URLs.

    Args:
        request (HttpRequest): The HTTP request object containing the data to be scraped.

    Returns:
        JSONResponse: A JSON response containing the scraped tweet data or error message.
    """

    # Use ThreadPoolExecutor to run the scrape_tweets_by_url function in a separate thread
    with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
        # Submit the scrape_tweets_by_url function to the executor with the request object as argument
        future = executor.submit(scrape_tweets_by_url, request, 0)
        
        # Wait for the function to complete and retrieve the result
        result = future.result()

    # Return the result obtained from scraping tweets
    return result
