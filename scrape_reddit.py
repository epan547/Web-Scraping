import praw
from mdutils.mdutils import MdUtils
from datetime import date

class WebScraper():
    def __init__(self):
        self.reddit = self.create_reddit()

    def create_reddit(self):
        # Authentication goes here. Get info from https://www.reddit.com/prefs/apps
        reddit = praw.Reddit(client_id='my_client_id', client_secret='my_client_secret', user_agent='my_user_agent')
        return reddit

    def get_hot_posts(self, subreddit, x=10):
        # get x hot posts from the specified subreddit
        # subreddit: string
        # x: int
        self.subname = subreddit
        self.hot_posts = self.reddit.subreddit(subreddit).hot(limit=x)

    def get_comments(self, post):
        comments = []
        for num, top_level_comment in enumerate(post.comments):
            comments.append(top_level_comment.body)
        # print(post.title)
        print(comments)

    def save_to_file(self):
        # Create a file with the name of the subreddit and today's date
        today = date.today().strftime('%Y-%m-%d')
        mdFile = MdUtils(file_name=(self.subname+'_'+today+'.md'), title=(self.subname+' '+today))
        for post in self.hot_posts:
            mdFile.new_header(level=1, title=post.title)
            self.add_comments(post, mdFile)
            print("Done with: " + post.title)

        mdFile.create_md_file()
        print('DONE')

    def add_comments(self, post, mdFile):
        for num, top_level_comment in enumerate(post.comments):
            mdFile.new_header(level=2, title="Comment #"+str(num+1))
            mdFile.new_paragraph(top_level_comment.body.rstrip())


if __name__=="__main__":
    ws = WebScraper()
    ws.get_hot_posts("Lyme")
    ws.save_to_file()
