import json
from django.utils import timezone
from time import sleep

from rest_framework import status
from rest_framework.decorators import api_view
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .serializers import TwitterProfileSerializers, TweetHashtagSerializer, TweetUrlSerializer
from .utils import twitterLogin_auth, message_json_response, save_data_in_directory
from .web_driver import initialize_driver


@api_view(["POST"])
def get_Tweeted_via_profile_name(request):
    """
    Retrieves tweets from a Twitter profile via its profile name using Selenium WebDriver.

    Parameters:
    - request (HttpRequest): The HTTP request object containing data.

    Returns:
    - JsonResponse: A JSON response with the retrieved tweets and status message.

    Example usage:
    ```
    # POST request to retrieve tweets from a Twitter profile
    # Request body should contain {"Profile_name": "twitter_handle"}
    response = get_Tweeted_via_profile_name(request)
    ```
    """
    serializer = TwitterProfileSerializers(data=request.data)
    profile_name = request.data.get("Profile_name")

    if serializer.is_valid():
        # Initialize Selenium WebDriver
        driver = initialize_driver()
        # Attempt Twitter login
        success, message = twitterLogin_auth(driver)
        if success:
            sleep(16)
            try:
                # Search for the profile name
                search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
                search_box.send_keys(profile_name)
                search_box.send_keys(Keys.ENTER)
                print("Entered the subject and clicked Successfully !!")
                sleep(3)
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'search_box Element not found')

            try:
                # Click on the 'People' tab
                people = driver.find_element(By.XPATH,
                                             "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span")
                people.click()
                sleep(5)
                print("Clicked on people Successfully !!")
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'people Element not found')

            try:
                # Click on the profile
                profile = driver.find_element(By.XPATH,
                                              "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
                profile.click()
                sleep(5)
                print("Went on profile Man ")
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'profile Element not found')

            data = []
            try:
                # Retrieve tweets
                articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'articles Element not found')

            while True:
                for _ in articles:
                    user_tag = driver.find_element(By.XPATH,
                                                   "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]").text
                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                    tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                    testid_value = 'reply'
                    reply = driver.find_element(By.XPATH, f'//*[@data-testid="{testid_value}"]').text
                    retweet = driver.find_element(By.XPATH,
                                                  '//button[@data-testid="retweet"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]').text
                    likes = driver.find_element(By.XPATH,
                                                '//button[@data-testid="like"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]').text
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
            # Save data to JSON file
            save_data_in_directory(f"Json_Response/{timezone.now().date()}/",profile_name, data)
            return message_json_response(status.HTTP_200_OK, 'success', 'Tweets get SuccessFully', data=data)

        return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'Twitter Authentication Error')

    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)


