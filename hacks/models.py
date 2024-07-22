from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Writer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    # profile_pic = models.ImageField(null=True, blank=True, 
                                    # upload_to="profiles/", 
                                    # default="profiles/default.jpg")
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.CharField(max_length=100, null=True, blank=True)
    # phone_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('username', 'twitter')
        
    def __str__(self) -> str:
        return self.username

class Hack(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="hack")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    comment_count = models.IntegerField(default=0, null=True, blank=True)

    @property
    def getVotes(self):
        vote_net = self.upvote - self.downvotes
        self.vote_net= vote_net
        self.save()
    
    @property
    def countComments(self):
        comments = self.comments.all()
        comment_count = comments.count()

        self.comment_count = comment_count
        self.save()

    def __str__(self) -> str:
        return self.body[:20]


    
class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    hack = models.ForeignKey(Hack, on_delete=models.CASCADE, null=True, related_name="comments")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="comment")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    reply_count = models.IntegerField(default=0, null=True, blank=True)
    @property
    def getVotes(self):
        votes = self.commentvote_set.all()
        upVotes = votes.filter(value='up').count()
        downVotes = votes.filter(value='down').count()
        vote_net = upVotes - downVotes
        

        self.upvote = upVotes
        self.downvote = downVotes
        self.vote_net= vote_net
        self.save()
        print(upVotes, downVotes, vote_net)
    
    @property
    def countReplies(self):
        replies = self.replies.all()
        reply_count = replies.count()

        self.reply_count = reply_count
        self.save()

    def __str__(self) -> str:
        return self.body[:20]

class Reply(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, 
                                null=True, related_name="replies")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="reply")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    @property
    def getVotes(self):
        
        vote_net = self.upvote - self.downvotes

        self.vote_net= vote_net
        self.save()
        # print(upVotes, downVotes, vote_net)

    def __str__(self) -> str:
        return self.body[:20]

class Report(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    hack = models.ForeignKey(Hack, on_delete=models.CASCADE, 
                             null=True, related_name="report")

# r