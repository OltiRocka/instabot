import json
import pandas as pd
import requests
import random
import json
import praw

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
        self.load_accounts()
        self.access_token = self.accounts["ACCESS_TOKEN"]
        self.reddit = praw.Reddit(
    client_id='A3Y57PNmwv6t1xp4-taihQ',
    client_secret='GFOJDT1N_qcV30ADaywdWMUiqFq_KQ',
    user_agent='Rocka-DEV'
)
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
        # Retrieve the specified subreddit
        subreddit = self.reddit.subreddit(content_category)
        # Retrieve the top posts from the subreddit
        top_posts = subreddit.top(limit=100)
        # Select a random post from the top posts
        posts = list(top_posts)
        for post in posts:
            if post.is_video:
                url = [post.media['reddit_video']['fallback_url']]
                description = (
                        str(post.title)
                        + "\n.\n.\n.\n"
                        + self.accounts["hashtags"][content_category]
                    )
                media_type = "reel"
            else:
                url = [post.url]
                description = (
                        str(post.title)
                        + "\n.\n.\n.\n"
                        + self.accounts["hashtags"][content_category]
                    )
                media_type = "image"
               
            self.post_df = pd.concat(
                    [
                        self.post_df,
                        pd.DataFrame(
                            {
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
