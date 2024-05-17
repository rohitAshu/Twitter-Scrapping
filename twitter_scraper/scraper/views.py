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
                    "type": "error",
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
                driver.get(f'https://twitter.com/search?q=%23{hashtags}&src=typed_query')
                sleep(3)

                # Scraping tweets
                data = []
                tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")
                for tweet in tweets:
                    user_tag = tweet.find_element(By.XPATH,
                                                  ".//span[contains(@class, 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')]").text
                    timestamp = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    tweet_content = tweet.find_element(By.XPATH,
                                                       ".//div[contains(@class, 'css-901oao r-18jsvk2 r-1tl8opc r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')]").text
                    reply = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']").text
                    retweet = tweet.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
                    data.append({
                        "UserTag": user_tag,
                        "Timestamp": timestamp,
                        "TweetContent": tweet_content,
                        "Reply": reply,
                        "Retweet": retweet
                    })

                # Save data to JSON file
                with open(f"{hashtags}_tweets.json", "w", encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return JsonResponse(
                    {
                        "code": status.HTTP_200_OK,
                        "type": "success",
                        "message": "Get tweets via this hashtag",
                        "data": data
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                print(f"Error scraping Twitter data: {e}")
                return False
            finally:
                if driver:
                    driver.quit()

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
