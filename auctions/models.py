from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class categories(models.Model):
    title=models.CharField(max_length=64)


    def __str__(self):
       return f'{self.title}'

class auction(models.Model):
    title = models.CharField(max_length=64)
    price = models.FloatField()
    category=models.ForeignKey(categories,on_delete=models.CASCADE)
    description = models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.TextField(default="please provide link")
    openorclosed =models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class bids(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biders")
      item = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="list")
      price = models.FloatField(max_length=100)

class Comment(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      comment = models.TextField(max_length=100)
      auctioninfo = models.ForeignKey(auction, on_delete=models.CASCADE)


      def  __str__(self):
           return '%s - %s' %(self.post.title, self.comment)


class watchlist(models.Model):
     product = models.ForeignKey(auction, on_delete=models.CASCADE, related_name="products")
     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
       return f'{self.user.username} added {self.product.title}'

