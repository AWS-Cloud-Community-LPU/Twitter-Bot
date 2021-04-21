# MIT License

# Copyright (c) 2021 AWS Cloud Community LPU

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contributed By: Ritik Kumar(https://github.com/ritikkr)



def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang="en", tweet_mode='extended')
        for tweet in tweets:
            hashtags = [i['text'].lower()
                        for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#')
                                 for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(5)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
    else:
        logger.error(
            "Hashtag search terms needs to be of type list", exc_info=True)
        return
