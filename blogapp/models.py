from django.db import models

# Create your models here.
class User(models.Model):
    v1 = [('Male', 'Male'),
          ('Female', 'Female'),
          ('Others', 'Others')]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=v1)
    pic = models.FileField(upload_to='profile_pics', default='sad.png')

    def __str__(self) -> str:
        return self.first_name
    

class Blog(models.Model):
    c1 = [('food', 'food'), 
          ('lifestyle', 'lifestyle'), 
          ('fashion', 'fashion'), 
          ('beauty', 'beauty')]

    title = models.CharField(max_length=150) 
    des = models.TextField()
    pic = models.FileField(upload_to='blog_photos', default='sad.jpg')
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    category = models.CharField(max_length=150, choices=c1)
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    message = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.message
    

class Donate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    amount = models.FloatField()

    