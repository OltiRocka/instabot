# Instagram Bot

InstaScraperAPI is a Python library that allows you to scrape data from Instagram profiles and publish it on given Instagram accounts. It provides a convenient way to gather Instagram posts from specific subreddits using the Reddit API (PRAW) and publish them on Instagram accounts associated with those subreddits. This README will guide you on how to install and use the library effectively.
## Installation

1. Clone the repository:

```git clone https://github.com/your_username/InstaScraperAPI.git```

2. Install the required dependencies by running the following command in the project directory:

```pip install -r requirements.txt```

3. Set up the JSON configuration file:
- Create a file named `.json` in the project directory.
- Add your Instagram access token and other account details following the structure provided in the `.json` section below.

The JSON configuration file (config.json) contains the necessary account details for the library to work. Here's an example structure:

## json
```
{
  "ACCESS_TOKEN": "<your_meta_access_token>",
  "hashtags": {
    "subreddit_1": "<all_hashtags>",
    "subreddit_2": "<all_hashtags>"
  },
  "accounts": {
    "subreddit_1": [
      "<instagram_acc_id_1>",
      "<instagram_acc_id_2>",
      "<instagram_acc_id_3>",
      "<instagram_acc_id_4>"
    ],
    "subreddit_2": [
      "<instagram_acc_id_1>",
      "<instagram_acc_id_2>",
      "<instagram_acc_id_3>",
      "<instagram_acc_id_4>"
    ]
  }
}
```
    "ACCESS_TOKEN": Your Instagram access token.
    "hashtags": Contains the hashtags associated with each content category.
    "accounts": Specifies the Instagram accounts associated with each content category.

Make sure to update the JSON configuration file with your own account details.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create a new issue on the GitHub repository.
License

This project is licensed under the MIT License. Feel free to use and modify the code according to your needs.
