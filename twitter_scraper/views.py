import threading
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .serializers import (
    TwitterProfileSerializers,
    TweetHashtagSerializer,
    TweetUrlSerializer,
)
from .utils import (
    twitter_login_auth,
    message_json_response,
    save_data_in_directory,
    random_sleep,
)
from .web_driver import InitializeDriver
from django.conf import settings


def print_current_thread():
    """
    Print the name of the current thread.

    This function retrieves the current thread using threading.current_thread()
    and prints its name.

    Example:
        print_current_thread()

    Output:
        ---------- Current Thread: MainThread
    """
    current_thread = threading.current_thread()
    print("---------- Current Thread:", current_thread.name)


MAX_THREAD_COUNT = 5
MAX_EXCEPTION_RETRIES = 3
NUMBER_OF_POSTS = 1

# Function to retry a given block of code


def retry_exception(recalling_method_name, any_generic_parameter, retry_count=0, exception_name=None):
    # If tweet elements are not found, check if retry attempts are exhausted
    if retry_count < MAX_EXCEPTION_RETRIES:
        retry_count = retry_count + 1
        # Retry the function after a delay
        print(
            f"******* Retrying attempt after {exception_name} in {recalling_method_name}, Attempt #: {retry_count}"
        )
        random_sleep()  # Add a delay before retrying
        return recalling_method_name(any_generic_parameter, retry_count)
    else:
        print(
            f"!!!!!!!!!!!!! All the retry attempts exhausted. Throwing error now........"
        )
        return message_json_response(status.HTTP_404_NOT_FOUND, "error", "Element not found")


def scrape_profile_tweets(profile_name=None, retry_count=0):
    """
    Scrapes the latest tweets from a specified Twitter profile.

    Args:
        profile_name (str): The Twitter handle of the profile to scrape tweets from.
        retry_count (int): The number of retries in case of errors during scraping.

    Returns:
        dict: A JSON response containing the status, message, and scraped tweet data if successful.
        str: Error message if the scraping fails.

    Raises:
        NoSuchElementException: If an element is not found on the page.
        StaleElementReferenceException: If an element is no longer attached to the DOM.
    """

    def tweet_content_exists(tweets, tweet_content):
        return any(tweet.get("TweetContent") == tweet_content for tweet in tweets)

    def save_data_and_return(data):
        save_data_in_directory(
            f"Json_Response/{timezone.now().date()}/", profile_name, data
        )
        return message_json_response(
            status.HTTP_200_OK, "success", "Tweets retrieved successfully", data=data
        )

    def scrap_data():
        nonlocal data
        articles = driver.find_elements(
            By.XPATH, "//div[@class='css-175oi2r' and @data-testid='cellInnerDiv']"
        )
        for article in articles:
            user_tag = article.find_element(
                By.XPATH,
                "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]",
            ).text
            
            parts = user_tag.split("\n")

            # Extract the username part
            username_with_at_symbol = parts[-1]

            # print(username_with_at_symbol)
            timestamp = article.find_element(By.XPATH, "//time").get_attribute(
                "datetime"
            )
            tweet = article.find_element(
                By.XPATH, "//div[@data-testid='tweetText']"
            ).text
            reply = article.find_element(By.XPATH, '//*[@data-testid="reply"]').text
            retweet = article.find_element(
                By.XPATH, '//button[@data-testid="retweet"]//span'
            ).text
            likes = article.find_element(
                By.XPATH, '//button[@data-testid="like"]//span'
            ).text

            if not tweet_content_exists(data, tweet):
                data.append(
                    {
                        "Name": profile_name,
                        "UserTag": username_with_at_symbol,
                        "Timestamp": timestamp,
                        "TweetContent": tweet,
                        "Reply": reply,
                        "Retweet": retweet,
                        "Likes": likes,
                    }
                )
                print("data : ", data)
                print("posts scrap : ", len(data))
        if len(data) >= NUMBER_OF_POSTS:
            print(f"{NUMBER_OF_POSTS} posts scrapp sucessfully")
            return save_data_and_return(data)

        driver.execute_script("window.scrollBy(0, 200);")
        sleep(5)
        scrap_data()

    def retry_scraping(exception_type):
        if "driver" in locals():
            driver.quit()
        return retry_exception(
            scrape_profile_tweets, profile_name, retry_count, exception_type
        )

    print_current_thread()
    driver_initializer = InitializeDriver()
    driver = driver_initializer.initialize_paid_proxy() if settings.PAIDPROXY else driver_initializer.initialize_free_proxy()
    print("Web Driver initialized successfully...")

    data = []
    success = twitter_login_auth(driver)
    if not success:
        return message_json_response(
            status.HTTP_400_BAD_REQUEST, "error", "Twitter Authentication Error"
        )

    try:
        search_box = driver.find_element(
            By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"
        )
        search_box.send_keys(profile_name)
        search_box.send_keys(Keys.ENTER)
        print("click on search !!!!!!!!!!!!!!!!!!!")
        random_sleep()
        people = driver.find_element(
            By.XPATH,
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span",
        )
        people.click()
        print("click on people !!!!!!!!!!!!!!!!!!")
        random_sleep()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]",
                )
            )
        )
        profile = driver.find_element(
            By.XPATH,
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]",
        )
        profile.click()
        print("click on people profile !!!!!!!!!!!!!!!!!!")
        random_sleep()
        scrap_data()
        sleep(2)
        driver.quit()
        return save_data_and_return(data)
    except NoSuchElementException as e:
        return retry_scraping(type(e).__name__)
    except StaleElementReferenceException as ex:
        return retry_scraping(type(ex).__name__)


