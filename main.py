# MIT License

# Copyright (c) 2021 AWS Cloud Community LPU

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import re
from datetime import datetime
import time
from os import path
import configparser
import feedparser
import tweepy
import constants as C


def get_time():
    """Gets Current Time

    Returns:
        HH:MM:SS AM/PM DD/MM/YYYY
    """
    return datetime.now().strftime('%I:%M:%S %p %d/%m/%Y')


def print_logs(message):
    """Creates logs in logs.txt

    Keyword arguments:
        message : Message to be logged
    """
    print("-------------", file=open(C.LOG_FILE, 'a+'))
    print(message, file=open(C.LOG_FILE, 'a+'))
    print("-------------\n\n", file=open(C.LOG_FILE, 'a+'))


def message_creator(entry) -> str:
    """
    Returns news in a proper format

    Keyword arguments:
        entry : a perticular entry of rss feed used for extracting data.
    """
    cleanr = re.compile(
        '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    summary = re.sub(cleanr, '', entry.summary)
    # Twitter URL Shortner: 31 Character
    # Hashtag awseducate: 11 Character
    extra_length = len(entry.title) + 31 + 11
    summary_length = 280 - extra_length     # Max tweet length: 280 Character
    message = entry.title + "\n\n" + \
        summary[:summary_length] + "...\n" + "#awseducate\n" + entry.link
    return message


def check_time():
    """
    Checks time

    Return:
        "morning" : if time is 6AM.
        "afternoon" : if time is 2PM.
        "evening" : if time is 5PM.
        "night" : if time is 10PM.
    """
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(1)
        if str(current_time) in ("06:00:00", "06:00:01", "06:00:02"):
            time.sleep(1)
            return "morning"
        if str(current_time) in ("14:00:00", "14:00:01", "14:00:02"):
            time.sleep(1)
            return "afternoon"
        if str(current_time) in ("17:00:00", "17:00:01", "17:00:02"):
            time.sleep(1)
            return "evening"
        if str(current_time) in ("22:00:00", "22:00:01", "22:00:02"):
            time.sleep(1)
            return "night"


def feed_parser():
    """Parses feed of AWS What's new and gives non duplicate news.
    """
    if not path.exists(C.TITLE_STORE):
        open(C.TITLE_STORE, 'a').close()
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    with open(C.TITLE_STORE, "r") as title_file:
        line_titles = title_file.readlines()
        for entry in news_feed.entries:
            flag = 0
            for line_title in line_titles:
                if str(entry.title)+"\n" == line_title:
                    flag = 1
            if flag == 0:
                return entry
    return news_feed.entries[0]


def main():
    """Main function responsible for starting the bot
    """
    config = configparser.ConfigParser()
    try:
        config.read('secrets.ini')
        auth = tweepy.OAuthHandler(
            config['KEYS']['API_KEY'], config['KEYS']['API_SECRET_KEY'])
        auth.set_access_token(
            config['KEYS']['ACCESS_TOKEN'], config['KEYS']['ACCESS_TOKEN_SECRET'])
        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)
    except KeyError:
        message = "File or Keys not Found"
        print(message)
        print_logs(message)
        exit(1)

    while True:
        try:
            entry = feed_parser()
            time_status = check_time()
            print(entry.title, file=open(C.TITLE_STORE, 'a+'))
            message = message_creator(entry)
            try:
                api.update_status(message)
                success_message = f"{get_time()}: Message Successfully tweeted:\n{message}"
                print_logs(success_message)
            except tweepy.error.TweepError as err:
                error_message = f"{get_time()}: Error with message:\n{message}\n{err}"
                print_logs(error_message)
                recipient_id = api.get_user("garvit__joshi").id_str
                api.send_direct_message(recipient_id, error_message)
                api.send_direct_message(recipient_id, str(err))
                exit(1)
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(1)


if __name__ == "__main__":
    print(f"\n{get_time()}: Bot Started\n",
          file=open(C.LOG_FILE, 'a+'))
    print(f"\n{get_time()}: Bot Started\n")
    main()
