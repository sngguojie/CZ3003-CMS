import tweepy

class TwitterApp:
	
	def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(self.auth)

	def get_public_tweets(self):
		public_tweets = self.api.home_timeline()
		return [tweet.text for tweet in public_tweets]

	def update_status(self, status):
		updated_status = self.api.update_status(status)
		return updated_status


if __name__ == '__main__':
	import env
	import datetime
	twitterapp = TwitterApp(env.TWIT_CONSUMER_KEY, env.TWIT_CONSUMER_SECRET, env.TWIT_ACCESS_TOKEN, env.TWIT_ACCESS_TOKEN_SECRET)
	twitterapp.get_public_tweets()
	twitterapp.update_status('Crisis Update! '+str(datetime.datetime.now()))