"""
MIT License

Copyright (c) 2022 AWS Cloud Community LPU

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
    return datetime.now().strftime("%I:%M:%S %p %d/%m/%Y")


def print_logs(log_message, console=False):
    """Creates logs in logs.txt

    Keyword arguments:
        message : Message to be logged
        console : specifies if to print log in console
    """
    line = "-------------\n"
    log_message = log_message + "\n"
    log_message = line + log_message + line
    if console is True:
        print(log_message)
    with open(C.LOG_FILE, "a+", encoding="utf8") as log_file:
        print(log_message, file=log_file)


def message_creator(entry) -> str:
    """
    Returns news in a proper format

    Keyword arguments:
        entry : a perticular entry of rss feed used for extracting data.

    Returns:
        message: Tweet(str) in 280 character
    """
    cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    summary = re.sub(cleanr, "", entry.summary)
    # Twitter URL Shortner: 31 Character
    # Hashtag awseducate: 11 Character
    extra_length = len(entry.title) + 31 + 11
    summary_length = 280 - extra_length  # Max tweet length: 280 Character
    message = (
        entry.title
        + "\n\n"
        + summary[:summary_length]
        + "...\n"
        + "#awseducate\n"
        + entry.link
    )
    return message


def feed_parser(api: tweepy.API):
    """Parses feed of AWS What's new and gives non duplicate news.

    Keyword arguments:
        api : Tweepy.API

    Returns:
        News: In case of a non-duplicate news
        None: In case of a no non-duplicate news found
    """
    if not path.exists(C.TITLE_STORE):
        with open(C.TITLE_STORE, "a", encoding="utf-8"):
            pass
    try:
        news_feed = feedparser.parse(C.AWS_FEED_URL)
    except Exception as err:
        time.sleep(20)
        send_exception(api, err, "Feed Parser")
        return None
    with open(C.TITLE_STORE, "r", encoding="utf-8") as title_file:
        line_titles = title_file.readlines()
        for entry in news_feed.entries:
            found_flag = 0  # turns to 1 if entry has already been tweeted
            for line_title in reversed(line_titles):
                if str(entry.title) + "\n" == line_title:
                    found_flag = 1
                    break
            if found_flag == 0:
                return entry
    return None


def send_exception(api: tweepy.API, err: Exception, message: str):
    """Sends Exception with information to the developer's account

    Keyword arguments:
        api : Tweepy.API
        err : Exception message
        message: The string that caused the exception.
    """
    error_message = f"{get_time()}: Error with message:\n{message}\n{err}\n"
    for dev in C.DEVELOPERS:
        error_message = error_message + f"Sending message to developer: {dev}\n"
        recipient_id = api.get_user(screen_name=dev).id_str
        api.send_direct_message(recipient_id, error_message)
    print_logs(error_message)


def main():
    """Main function responsible for starting the bot"""
    config = configparser.ConfigParser()
    try:
        config.read("secrets.ini")
        auth = tweepy.OAuthHandler(
            config["KEYS"]["API_KEY"], config["KEYS"]["API_SECRET_KEY"]
        )
        auth.set_access_token(
            config["KEYS"]["ACCESS_TOKEN"], config["KEYS"]["ACCESS_TOKEN_SECRET"]
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)
    except KeyError:
        message = "Secrets File or Keys not Found"
        print_logs(message, True)
        sys.exit(1)

    while True:
        try:
            entry = feed_parser(api)
            if entry is None:
                # Wait for 10 seconds for again parsing the entry if no non-duplicate news is found
                time.sleep(10)
                continue
            with open(C.TITLE_STORE, "a+", encoding="utf-8") as title_file:
                print(entry.title, file=title_file)
            message = message_creator(entry)
            try:
                api.update_status(message)
                success_message = (
                    f"{get_time()}: Message Successfully tweeted:\n{message}"
                )
                print_logs(success_message)
            except Exception as err:
                send_exception(api, err, message)
                end_text = f"{get_time()}: Bot caught an Exception"
                print_logs(end_text, True)

        except KeyboardInterrupt:
            end_text = f"{get_time()}: Bot Stopped by User"
            print_logs(end_text, True)
            sys.exit(0)


if __name__ == "__main__":
    start_text = f"{get_time()}: Bot Started"
    print_logs(start_text, True)
    main()