@api_view(["POST"])
def fetch_tweets_by_hash_tag(request):
    """
    Retrieves tweets based on hashtags using Selenium WebDriver.

    This function performs the following steps:
    1. Validates the request data using the TweetHashtagSerializer serializer.
    2. Initializes a Selenium WebDriver instance.
    3. Logs in to Twitter using authentication.
    4. Enters the provided hashtag in the Twitter search box.
    5. Retrieves tweet data including timestamp, tweet content, reply count, retweet count, and like count.
    6. Saves the tweet data to a JSON file named after the hashtag.

    Parameters:
    - request (HttpRequest): The HTTP request object containing data.

    Returns:
    - JsonResponse: A JSON response with the retrieved tweets and status message.

    Example usage:
    ```
    # POST request to retrieve tweets based on hashtags
    # Request body should contain {"hashtags": "your_hashtag"}
    response = fetch_tweets_by_hash_tag(request)
    ```

    Possible errors:
    - If the request data is invalid, returns a JSON response with status code 400 and error details.
    - If there's an error during Twitter authentication, returns a JSON response with status code 400 and an authentication error message.
    - If any required element (e.g., search box, articles) is not found, returns a JSON response with status code 400 and error details.
    """
    serializer = TweetHashtagSerializer(data=request.data)
    hashtags = request.data.get("hashtags")
    if serializer.is_valid():
        driver = initialize_driver()
        success, message = twitterLogin_auth(driver)
        if success:
            try:
                sleep(16)
                search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
                search_box.send_keys(hashtags)
                search_box.send_keys(Keys.ENTER)
                print("Entered the subject and clicked Successfully !!")
                sleep(10)
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'search_box element not found')
            data = []
            try:
                articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
                print('articles Found')
                # pass

            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'articles element not found')
            while True:
                for article in articles:
                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                    tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                    reply = driver.find_element(By.XPATH, f'//*[@data-testid="reply"]').text
                    retweet = driver.find_element(By.XPATH,
                                                  '//button[@data-testid="retweet"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]').text
                    likes = driver.find_element(By.XPATH,
                                                '//button[@data-testid="like"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]').text
                    data.append({
                        "Timestamp": timestamp,
                        "TweetContent": tweet,
                        "Reply": reply,
                        "Retweet": retweet,
                        "Likes": likes
                    })
                    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                    driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
                    if len(data) > 5:
                        break
                break
                # Save data to JSON file
            save_data_in_directory(f"Json_Response/{timezone.now().date()}/",hashtags, data)
            driver.quit()
            return message_json_response(status.HTTP_200_OK, 'success', 'tweet get successfully', data=data)
        return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'Twitter Authentication Failed')
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)


@api_view(["GET"])
def Twiiter_treding_hashtag(request):
    """
    Retrieves trending hashtags from Twitter using Selenium WebDriver.
    This function performs the following steps:
    1. Initializes a Selenium WebDriver instance.
    2. Logs in to Twitter using authentication.
    3. Clicks on the Explore button.
    4. Clicks on the Trending button to view trending topics.
    5. Scrolls down to load more trending topics.
    6. Extracts data from trending topic elements.
    7. Returns a JSON response with trending topics data.
    Parameters:
    - request (HttpRequest): The HTTP request object.
    Returns:
    - JsonResponse: A JSON response with trending hashtags data.

    Example usage:
    ```
    # GET request to retrieve trending hashtags from Twitter
    response = Twitter_trending_hashtag(request)
    ```

    Possible errors:
    - If there's an error during Twitter authentication, returns a JSON response with status code 400 and an authentication error message.
    - If any required element (e.g., explore button, trending topics) is not found, returns a JSON response with status code 400 and error details.
    """
    driver = initialize_driver()
    success, message = twitterLogin_auth(driver)
    if success:
        sleep(16)
        try:
            explore_btn = driver.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div/div[2]/span")
            explore_btn.click()
            print('Explore button found and clicked')
            sleep(5)
        except NoSuchElementException:
            return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'explore  element not found')
        # Click on the Trending button
        try:
            trending_btn = driver.find_element(By.XPATH,
                                               "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span")
            trending_btn.click()
            print('Trending button found and clicked')
            sleep(5)
        except NoSuchElementException:
            return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'treding  element not found')

        # Scroll down to load more trending topics
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)  # Adjust sleep time as needed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Find all trending topic elements
        try:
            trending_topics_elements = driver.find_elements(By.XPATH, '//*[@data-testid="cellInnerDiv"]')
            print('Trending topic elements found')
        except NoSuchElementException:
            return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'trending_topic element not found')
        # Extract data from trending topic elements
        trending_topics = []

        for element in trending_topics_elements:
            text = element.text.split('\n')
            if len(text) >= 4:
                item = {
                    "id": text[0].strip(),
                    "category": text[2].split(' · ')[0].strip(),
                    "type": text[2].split(' · ')[1].strip() if ' · ' in text[2] else "Trending",
                    "trending": text[3].strip(),
                    "posts": text[4].strip() if len(text) > 4 else "N/A"
                }
                trending_topics.append(item)
        # Return JSON response with trending topics data
        save_data_in_directory(f"Json_Response/{timezone.now().date()}/",'trading_data', trending_topics)
        return message_json_response(status.HTTP_200_OK, 'success', 'trending Hashtag here',
                                     data=trending_topics)
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'twitter authentication failed')


