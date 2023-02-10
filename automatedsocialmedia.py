import tweepy
import time
import logging
import argparse
import facebook
import instagram

# Enter your API credentials here
TWITTER_API_KEY = "YOUR TWITTER API KEY"
TWITTER_API_SECRET = "YOUR TWITTER API SECRET"
TWITTER_ACCESS_TOKEN = "YOUR TWITTER ACCESS TOKEN"
TWITTER_ACCESS_TOKEN_SECRET = "YOUR TWITTER ACCESS TOKEN SECRET"

FACEBOOK_API_KEY = "YOUR FACEBOOK API KEY"
FACEBOOK_API_SECRET = "YOUR FACEBOOK API SECRET"

INSTAGRAM_API_KEY = "YOUR INSTAGRAM API KEY"
INSTAGRAM_API_SECRET = "YOUR INSTAGRAM API SECRET"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Authenticate to Facebook
facebook_auth = facebook.OAuthHandler(FACEBOOK_API_KEY, FACEBOOK_API_SECRET)

# Authenticate to Instagram
instagram_auth = instagram.OAuthHandler(INSTAGRAM_API_KEY, INSTAGRAM_API_SECRET)

# Create API object
api = tweepy.API(auth)
facebook_api = facebook.API(facebook_auth)
instagram_api = instagram.API(instagram_auth)


def like_tweets(query, count):
    """Like tweets that match a query."""
    logger.info(f"Liking {count} tweets that match query: {query}")
    tweets = tweepy.Cursor(api.search, q=query, lang="en").items(count)


    try:
        for tweet in tweepy.Cursor(api.search, q=query, tweet_mode="extended").items(count):
            try:
                tweet.favorite()
                logger.info(f"Liked tweet {tweet.id} by @{tweet.user.screen_name}")
                time.sleep(30)
            except tweepy.TweepError as e:
                logger.error(f"Could not like tweet {tweet.id}: {e}")
    except tweepy.TweepError as e:
        logger.error(f"Error searching for tweets: {e}")


def like_facebook_posts(query, count):
    """Like Facebook posts that match a query."""
    logger.info(f"Liking {count} Facebook posts that match query: {query}")
    try:
        posts = facebook_api.search(q=query, count=count)
        for post in posts:
            try:
                facebook_api.like(post["id"])
                logger.info(f"Liked Facebook post {post['id']}")
                time.sleep(30)
            except facebook.FacebookError as e:
                logger.error(f"Could not like Facebook post {post['id']}: {e}")
    except facebook.FacebookError as e:
        logger.error(f"Error searching for Facebook posts: {e}")


def like_instagram_posts(query, count):
    """Like Instagram posts that match a query."""
    logger.info(f"Liking {count} Instagram posts that match query: {query}")
    try:
        posts = instagram_api.search(q=query, count=count)
        for post in posts:
            try:
                instagram_api.like(post["id"])
                logger.info(f"Liked Instagram post {post['id']}")
                time.sleep(30)
            except instagram.InstagramError as e:
                logger.error(f"Could not like Instagram post {post['id']}: {e}")
    except instagram.InstagramError as e:
        logger.error(f"Error searching for Instagram posts: {e}")


def main():
    parser = argparse.ArgumentParser(description="Automate social media interactions")
    parser.add_argument("--platform", type=str, required=True, choices=["twitter", "facebook", "instagram"],
                        help="The platform to automate interactions on")
    parser.add_argument("--query", type=str, required=True, help="The query to search for")
    parser.add_argument("--count", type=int, required=True, help="The number of interactions to perform")
    args = parser.parse_args()

    if args.platform == "twitter":
        like_tweets(args.query, args.count)
    elif args.platform == "facebook":
        like_facebook_posts(args.query, args.count)
    elif args.platform == "instagram":
        like_instagram_posts(args.query, args.count)


if __name__ == "__main__":
    main()

