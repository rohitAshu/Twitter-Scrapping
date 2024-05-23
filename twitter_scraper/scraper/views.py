import os
from django.utils import timezone
from .web_driver import initialize_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # type: ignore
from time import sleep
from .utils import (
    twitterLogin_auth,
    message_json_response,
    save_data_in_directory,
    type_slowly,
)
from .serializers import (
    TwitterProfileSerializer,
    TweetHashtagSerializer,
    TweetUrlSerializer,
)
import json
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from selenium.webdriver.common.action_chains import ActionChains


@api_view(["POST"])
def get_tweeted_via_profile_name(request):
    """
    Fetches tweets from a Twitter profile given its name.

    Args:
        request: HTTP request object containing data.

    Returns:
        JSON response containing tweets data if successful,
        otherwise returns an error response.

    Raises:
        None
    """
    serializer = TwitterProfileSerializer(data=request.data)
    profile_name = request.data.get("Profile_name")
    if serializer.is_valid():
        driver = initialize_driver()
        success = twitterLogin_auth(driver)

        if success:
            sleep(16)
            try:
                search_box = driver.find_element(
                    By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"
                )
                action = ActionChains(driver)
                action.move_to_element(search_box).click().perform()
                for char in profile_name:
                    action.send_keys(char).perform()
                    sleep(0.1)  # Adjust delay as needed
                search_box.send_keys(Keys.ENTER)
                sleep(5)

            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "search_box Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                people = driver.find_element(
                    By.XPATH,
                    "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span",
                )
                people.click()
                sleep(5)
                print("Clicked on people Successfully !!")
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "people Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                profile = driver.find_element(
                    By.XPATH,
                    "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]",
                )
                profile.click()
                sleep(7)
                print("Went on profile ")
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "profile Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = []
            try:
                articles = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "articles Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            while True:
                for article in articles:
                    user_tag = driver.find_element(
                        By.XPATH,
                        "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]",
                    ).text

                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute(
                        "datetime"
                    )
                    tweet = driver.find_element(
                        By.XPATH, "//div[@data-testid='tweetText']"
                    ).text
                    testid_value = "reply"
                    reply = driver.find_element(
                        By.XPATH, f'//*[@data-testid="{testid_value}"]'
                    ).text
                    retweet = driver.find_element(
                        By.XPATH,
                        '//button[@data-testid="retweet"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]',
                    ).text
                    likes = driver.find_element(
                        By.XPATH,
                        '//button[@data-testid="like"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]',
                    ).text
                    data.append(
                        {
                            "Name": profile_name,
                            "UserTag": user_tag,
                            "Timestamp": timestamp,
                            "TweetContent": tweet,
                            "Reply": reply,
                            "Retweet": retweet,
                            "Likes": likes,
                        }
                    )

                    driver.execute_script(
                        "window.scrollTo(0,document.body.scrollHeight);"
                    )
                    if len(data) > 5:
                        break
                break
                # Save data to JSON file
            directory = "Json_Response"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Define the file path
            file_path = os.path.join(directory, f"{profile_name}.json")

            # Save the JSON data to the specified folder
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return JsonResponse(
                {
                    "code": status.HTTP_200_OK,
                    "type": "success",
                    "message": "Tweets get  SuccessFully ",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            {
                "code": status.HTTP_400_BAD_REQUEST,
                "type": "error",
                "message": "Twitter Authentication Error",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return JsonResponse(
        {
            "code": status.HTTP_400_BAD_REQUEST,
            "type": "error",
            "message": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def fetch_tweets_by_hash_tag(request):
    serializer = TweetHashtagSerializer(data=request.data)
    hashtags = request.data.get("hashtags")
    if serializer.is_valid():
        driver = initialize_driver()
        success = twitterLogin_auth(driver)
        if success:
            try:
                sleep(16)
                search_box = driver.find_element(
                    By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"
                )
                actions = ActionChains(driver)
                actions.move_to_element(search_box).click().perform()
                type_slowly(search_box, hashtags)
                search_box.send_keys(Keys.ENTER)
                print("Entered the subject and clicked Successfully!")
                sleep(10)
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "search_box Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = []
            try:
                articles = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
                print("articles Found")
                # pass

            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": "articles Element not found",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            while True:
                for article in articles:
                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute(
                        "datetime"
                    )
                    tweet = driver.find_element(
                        By.XPATH, "//div[@data-testid='tweetText']"
                    ).text
                    testid_value = "reply"
                    reply = driver.find_element(
                        By.XPATH, f'//*[@data-testid="{testid_value}"]'
                    ).text
                    retweet = driver.find_element(
                        By.XPATH,
                        '//button[@data-testid="retweet"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]',
                    ).text
                    likes = driver.find_element(
                        By.XPATH,
                        '//button[@data-testid="like"]//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3" and @style="text-overflow: unset;"]',
                    ).text
                    data.append(
                        {
                            "Timestamp": timestamp,
                            "TweetContent": tweet,
                            "Reply": reply,
                            "Retweet": retweet,
                            "Likes": likes,
                        }
                    )

                    driver.execute_script(
                        "window.scrollTo(0,document.body.scrollHeight);"
                    )
                    articles = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
                    if len(data) > 5:
                        break
                break
                # Save data to JSON file
            directory = "Json_Response"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Define the file path
            file_path = os.path.join(directory, f"{hashtags}.json")

            # Save the JSON data to the specified folder
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            driver.quit()
            # return True
            return JsonResponse(
                {
                    "code": status.HTTP_200_OK,
                    "type": "success",
                    "message": "tweet get Successfully",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )

        return JsonResponse(
            {
                "code": status.HTTP_400_BAD_REQUEST,
                "type": "error",
                "message": "Twitter Authentication Failed",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(
        {
            "code": status.HTTP_400_BAD_REQUEST,
            "type": "error",
            "message": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
def twiiter_treding_hashtag(request):
    """
    Fetches the trending hashtags from Twitter.

    This function initializes a WebDriver session, performs Twitter login authentication,
    clicks on the Explore and Trending buttons, scrolls down to load more trending topics,
    extracts data from the trending topic elements, and returns a JSON response with the trending topics.

    Returns:
        JsonResponse: A JSON response containing the trending hashtags.
    """
    driver = initialize_driver()
    success = twitterLogin_auth(driver)
    if success:
        sleep(16)  # Assuming this sleep is needed for Twitter to load properly

        # Click on the Explore button
        try:
            explore_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/"
                "div[2]/nav/a[2]/div/div[2]/span",
            )
            explore_btn.click()
            print("Explore button found and clicked")
            sleep(5)
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": "Explore button not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Click on the Trending button
        try:
            trending_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/"
                "div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span",
            )
            trending_btn.click()
            print("Trending button found and clicked")
            sleep(5)
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": "Trending button not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
            trending_topics_elements = driver.find_elements(
                By.XPATH, '//*[@data-testid="cellInnerDiv"]'
            )
            print("Trending topic elements found")
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": "Trending topic elements not found",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract data from trending topic elements
        trending_topics = []

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

                directory = "Json_Response"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Define the file path
                file_path = os.path.join(directory, "trending_hashtag.json")

                # Save the JSON data to the specified folder
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(item, f, ensure_ascii=False, indent=4)
        # Return JSON response with trending topics data
        return JsonResponse(
            {
                "code": status.HTTP_200_OK,
                "type": "success",
                "message": "Trending Hashtag here",
                "data": trending_topics,
            },
            status=status.HTTP_200_OK,
            json_dumps_params={"indent": 2},
        )

    return JsonResponse(
        {
            "code": status.HTTP_400_BAD_REQUEST,
            "type": "error",
            "message": "Twitter Authentication Failed",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def get_tweets_by_id(request):
    serializer = TweetUrlSerializer(data=request.data)

    if serializer.is_valid():
        driver = initialize_driver()
        post_ids = request.data.get("post_ids")
        success = twitterLogin_auth(driver)
        if success:
            sleep(16)
        data = []
        for post_id in post_ids:
            twiiter_url = (
                f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            )
            driver.get(twiiter_url)
            sleep(5)
            try:
                # Find tweet elements
                tweet_elements = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
            except NoSuchElementException:
                return message_json_response(
                    status.HTTP_400_BAD_REQUEST,
                    "error",
                    "tweet_elements element not found",
                )

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
                driver.find_element(By.CSS_SELECTOR, 'button[data-testid="retweet"]')
                .find_element(
                    By.CSS_SELECTOR,
                    'span[data-testid="app-text-transition-container"] span',
                )
                .text
            )
            bookmark_count = (
                driver.find_element(By.CSS_SELECTOR, 'button[data-testid="bookmark"]')
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
            views_count = driver.find_element(By.CSS_SELECTOR, "span.css-1jxf684").text
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
        save_data_in_directory(
            f"Json_Response/{timezone.now().date()}/",
            request.data.get("user_name"),
            data,
        )
        return message_json_response(
            status.HTTP_200_OK, "error", "tweets get  successFully", data=data
        )
    return message_json_response(
        status.HTTP_400_BAD_REQUEST, "error", serializer.errors
    )


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
        post_ids = request.data.get("post_ids")
        success, message = twitterLogin_auth(driver)
        if success:
            sleep(16)
        data = []

        for post_id in post_ids:
            twiiter_url = (
                f"https://x.com/{request.data.get('user_name')}/status/{post_id}"
            )
            driver.get(twiiter_url)
            sleep(5)
            testid_value = "tweetPhoto"
            try:
                reply = driver.find_element(
                    By.XPATH, f'//*[@data-testid="{testid_value}"]'
                )
                reply.click()
                sleep(10)
            except NoSuchElementException:
                return message_json_response(
                    status.HTTP_400_BAD_REQUEST, "error", "reply element not found"
                )

            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
            except Exception as e:
                return message_json_response(
                    status.HTTP_200_OK, "success", "error", data={e}
                )
            while True:
                try:
                    elements = driver.find_elements(
                        By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']"
                    )
                except NoSuchElementException:
                    return message_json_response(
                        status.HTTP_400_BAD_REQUEST,
                        "success",
                        "elements components is not found",
                    )
                all_texts = set()  # Use a set to avoid duplicates
                for element in elements:
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    all_texts.add(element.text)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)  # Adjust the sleep time as needed
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            data.append(
                {
                    "comments": list(all_texts),
                }
            )
        return message_json_response(
            status.HTTP_200_OK, "success", "tweets get successFully", data=data
        )
    return message_json_response(
        status.HTTP_400_BAD_REQUEST, "error", serializer.errors
    )
