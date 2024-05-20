from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .web_driver import initialize_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # type: ignore
from time import sleep
from rest_framework import status
from .utils import twitterLogin_auth
from .serializers import TwitterProfileSerializers,TweetHashtagSerializer
import json


@api_view(["POST"])
def get_Tweeted_via_profile_name(request):
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
    serializer = TwitterProfileSerializers(data=request.data)
    profile_name = request.data.get("Profile_name")
    if serializer.is_valid():
        driver = initialize_driver()
        success, message = twitterLogin_auth(driver)

        if success:
            sleep(16)
            try:
                search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
                search_box.send_keys(profile_name)
                search_box.send_keys(Keys.ENTER)
                print("Entered the subject and clicked Successfully !!")
                sleep(3)
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'search_box Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                people = driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span")
                people.click()
                sleep(5)
                print("Clicked on people Successfully !!")
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'people Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                profile = driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]")
                profile.click()
                sleep(5)
                print("Went on profile Man ")
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'profile Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = []
            try:
                articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'articles Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            while True:
                for article in articles:
                    user_tag = driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[2]").text

                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                    tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                    reply = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
                    retweet = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
                    data.append({
                        "Name": profile_name,
                        "UserTag": user_tag,
                        "Timestamp": timestamp,
                        "TweetContent": tweet,
                        "Reply": reply,
                        "Retweet": retweet
                    })

                    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                    if len(data) > 5:
                        break
                break
                # Save data to JSON file
            with open(f"{profile_name}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return JsonResponse(
                {
                    "code": status.HTTP_200_OK,
                    "type": "success",
                    "message": 'Tweets get  SuccessFully ',
                    "data": data
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
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'search_box Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = []
            try:
                articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
                print('articles Found')
                # pass

            except NoSuchElementException:
                return JsonResponse(
                    {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "type": "error",
                        "message": 'articles Element not found',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            while True:
                for article in articles:
                    timestamp = driver.find_element(By.XPATH, "//time").get_attribute('datetime')
                    tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
                    reply = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
                    retweet = driver.find_element(By.CLASS_NAME, "css-1jxf684").text
                    data.append({
                        "Name": hashtags,
                        "Timestamp": timestamp,
                        "TweetContent": tweet,
                        "Reply": reply,
                        "Retweet": retweet
                    })
                    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                    articles = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
                    if len(data) > 5:
                        break
                break
                # Save data to JSON file
            with open(f"{hashtags}.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            driver.quit()
            # return True
            return JsonResponse(
                {
                    "code": status.HTTP_200_OK,
                    "type": "success",
                    "message": 'tweet get Successfully',
                    "data": data
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
def Twiiter_treding_hashtag():
    """
    Fetches the trending hashtags from Twitter.

    This function initializes a WebDriver session, performs Twitter login authentication,
    clicks on the Explore and Trending buttons, scrolls down to load more trending topics,
    extracts data from the trending topic elements, and returns a JSON response with the trending topics.

    Returns:
        JsonResponse: A JSON response containing the trending hashtags.
    """
    driver = initialize_driver()
    success, message = twitterLogin_auth(driver)
    if success:
        sleep(16)  # Assuming this sleep is needed for Twitter to load properly

        # Click on the Explore button
        try:
            explore_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div/div[2]/span")
            explore_btn.click()
            print('Explore button found and clicked')
            sleep(5)
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": 'Explore button not found',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Click on the Trending button
        try:
            trending_btn = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span")
            trending_btn.click()
            print('Trending button found and clicked')
            sleep(5)
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": 'Trending button not found',
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
            trending_topics_elements = driver.find_elements(By.XPATH, '//*[@data-testid="cellInnerDiv"]')
            print('Trending topic elements found')
        except NoSuchElementException:
            return JsonResponse(
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "type": "error",
                    "message": 'Trending topic elements not found',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        return JsonResponse(
            {
                "code": status.HTTP_200_OK,
                "type": "success",
                "message": "Trading Hashtag here",
                "data": trending_topics
            },
            status=status.HTTP_200_OK,
            json_dumps_params={'indent': 2}
        )

    return JsonResponse(
        {
            "code": status.HTTP_400_BAD_REQUEST,
            "type": "error",
            "message": "Twitter Authentication Failed",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


