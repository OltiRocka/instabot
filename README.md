# instabot

This project is a Python-based Instagram scraper and publisher that allows you to scrape Instagram data for specific accounts and post the scraped media on specified Instagram accounts using the Instagram API.

The project is designed to run on AWS Lambda, enabling you to automate the scraping and publishing process. It uses the serverless computing power of AWS Lambda to perform the tasks without the need for managing infrastructure.

## Features

- Scrapes Instagram data from specified accounts and stores it in a Pandas DataFrame.
- Posts the scraped media (images, reels, or carousels) on specified Instagram accounts using the Instagram API.
- Supports multiple content categories, allowing you to scrape and publish media for different niches.
- Configurable through a JSON file that contains account information and content categories.
- Uses the Requests library to make HTTP requests to the Instagram API.
- Uses BeautifulSoup for HTML parsing.

## Prerequisites

- Python 3.7 or higher
- AWS account
- Instagram Business account
- Instagram API access token
- AWS Lambda function setup and configuration

## Installation

1. Clone the repository: ```git clone https://github.com/OltiRocka/instabot.git```
2. Install the required Python packages: ```pip install -r requirements.txt```

3. Set up the Instagram API access token:

- Obtain an access token from the Instagram Developer Platform for your Instagram Business account.
- Create a JSON file named `.json` and add the access token and other account information as shown in the example provided.

    Example `.json` file:
    ```
    {
      "ACCESS_TOKEN": "<your_access_token>",
      "hashtags": {
        "niche_1": "<string_of_hashtags_for_niche_1>",
        "niche_2": "<string_of_hashtags_for_niche_2>"
      },
      "accounts": {
        "niche_1": [
          "instagram_account_id_1",
          "instagram_account_id_2",
          "instagram_account_id_3",
          "instagram_account_id_4"
        ],
        "niche_2": [
          "instagram_account_id_1",
          "instagram_account_id_2",
          "instagram_account_id_3",
          "instagram_account_id_4"
        ]
      },
      "content_types": {
        "niche_1": [
          "existing_acc_1",
          "existing_acc_2",
          "existing_acc_3",
          "existing_acc_4",
          "existing_acc_5",
          "existing_acc_6"
        ],
        "niche_2": [
          "existing_acc_1",
          "existing_acc_2",
          "existing_acc_3",
          "existing_acc_4",
          "existing_acc_5",
          "existing_acc_6"
        ]
      }
    }
    ```

4. Configure the AWS Lambda function:

- Set up an AWS Lambda function and configure it with the necessary permissions.
- Configure the AWS Lambda function to trigger the scraping and publishing process at the desired interval (e.g., once per day).
- Set environment variables for the Instagram API access token and other required configurations.

5. Deploy the code to AWS Lambda:

- Package the code and dependencies into a ZIP file.
- Upload the ZIP file to the AWS Lambda function.

## Usage

1. Update the `.json` file with the desired Instagram accounts and content categories to scrape and publish.

2. Test the scraper functionality locally by running the following command: ```python instascraper.py```

3. Set up the AWS Lambda function to run the script automatically at the desired interval.

4. Monitor the AWS Lambda function logs to check the scraping and publishing process.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.



