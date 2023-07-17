import json
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
import json
import time

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
        self.base_url = "https://instagram.com/"
        self.load_accounts()
        self.access_token = self.accounts["ACCESS_TOKEN"]
    def load_accounts(self):
        with open(".json", "r") as file:
            self.accounts = json.load(file)


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
        headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-CSRFToken": "PqnjxscfstkbqJqsHYm4SKh2IOJRFk4A",
    "X-IG-App-ID": "936619743392459",
    "X-ASBD-ID": "129477",
    "X-IG-WWW-Claim": "hmac.AR36pw8gkrJL1t4a4yCx7va4l8BRr8VegR7PPI6Omn9kgZt9",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://www.instagram.com/cats.virals/",
    "Cookie": "ig_did=129496B2-ABDB-4A34-BAEB-3041BF863C59; datr=Nk-DZG7I1Kk73kw02xF-g-mL; mid=ZINPNwAEAAGQ_vVhNDlhSu0SEDXP; ig_nrcb=1; shbid='5477\05459706249455\0541721119822:01f7e0a9e67c945ca92aaba598106390614a42754346588d103365796985c81ef5cf4ba8'; shbts='1689583822\05459706249455\0541721119822:01f7a265f3a61585f8a5562013ea108410a59bea3cb808697d041cbc49b90f35bd7e8464'; csrftoken=PqnjxscfstkbqJqsHYm4SKh2IOJRFk4A; ds_user_id=59706249455; sessionid=59706249455%3AjEQIZq2QRL3VtT%3A11%3AAYcJt6vF64OJIcg8pF0UUqzIcsrKujpOP9kBbvpJhQ; rur='RVA\05459706249455\0541721138543:01f7e5bbe632e90fa25b826f9157d76a79ab7e902252863cd04eb3f7831cd3cc3d9a65f5'",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}
        usernames = self.accounts["content_types"][content_category]
        for username in usernames:
            # Send request to search for the username
            session = requests.Session()
            response = session.get(f"{self.base_url}{username}", headers = headers)
            print(f"{self.base_url}{username}")
            soup = BeautifulSoup(str(response.text), "html.parser")
            try:
                data = json.loads(soup.find_all("script")[0].text)
            except Exception as e:
                print(e)
                print(soup)
            
            for post in data[1]["itemListElement"]:
                if len(post["video"]) >= 1:
                    url = [post["video"][0]["contentUrl"]]
                    description = (
                        post["articleBody"]
                        + "\n.\n.\n.\n"
                        + self.accounts["hashtags"][content_category]
                    )
                    media_type = "reel"
                elif len(post["image"]) == 1:
                    url = [post["image"][0]["url"]]
                    description = (
                        post["articleBody"]
                        + "\n.\n.\n.\n"
                        + self.accounts["hashtags"][content_category]
                    )
                    media_type = "image"
                else:
                    url = [image["url"] for image in post["image"]]
                    description = (
                        post["articleBody"].split("\n")[0]
                        + "\n.\n.\n.\n"
                        + self.accounts["hashtags"][content_category]
                    )
                    media_type = "carousel"
                self.post_df = pd.concat(
                    [
                        self.post_df,
                        pd.DataFrame(
                            {
                                "username": [username],
                                "url": [url],
                                "description": [description],
                                "media_type": [media_type],
                                'niche':[content_category]
                            }
                        ),
                    ]
                )
        return self.post_df

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
        return requests.get(url, timeout=30, headers = self.headers)

    def publish_media(self, url, caption, account, media_type):
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
        if media_type == "image":
            payload = {
                "image_url": url[0],
                "caption": caption,
                "access_token": self.access_token,
            }
        elif media_type == "reel":
            payload = {
                "video_url": url[0],
                "caption": caption,
                "access_token": self.access_token,
                "media_type": "REELS",
            }
        elif media_type == "carousel":
            item_container_ids = []
            for media_url in url:
                create_item_container_url = (
                    f"https://graph.facebook.com/v17.0/{str(account)}/media"
                )
                create_item_container_params = {
                    "access_token": self.access_token,
                    "image_url": media_url,
                    "is_carousel_item": "true",
                }
                create_item_container_response = requests.post(
                    create_item_container_url, params=create_item_container_params
                )
                create_item_container_data = create_item_container_response.json()
                item_container_id = create_item_container_data.get("id")

                item_container_ids.append(item_container_id)

            payload = {
                "children": ",".join(item_container_ids),
                "caption": caption,
                "access_token": self.access_token,
                "media_type": "CAROUSEL",
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
            if media_type == "reel":
                time.sleep(20)
            response_publish = self.send_post_request(url_publish, payload_publish)
            return (
                "Success"
                if response_publish.status_code == 200
                else f"Problem while Publishing: {response.text}"
            )
        else:
            return f"Problem while Saving : {response.text}"

    def send_post_request(self, url, payload):
        """
        Sends a POST re quest to the specified URL.

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

    def reset_df(self):
        self.post_df = pd.DataFrame()


def main(event, context):
    scraper = InstaScraperAPI()
    for niche in list(scraper.accounts["accounts"].keys()):
        df = scraper.scrape_data(niche)
        time.sleep(10)
        
    df.reset_index(inplace=True)
    for niche in list(scraper.accounts["accounts"].keys()):
        df_content = df.loc[df['niche']==niche]
        df_content.reset_index(inplace=True)
        for account in list(scraper.accounts["accounts"][niche]):
            random_index = random.choice(df_content.index)
            response = scraper.publish_media(
                url=df_content["url"].iloc[random_index],
                caption=df_content["description"].iloc[random_index],
                account=account,
                media_type=df_content["media_type"].iloc[random_index],
            )
            print(response)
main(1,2)