@api_view(["POST"])
def get_tweeted_via_profile_name(request):
    """
    Handles POST requests to retrieve tweets from a specified Twitter profile.

    Args:
        request (HttpRequest): The HTTP request object containing the profile name in the request data.

    Returns:
        JsonResponse: A JSON response with the status, message, and scraped tweet data if successful.
                      If the request data is invalid, returns an error response with the validation errors.

    Raises:
        None
    """
    serializer = TwitterProfileSerializers(data=request.data)
    profile_name = request.data.get("Profile_name")
    if serializer.is_valid():
        with ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
            future = executor.submit(scrape_profile_tweets, profile_name, 0)
            result = future.result()
        return result
    return message_json_response(
        status.HTTP_400_BAD_REQUEST, "error", serializer.errors
    )


def scrape_hashtag_tweets(hashtags, retry_count):
    """
    Scrapes tweets containing specified hashtags.

    Args:
        hashtags (str): The hashtag(s) to scrape tweets for.
        retry_count (int): The number of retries in case of errors during scraping.

    Returns:
        dict: A JSON response containing the status, message, and scraped tweet data if successful.
        str: Error message if the scraping fails.

    Raises:
        NoSuchElementException: If an element is not found on the page.
        StaleElementReferenceException: If an element is no longer attached to the DOM.
    """

    def tweet_content_exists(tweets, tweet_content):
        return any(tweet.get("TweetContent") == tweet_content for tweet in tweets)

    def save_data_and_return(data):
        save_data_in_directory(
            f"Json_Response/{timezone.now().date()}/", hashtags, data
        )
        return message_json_response(
            status.HTTP_200_OK, "success", "Tweets retrieved successfully", data=data
        )

    def scrap_data():
        nonlocal data
        articles = driver.find_elements(
            By.XPATH, "//div[@class='css-175oi2r' and @data-testid='cellInnerDiv']"
        )
        for article in articles:
            timestamp = article.find_element(By.XPATH, "//time").get_attribute(
                "datetime"
            )
            tweet = article.find_element(
                By.XPATH, "//div[@data-testid='tweetText']"
            ).text
            reply = article.find_element(By.XPATH, '//*[@data-testid="reply"]').text
            retweet = article.find_element(
                By.XPATH, '//button[@data-testid="retweet"]//span'
            ).text
            likes = article.find_element(
                By.XPATH, '//button[@data-testid="like"]//span'
            ).text

            if not tweet_content_exists(data, tweet):
                data.append(
                    {
                        "Name": hashtags,
                        "Timestamp": timestamp,
                        "TweetContent": tweet,
                        "Reply": reply,
                        "Retweet": retweet,
                        "Likes": likes,
                    }
                )
                print("data :", data)
                print("posts scrap : ", len(data))

        if len(data) >= NUMBER_OF_POSTS:
            return save_data_and_return(data)

        driver.execute_script("window.scrollBy(0, 200);")
        sleep(5)
        scrap_data()

    def retry_scraping(exception_type):
        if "driver" in locals():
            driver.quit()
        return retry_exception(
            scrape_hashtag_tweets, hashtags, retry_count, exception_type
        )

    print_current_thread()
    driver_initializer = InitializeDriver()
    driver = driver_initializer.initialize_paid_proxy() if settings.PAIDPROXY else driver_initializer.initialize_free_proxy()
    print("Driver initialized successfully...")

    data = []
    success = twitter_login_auth(driver)
    print("Login successful...")
    if not success:
        return message_json_response(
            status.HTTP_400_BAD_REQUEST, "error", "Twitter Authentication Error"
        )

    try:
        random_sleep()
        search_box = driver.find_element(
            By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"
        )
        search_box.send_keys(hashtags)
        search_box.send_keys(Keys.ENTER)
        print("Click on search box...")
        random_sleep()
        scrap_data()
        sleep(2)
        driver.quit()
        return save_data_and_return(data)
    except StaleElementReferenceException as ex:
        return retry_scraping(type(ex).__name__)
    except NoSuchElementException as e:
        return retry_scraping(type(e).__name__)


