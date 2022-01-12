from typing import Dict
from discord_webhook import DiscordWebhook, DiscordEmbed

def send_webhook(webhook_url: str, tweet_data: Dict):
    webhook = DiscordWebhook(
        url=webhook_url
    )
    embed = DiscordEmbed(
        title=f"Tweet From {tweet_data['username']}", 
        color="92A9BD", 
        description=f"{tweet_data['tweet_text']}"
    )
    embed.set_author(
        name=f"Followers: {tweet_data['user_followers_count']} | Following: {tweet_data['user_friends_count']}", 
        icon_url=f"{tweet_data['user_profile_image_url_https'].replace('normal','400x400')}"
    )
    embed.add_embed_field(
        name="**Shortcuts:**", 
        value=f"[Tweet](https://twitter.com/{tweet_data['user_screen_name']}/status/{tweet_data['tweet_id']}) - [Likes](https://twitter.com/{tweet_data['user_screen_name']}/status/{tweet_data['tweet_id']}/likes) - [Retweets](https://twitter.com/{tweet_data['user_screen_name']}/status/{tweet_data['tweet_id']}/retweets) - [Profile](https://twitter.com/{tweet_data['user_screen_name']})", 
        inline=False
    )
    embed.set_footer(
        text="Tim Solutions makes difference", 
        icon_url="https://i.imgur.com/8KANDeK.jpg"
    )
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()