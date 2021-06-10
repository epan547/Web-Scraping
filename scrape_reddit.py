import praw
from praw.models import MoreComments
from mdutils.mdutils import MdUtils
from datetime import date, datetime

class WebScraper():
    # Class wrapper for reddit scraping functionality
    def __init__(self):
        self.reddit = self.create_reddit()

    def create_reddit(self):
        # Authentication information goes here. Get info from https://www.reddit.com/prefs/apps
        reddit = praw.Reddit(client_id='', client_secret='', user_agent='')
        return reddit

    def get_hot_posts(self, subreddit, x=10):
        # get x hot posts from the specified subreddit
        # subreddit: string
        # x: int
        self.subname = subreddit
        self.hot_posts = self.reddit.subreddit(subreddit).hot(limit=x)

    def get_comments(self, post):
        # Gets the top level comments for a specified post
        comments = []
        for num, top_level_comment in enumerate(post.comments):
            comments.append(top_level_comment.body)
        # print(post.title)
        print(comments)

    def save_to_file(self):
        # Create a markdown file with the name of the subreddit and today's date
        today = date.today().strftime('%Y-%m-%d')
        mdFile = MdUtils(file_name=(self.subname+'_'+today+'.md'), title=(self.subname+' '+today))
        for post in self.hot_posts:
            mdFile.new_header(level=1, title=post.title)
            mdFile.new_paragraph("Created: " + datetime.utcfromtimestamp(int(post.created_utc)).strftime('%Y-%m-%d %H:%M:%S'))
            mdFile.new_paragraph(post.selftext)
            mdFile.new_paragraph(post.url)
            self.add_comments(post, mdFile)
            print("Done with: " + post.title)

        mdFile.create_md_file()
        print('DONE')

    def add_comments(self, post, mdFile):
        # Append comments to given markdown file
        for num, top_level_comment in enumerate(post.comments):
            # Ignore subcomments
            if isinstance(top_level_comment, MoreComments):
                continue
            mdFile.new_header(level=2, title="Comment #"+str(num+1))
            mdFile.new_paragraph(top_level_comment.body.rstrip())

    # TODO: Add light filtering, and mark likely key quotes


if __name__=="__main__":
    ws = WebScraper()
    ws.get_hot_posts("CoronavirusNewYork")
    ws.save_to_file()