@api_view(["POST"])
def fetch_tweets_by_hash_tag(request):
    """
    Handles POST requests to fetch tweets based on specified hashtags.

    Args:
        request (HttpRequest): The HTTP request object containing the hashtags in the request data.

    Returns:
        JsonResponse: A JSON response with the status, message, and scraped tweet data if successful.
                      If the request data is invalid, returns an error response with the validation errors.

    Raises:
        None
    """
    retry_count = 0
    serializer = TweetHashtagSerializer(data=request.data)
    hashtags = request.data.get("hashtags")
    if serializer.is_valid():
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = executor.submit(scrape_hashtag_tweets, hashtags, retry_count)
            result = future.result()
        return result
    return message_json_response(
        status.HTTP_400_BAD_REQUEST, "error", serializer.errors
    )


def scrape_trending_hashtags(request, retry_count=0):
    """
    Scrape trending hashtags from Twitter.

    This function scrapes trending hashtags from Twitter's explore section. It scrolls through the page
    to load all trending topics and extracts relevant information such as ID, category, type, trending topic,
    and number of posts.

    Args:
    - request (HttpRequest): The HTTP request object.
    - retry_count (int): The number of times the function has retried scraping.

    Returns:
    - Tuple[bool, list]: A tuple containing a boolean indicating success (True) or failure (False),
                         and a list of dictionaries representing trending topics.
                         Each dictionary contains the following keys:
                         - "id": ID of the trending topic.
                         - "category": Category of the trending topic.
                         - "type": Type of the trending topic.
                         - "trending": The trending topic itself.
                         - "posts": Number of posts related to the trending topic.
    """
    print_current_thread()
    driver_initializer = InitializeDriver()
    driver = driver_initializer.initialize_paid_proxy() if settings.PAIDPROXY else driver_initializer.initialize_free_proxy()
    print("initialize driver successful !!!!!!!!!!!!!!!!")
    twitter_login_auth(driver)
    print("login successful !!!!!!!!!!!!!!!!")
    try:
        random_sleep()

        explore_btn = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div/div[2]/span",
        )
        print("explore element is found")
        explore_btn.click()
        print("explore element clicked")
        random_sleep()
        trending_btn = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span",
        )
        print("trending element is found")
        trending_btn.click()
        print("trending element clicked")
        random_sleep()
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("new_height found")
        last_height = driver.execute_script("return document.body.scrollHeight")
        print("last limit is found")

        while True:
            random_sleep()
            driver.execute_script("window.scrollBy(0, 1000);")
            random_sleep()
            if new_height == last_height:
                break
            last_height = new_height
        trending_topics = []
        trending_topics_elements = driver.find_elements(
            By.XPATH, '//*[@data-testid="cellInnerDiv"]'
        )
        print("trending element is found")
        for element in trending_topics_elements:
            text = element.text.split("\n")
            if len(text) >= 4:
                item = {
                    "id": text[0].strip(),
                    "category": text[2].split(" · ")[0].strip(),
                    "type": (
                        text[2].split(" · ")[1].strip()
                        if " · " in text[2]
                        else "Trending"
                    ),
                    "trending": text[3].strip(),
                    "posts": text[4].strip() if len(text) > 4 else "N/A",
                }
                trending_topics.append(item)
        # json_response = trending_topics

    except NoSuchElementException as e:
        if "driver" in locals():
            driver.quit()
        return retry_exception(
            scrape_trending_hashtags, request, retry_count, type(e).__name__
        )
    except StaleElementReferenceException as ex:
        if "driver" in locals():
            driver.quit()
        return retry_exception(
            scrape_trending_hashtags, request, retry_count, type(ex).__name__
        )

    if "driver" in locals():
        driver.quit()
    return True, trending_topics


