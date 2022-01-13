import tweepy
import asyncio
import platform
from read_settings import read_settings
from webhook import send_webhook

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class TwitterMonitor:
    def __init__(self):
        self.settings_data = read_settings()
        self.user_accounts = {  # edit account inside dict
            "niewiemczego": None, 
            "sajm0neq": None
        }

    async def account_data(self, account_name: str):
        try:
            auth = tweepy.OAuthHandler(consumer_key=self.settings_data["Settings"]["consumer_key"], consumer_secret=self.settings_data["Settings"]["consumer_secret"])
            auth.set_access_token(key=self.settings_data["Settings"]["access_token"], secret=self.settings_data["Settings"]["access_token_secret"])
            api = tweepy.API(auth)
            public_tweets = api.user_timeline(screen_name=account_name, tweet_mode="extended", exclude_replies="true")

            if len(public_tweets) > 0:
                data = {}
                data["tweet_id"] = public_tweets[0].id
                data["tweet_text"] = public_tweets[0].full_text
                data["username"] = public_tweets[0].user.name
                data["user_screen_name"] = public_tweets[0].user.screen_name
                data["user_description"] = public_tweets[0].user.description
                data["user_profile_image_url_https"] = public_tweets[0].user.profile_image_url_https
                data["user_followers_count"] = public_tweets[0].user.followers_count
                data["user_friends_count"] = public_tweets[0].user.friends_count

                if self.user_accounts[account_name] != None:
                    if self.user_accounts[account_name] != data["tweet_id"]:
                        self.user_accounts[account_name] = data["tweet_id"]
                        return data
                    return None
                self.user_accounts[account_name] = data["tweet_id"]
                return None
            return None
        except tweepy.errors.TooManyRequests:
            print("Rate limit exceeded!")
            await asyncio.sleep(15*60)  # sleeping for 15 minutes
            return None

    async def monitor_twitter(self):
        while 1:
            for index, account in enumerate(self.user_accounts.items()):
                new_tweet = await self.account_data(account[0])
                if new_tweet != None:
                    send_webhook(self.settings_data["Settings"]["webhook_url"], new_tweet)
                await asyncio.sleep(1.1)  # sleeping for 1.1 sec to avoid getting rate limited

if __name__ == "__main__":
    TwitterMonitor = TwitterMonitor()
    asyncio.get_event_loop().run_until_complete(TwitterMonitor.monitor_twitter())
