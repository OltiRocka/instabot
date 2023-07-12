from instascraper import InstaScraperAPI

scraper = InstaScraperAPI()
df = scraper.scrape_data('cats')
df = df.loc[df['media_type']=='image']
df = df.sort_values(by=['likes'])
df = df.head(5)


response = scraper.publish_media(url=df['post_urls'].iloc[1], caption=df['description'].iloc[1], account = 'dailykattos')
print(response)