@api_view(["get"])
def get_trending_tweets(request):
    """
    Function to get trending tweets by scraping Twitter for trending hashtags.

    Args:
        request (HttpRequest): The HTTP request object containing the request data.

    Returns:
        JSONResponse: A JSON response containing the scraped trending tweets data or an error message.
    """

    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(scrape_trending_hashtags, request)
        # result = future.result()
        success, result = future.result()
    if not success:
        return message_json_response(status.HTTP_400_BAD_REQUEST, "error", result)
    print("done scrapping !!!!!!!!!!!!!!!!!!!!!!!!!!")
    save_data_in_directory(
        f"Json_Response/{timezone.now().date()}/", "Trending", result
    )
    return message_json_response(
        status.HTTP_200_OK, "success", "Tweets retrieved successfully", data=result
    )


def scrape_tweets_by_id(request, retry_count):
    """
    Endpoint to scrape tweets from Twitter based on provided post URLs.

    Args:
        request (HttpRequest): The HTTP request object containing the data to be scraped.

    Returns:
        JSONResponse: A JSON response containing the scraped tweet data or error message.
    """
    serializer = TweetUrlSerializer(data=request.data)
    if serializer.is_valid():
        print_current_thread()
        driver_initializer = InitializeDriver()
        driver = driver_initializer.initialize_paid_proxy() if settings.PAIDPROXY else driver_initializer.initialize_free_proxy()
        print("initialize driver sucessfulyy !!!!!!!!!!!!!!!!")
        post_ids = request.data.get("post_ids")

        success = twitter_login_auth(driver)
        if success:
            print("login sucessfully !!!!!!!!!!!!!!!!")
            random_sleep()

        data = []

        for post_id in post_ids:
            twitter_url = (
                f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            )
            try:
                driver.get(twitter_url)
                random_sleep()

                tweet = driver.find_element(
                    By.XPATH, "//div[@data-testid='tweetText']"
                ).text
                image_url = driver.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img'
                ).get_attribute("src")
                reply_count = (
                    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="reply"]')
                    .find_element(
                        By.CSS_SELECTOR,
                        'span[data-testid="app-text-transition-container"] span',
                    )
                    .text
                )
                like_count = (
                    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]')
                    .find_element(
                        By.CSS_SELECTOR,
                        'span[data-testid="app-text-transition-container"] span',
                    )
                    .text
                )
                repost_count = (
                    driver.find_element(
                        By.CSS_SELECTOR, 'button[data-testid="retweet"]'
                    )
                    .find_element(
                        By.CSS_SELECTOR,
                        'span[data-testid="app-text-transition-container"] span',
                    )
                    .text
                )
                bookmark_count = (
                    driver.find_element(
                        By.CSS_SELECTOR, 'button[data-testid="bookmark"]'
                    )
                    .find_element(
                        By.CSS_SELECTOR,
                        'span[data-testid="app-text-transition-container"] span',
                    )
                    .text
                )

                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

                timestamp = driver.find_element(By.XPATH, "//time").get_attribute(
                    "datetime"
                )
                views_count = driver.find_element(
                    By.CSS_SELECTOR, "span.css-1jxf684"
                ).text

                data.append(
                    {
                        "username": request.data.get("user_name"),
                        "TweetContent": tweet,
                        "views_count": views_count,
                        "timestamp": timestamp,
                        "content_image": image_url,
                        "reply_count": reply_count,
                        "like_count": like_count,
                        "repost_count": repost_count,
                        "bookmark_count": bookmark_count,
                    }
                )
                print("scrapping !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except NoSuchElementException as e:
                if "driver" in locals():
                    driver.quit()
                return retry_exception(
                    scrape_tweets_by_id, request, retry_count, type(e).__name__
                )
            except StaleElementReferenceException as ex:
                if "driver" in locals():
                    driver.quit()
                return retry_exception(
                    scrape_tweets_by_id, request, retry_count, type(ex).__name__
                )
        print("done scrapping !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        save_data_in_directory(
            f"Json_Response/{timezone.now().date()}/",
            request.data.get("user_name"),
            data,
        )

        if "driver" in locals():
            driver.quit()

        return message_json_response(
            status.HTTP_200_OK, "success", "Tweets retrieved successfully", data=data
        )

    return message_json_response(
        status.HTTP_400_BAD_REQUEST, "error", serializer.errors
    )


@api_view(["POST"])
def get_tweets_by_id(request):
    """
    Endpoint to asynchronously scrape tweets from Twitter based on provided post URLs.

    Args:
        request (HttpRequest): The HTTP request object containing the data to be scraped.

    Returns:
        JSONResponse: A JSON response containing the scraped tweet data or error message.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        retry_count = 0
        future = executor.submit(scrape_tweets_by_id, request, retry_count)
        result = future.result()

    return result


def get_comments_for_tweet(request, retry_count=0):
    """
    Retrieves comments for tweets identified by their post IDs.

    This function takes an HTTP request object containing data, validates it using a TweetUrlSerializer, and then initializes a WebDriver using the initialize_driver function. It then extracts the post IDs from the request data and attempts to log in to Twitter using the twitter_login_auth function.

    If the login is successful, the function iterates through each post ID, visits the corresponding tweet URL, clicks on the image element (assuming 'tweetPhoto' is the data-testid value for the image), and then collects the text content of elements matching a specific test_id (which is not defined in the provided code).

    The function scrolls through the page to load more content dynamically and collects all unique text content found.

    Once all comments are collected, they are returned as a JSON response with a success status code (HTTP 200 OK).

    Args:
        request: An HTTP request object containing data.

    Returns:
        A JSON respons data = []e containing comments for the specified tweets.

    Raises:
        NoSuchElementException: If the reply element is not found.
    """
    serializer = TweetUrlSerializer(data=request.data)
    if serializer.is_valid():
        driver_initializer = InitializeDriver()
        driver = driver_initializer.initialize_paid_proxy() if settings.PAIDPROXY else driver_initializer.initialize_free_proxy()
        print("initilize driver !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        post_ids = request.data.get("post_ids")
        success = twitter_login_auth(driver)
        if success:
            print("login sucessfully !!!!!!!!!!!!!!!!!!!!!!!!!!")
            sleep(16)
        data = []

        for post_id in post_ids:
            twiiter_url = (
                f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            )
            driver.get(twiiter_url)
            sleep(5)
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@role='article']")))
                
                while len(data) < 5:
                    # Scroll down to load more comments
                    driver.execute_script("window.scrollBy(0, 200);")
                    sleep(5)
                    
                    # Locate all tweet elements
                    elements = driver.find_elements(By.XPATH, "//*[@role='article']")
                    
                    for element in elements:
                        # Extract comment text
                        comment_text = element.text.strip()
                        if comment_text and {"comment": comment_text} not in data:
                            data.append({"comment": comment_text})
            except NoSuchElementException as e:
                if "driver" in locals():
                    driver.quit()
                return retry_exception(
                    scrape_trending_hashtags, request, retry_count, type(e).__name__
                )
        if data:
            formatted_comments = []
            for item in data:
                comment_text = item['comment'].split('\n')
                
                try:
                    if len(comment_text) >= 8:
                        name = comment_text[0]
                        username = comment_text[1]
                        time = comment_text[3]
                        comment = comment_text[4]
                        likes = comment_text[5].split()[0]
                        views = comment_text[7]
                        
                        formatted_comment = {
                            "Name": name,
                            "Username": username,
                            "Time": time,
                            "Comment": comment,
                            "Likes": likes,
                            "Views": views
                        }
                        
                        formatted_comments.append(formatted_comment)
                    else:
                        print(f"Skipping item due to insufficient data: {item['comment']}")
                except IndexError as e:
                    print(f"Error processing item: {item['comment']}. Error: {str(e)}")
            
            json_response = {"comments": formatted_comments}
            save_data_in_directory(
            f"Json_Response/{timezone.now().date()}/", 'profile_name', data
        )
            return message_json_response(
            status.HTTP_200_OK, "success", "comments get  successFully", data=json_response
        )

@api_view(["POST"])
def get_comments_for_tweets(request):
    """
    Endpoint to asynchronously scrape comments for tweets from Twitter.

    Args:
        request (HttpRequest): The HTTP request object containing the tweet data.

    Returns:
        JSONResponse: A JSON response containing the scraped comments data or error message.
    """

    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(get_comments_for_tweet, request)
        result = future.result()
    return result