@api_view(["POST"])
def get_tweets_by_url(request):
    """
    Retrieves tweet details from URLs specified in the request data.

    This function takes an HTTP request object containing data, validates it using a TweetUrlSerializer, and then initializes a WebDriver using the initialize_driver function. It then extracts the post IDs from the request data and attempts to log in to Twitter using the twitterLogin_auth function.

    If the login is successful, the function iterates through each post ID, visits the corresponding tweet URL, and extracts various details such as tweet content, image URL, reply count, like count, repost count, bookmark count, timestamp, and views count.

    The extracted tweet details are then stored in a list of dictionaries and saved in a directory named with the current date under the 'Json_Response' directory using the save_data_in_directory function.

    Finally, a JSON response containing the extracted tweet details is returned with a success status code (HTTP 200 OK).

    Args:
        request: An HTTP request object containing data.

    Returns:
        A JSON response containing tweet details for the specified URLs.

    Raises:
        NoSuchElementException: If any element on the tweet page is not found.
    """
    serializer = TweetUrlSerializer(data=request.data)
    if serializer.is_valid():
        driver = initialize_driver()
        post_ids = request.data.get('post_ids')
        success, message = twitterLogin_auth(driver)
        if success:
            sleep(16)
        data = []
        for post_id in post_ids:
            twiiter_url = f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            driver.get(twiiter_url)
            sleep(5)

            try:
                # Find tweet elements
                tweet_elements = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'tweet_elements element not found')



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
        save_data_in_directory(f"Json_Response/{timezone.now().date()}/",request.data.get('user_name'), data)
        return message_json_response(status.HTTP_200_OK, 'error', 'tweets get  successFully' ,data=data)
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)


@api_view(["POST"])
def get_comments_for_tweets(request):
    """
    Retrieves comments for tweets identified by their post IDs.

    This function takes an HTTP request object containing data, validates it using a TweetUrlSerializer, and then initializes a WebDriver using the initialize_driver function. It then extracts the post IDs from the request data and attempts to log in to Twitter using the twitterLogin_auth function.

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
        driver = initialize_driver()
        post_ids = request.data.get('post_ids')
        success, message = twitterLogin_auth(driver)
        if success:
            sleep(16)
        data = []

        for post_id in post_ids:
            twiiter_url = f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            driver.get(twiiter_url)
            print("twitter url open")
            sleep(5)
            testid_value = "tweetPhoto"
            try:
                reply = driver.find_element(By.XPATH, f'//*[@data-testid="{testid_value}"]')
                reply.click()
                print("Click the image Successfully")
                sleep(10)
            except NoSuchElementException:
                return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', 'reply element not found')
            test_id = 'tweetText'

            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
                print('last_height')
            except Exception as e:
                return message_json_response(status.HTTP_200_OK, 'success', 'error' ,data={e})
            while True:
                try:
                    elements = driver.find_elements(By.XPATH, f'//*[@data-testid="{test_id}"]')
                    print('elements part mil gya')
                except NoSuchElementException:
                    return message_json_response(status.HTTP_400_BAD_REQUEST, 'success', 'elements components is not found')
                print("while loop k andr aa gya ")
                all_texts = set()  # Use a set to avoid duplicates
                for element in elements:
                    all_texts.add(element.text)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)  # Adjust the sleep time as needed
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                        break
                last_height = new_height
            data.append({
                        "comments": list(all_texts),
                    })
        return message_json_response(status.HTTP_200_OK, 'success', 'tweets get  successFully' ,data=data)
    return message_json_response(status.HTTP_400_BAD_REQUEST, 'error', serializer.errors)
