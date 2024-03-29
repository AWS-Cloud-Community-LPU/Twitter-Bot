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

EXCEPTION_THRESHOLD = 10  # Bot Exits after reaching exception threshold

TITLE_STORE = "titles.txt"  # logs titles of news that are already sent

LOG_FILE = "Main.log"  # log file

AWS_FEED_URL = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"  # RSS feed URL

DEVELOPERS = [
    "garvit__joshi",
]  # Used for Sending Exceptions to the Developers

line_titles = []  # Used for saving titles to Memory
