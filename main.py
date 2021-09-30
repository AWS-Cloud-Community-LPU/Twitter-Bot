"""
MIT License

Copyright (c) 2021 AWS Cloud Community LPU

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import re
from datetime import datetime
import time
import sys
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


def print_logs(log_message):
    """Creates logs in logs.txt

    Keyword arguments:
        message : Message to be logged
    """
    line = "-------------\n"
    log_message = log_message + "\n"
    log_message = line + log_message + line
    with open(C.LOG_FILE, 'a+', encoding='utf8') as log_file:
        print(log_message, file=log_file)


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


def feed_parser():
    """Parses feed of AWS What's new and gives non duplicate news.

    Returns:
        News: In case of a non-duplicate news
        None: In case of a no non-duplicate news found
    """
    if not path.exists(C.TITLE_STORE):
        with open(C.TITLE_STORE, 'a', encoding='utf-8'):
            pass
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    with open(C.TITLE_STORE, "r", encoding="utf-8") as title_file:
        line_titles = title_file.readlines()
        for entry in news_feed.entries:
            flag = 0
            for line_title in line_titles:
                if str(entry.title)+"\n" == line_title:
                    flag = 1
            if flag == 0:
                return entry
    return None


def send_exception(api: tweepy.API, err: Exception, message: str):
    """Sends Exception with information to the developer's account

    Keyword arguments:
        api : Tweepy.API
        err : Exception message
        message: The string that caused the exception.
    """
    error_message = f"{get_time()}: Error with message:\n{message}\n{err}"
    print_logs(error_message)
    recipient_id = api.get_user(screen_name="garvit__joshi").id_str
    api.send_direct_message(recipient_id, error_message)
    api.send_direct_message(recipient_id, str(err))


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
        api = tweepy.API(auth, wait_on_rate_limit=True)
    except KeyError:
        message = "File or Keys not Found"
        print(message)
        print_logs(message)
        sys.exit(1)

    while True:
        try:
            entry = feed_parser()
            if(entry == None):
                # Wait for 5 min for again parsing the entry if no non-duplicate news is found
                time.sleep(300)
                continue
            time.sleep(10)  # wait for 10 Seconds until next news
            with open(C.TITLE_STORE, 'a+', encoding='utf-8') as title_file:
                print(entry.title, file=title_file)
            message = message_creator(entry)
            try:
                api.update_status(message)
                success_message = f"{get_time()}: Message Successfully tweeted:\n{message}"
                print_logs(success_message)
            except Exception as err:
                send_exception(api, err, message)
                end_text = f"{get_time()}: Bot Stopped by Exception"
                print_logs(end_text)
                print(end_text)
                sys.exit(1)

        except KeyboardInterrupt:
            end_text = f"{get_time()}: Bot Stopped by User"
            print_logs(end_text)
            print(end_text)
            sys.exit(0)


if __name__ == "__main__":
    start_text = f"{get_time()}: Bot Started"
    print_logs(start_text)
    print(start_text)
    main()
