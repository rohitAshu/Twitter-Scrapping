# import json

# from django.test import TestCase, Client
# from rest_framework import status


# def setup():
#     def setUp(self):
#         self.client = Client()


# class GetTweetsTestCase(TestCase):
#     setup()

#     def test_get_tweets_success(self):
#         print("Enter in test case ========================================")
#         # Define a sample profile name
#         profile_name = "Modi"
#         print(profile_name)

#         # Define a sample request data
#         request_data = {"Profile_name": profile_name}

#         # Send a POST request to the API endpoint
#         response = self.client.post("/twitter/api/v1/get-profile/", data=request_data)

#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected message and data
#         self.assertEqual(response.json()["type"], "success")
#         self.assertEqual(response.json()["message"], "Tweets get  SuccessFully ")

#         # Check if the response data is not empty
#         self.assertTrue(response.json()["data"])
#         print(
#             "get profile---------------------------pass"
#         )

#     def test_invalid_input(self):
#         # Define invalid request data (missing Profile_name)
#         invalid_request_data = {}

#         # Send a POST request with invalid data
#         response = self.client.post(
#             "/twitter/api/v1/get-profile/", data=invalid_request_data
#         )

#         # Check if the response status code is 400 (Bad Request)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Check if the response contains the expected error message
#         self.assertEqual(response.json()["type"], "error")
#         self.assertIn(
#             "Profile_name", response.json()["message"]
#         )  # Assuming serializer error messages include field names
#         print(
#             "-------------------------------------------fail"
#         )


# class FetchTweetsByHashtagTestCase(TestCase):
#     setup()

#     def test_fetch_tweets_success(self):
#         # Define a sample hashtag
#         hashtag = "#PakistanBackstabsRussia"

#         # Define a sample request data
#         request_data = {"hashtags": hashtag}

#         # Send a POST request to the API endpoint
#         response = self.client.post(
#             "/twitter/api/v1/get-tweet-hashtag/", data=request_data
#         )

#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected message and data
#         self.assertEqual(response.json()["type"], "success")
#         self.assertEqual(response.json()["message"], "tweet get Successfully")

#         # Check if the response data is not empty
#         self.assertTrue(response.json()["data"])
#         print(
#             "get tweet by hashtag-----------------------------------pass"
#         )

#     def test_invalid_input(self):
#         # Define invalid request data (missing hashtags)
#         invalid_request_data = {}

#         # Send a POST request with invalid data
#         response = self.client.post(
#             "/twitter/api/v1/get-tweet-hashtag/", data=invalid_request_data
#         )

#         # Check if the response status code is 400 (Bad Request)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Check if the response contains the expected error message
#         self.assertEqual(response.json()["type"], "error")
#         self.assertIn(
#             "hashtags", response.json()["message"]
#         )  # Assuming serializer error messages include field names
#         print(
#             "get tweet by hashtag-----------------------------------fail"
#         )


# class TwitterTrendingHashtagTestCase(TestCase):
#     setup()

#     def test_get_trending_hashtags_success(self):
#         # Send a GET request to the API endpoint
#         response = self.client.get("/twitter/api/v1/get-trending-hashtag/")

#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected message and data
#         self.assertEqual(response.json()["type"], "success")
#         self.assertEqual(response.json()["message"], "Trending Hashtag here")

#         # Check if the response data is not empty
#         self.assertTrue(response.json()["data"])
#         print(
#             "get trending hashtag-------------------------------------pass"
#         )


# class GetTweetsByIdTestCase(TestCase):
#     setup()

#     def test_get_tweets_success(self):
#         # Define a sample request data
#         request_data = {
#             "user_name": "narendramodi",
#             "post_ids": [1793170649688514579, 1792644927052001747],
#         }

#         # Send a POST request to the API endpoint with JSON data
#         response = self.client.post(
#             "/twitter/api/v1/get-tweets-by-id/",
#             data=json.dumps(request_data),
#             content_type="application/json",
#         )

#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected message and data
#         self.assertEqual(response.json()["type"], "error")
#         self.assertEqual(response.json()["message"], "tweets get  successFully")

#         # Check if the response data is not empty
#         self.assertTrue(response.json()["data"])
#         print(
#             "get tweet by id-----------------------------------------pass"
#         )

#     def test_invalid_input(self):
#         # Define invalid request data (missing user_name)
#         invalid_request_data = {"post_ids": [123456, 789012]}

#         # Send a POST request with invalid data
#         response = self.client.post(
#             "/twitter/api/v1/get-tweets-by-id/", data=invalid_request_data
#         )

#         # Check if the response status code is 400 (Bad Request)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Check if the response contains the expected error message
#         self.assertEqual(response.json()["type"], "error")
#         self.assertIn(
#             "user_name", response.json()["message"]
#         )  # Assuming serializer error messages include field names
#         print(
#             "get tweet by id----------------------------------fail"
#         )


# class GetCommentsForTweetsTestCase(TestCase):
#     setup()

#     def test_get_comments_success(self):
#         # Define a sample request data
#         request_data = {
#             "user_name": "narendramodi",
#             "post_ids": [1793170649688514579, 1792644927052001747],
#         }

#         # Send a POST request to the API endpoint
#         response = self.client.post(
#             "/twitter/api/v1/get-comments-for-tweet/",
#             data=json.dumps(request_data),
#             content_type="application/json",
#         )

#         # Check if the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected message and data
#         self.assertEqual(response.json()["type"], "success")
#         self.assertEqual(response.json()["message"], "tweets get successfully")

#         # Check if the response data is not empty
#         self.assertTrue(response.json()["data"])
#         print("Get comments for tweets - success case passed")
#         print(
#             "get comment by id-----------------------------------pass"
#         )

#     def test_invalid_input(self):
#         # Define invalid request data (missing user_name and post_ids)
#         invalid_request_data = {}

#         # Send a POST request with invalid data
#         response = self.client.post(
#             "/twitter/api/v1/get-comments-for-tweet/",
#             data=json.dumps(invalid_request_data),
#             content_type="application/json",
#         )

#         # Check if the response status code is 400 (Bad Request)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Check if the response contains the expected error message
#         self.assertEqual(response.json()["type"], "error")
#         self.assertIn("user_name", response.json()["message"])
#         self.assertIn("post_ids", response.json()["message"])
#         print("Get comments for tweets - invalid input case passed")
#         print(
#             "get comment by id-----------------------------------fail"
#         )
