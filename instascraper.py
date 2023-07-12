import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv, find_dotenv


class InstaScraperAPI:
    """
    A class used to scrape data from Instagram profiles and post it on given Instagram Accounts.

    Attributes
    ----------
    post_df : pd.DataFrame
        a DataFrame that stores the scraped Instagram posts data
    base_url : str
        the base URL for the Instagram API endpoint
    headers : dict
        the headers to be used in API requests

    Methods
    -------
    scrape_data(usernames: list) -> pd.DataFrame:
        Scrape Instagram data for a list of usernames
    publish_media(url: str, caption: str, account: str) -> str:
        Publishes the scraped media on the Facebook account
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the DataScraper object.
        """
        self.post_df = pd.DataFrame()
        self.base_url = "https://instastories.watch/api/profile/v3"
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.headers = self.get_headers()
        self.load_accounts()

    def load_accounts(self):
        with open(".json", "r") as file:
            self.accounts = json.load(file)

    @staticmethod
    def get_headers():
        """
        Returns the headers for HTTP requests.

        Returns
        -------
        dict
            headers for HTTP requests
        """
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "instastories.watch",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        }

    def scrape_data(self, content_category):
        """
        Scrape Instagram data for accounts of a specific content category.

        Parameters
        ----------
        content_category : str
            content category to scrape data from associated Instagram accounts

        Returns
        -------
        pd.DataFrame
            DataFrame with scraped data
        str
            content category
        """
        usernames = self.accounts["content_types"][content_category]
        for username in usernames:
            # Send request to search for the username
            response = self.send_request(f"{self.base_url}/search?username={username}")
            user_info = self.send_request(f"{self.base_url}/info?username={username}")
            posts_info = self.send_request(
                f"{self.base_url}/publications?nextMaxId=&username={username}"
            )

            items = json.loads(posts_info.text)["items"]
            posts = [i for i in items if "medias" in i.keys()]

            data = self.extract_data(
                posts, username, json.loads(user_info.text)["subscriber"]
            )

            # Concatenate the data to the post_df DataFrame
            self.post_df = pd.concat([self.post_df, pd.DataFrame(data)]).reset_index(
                drop=True
            )

        self.post_df["media_type"] = self.post_df["post_urls"].apply(
            lambda url: "video" if ".mp4" in url else "image"
        )

        return self.post_df, content_category

    def send_request(self, url):
        """
        Sends a GET request to the specified URL.

        Parameters
        ----------
        url : str
            URL to send the GET request to

        Returns
        -------
        requests.Response
            Response object
        """
        return requests.get(url, headers=self.headers)

    @staticmethod
    def extract_data(posts, username, subscriber):
        """
        Extracts relevant data from the posts.

        Parameters
        ----------
        posts : list
            list of posts
        username : str
            Instagram username
        subscriber : int
            number of subscribers

        Returns
        -------
        dict
            a dictionary with the extracted data
        """
        post_urls = [post["medias"][0]["originalUrl"] for post in posts]
        likes = [int(post["likes"]) for post in posts]
        descriptions = [
            "\n".join(
                [row for row in post.get("text", "").split("\n") if "@" not in row]
            )
            for post in posts
        ]

        data = {
            "username": [username] * len(post_urls),
            "followers": [subscriber] * len(post_urls),
            "post_urls": post_urls,
            "likes": likes,
            "description": descriptions,
        }

        return data

    def publish_media(self, url, caption, account):
        """
        Publishes the scraped media on the Facebook account.

        Parameters
        ----------
        url : str
            URL of the media to publish
        caption : str
            caption for the media
        account : str
            ID of the Facebook account

        Returns
        -------
        str
            success message or error message
        """

        payload = {
            "image_url": url,
            "caption": caption,
            "access_token": self.access_token,
        }
        url = f"https://graph.facebook.com/v17.0/{str(account)}/media"
        url_publish = f"https://graph.facebook.com/v17.0/{str(account)}/media_publish"
        response = self.send_post_request(url, payload)

        if response.status_code == 200:
            creation_id = json.loads(response.text)["id"]
            payload_publish = {
                "access_token": self.access_token,
                "creation_id": creation_id,
            }
            response_publish = self.send_post_request(url_publish, payload_publish)

            return (
                "Success"
                if response_publish.status_code == 200
                else "Problem while Publishing"
            )
        else:
            return "Problem while Saving"

    def send_post_request(self, url, payload):
        """
        Sends a POST request to the specified URL.

        Parameters
        ----------
        url : str
            URL to send the POST request to
        payload : dict
            data to send in the body of the request

        Returns
        -------
        requests.Response
            Response object
        """
        return requests.post(url=url, data=payload)
