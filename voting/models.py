from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # candidate is a registered user
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} for {self.position.name}"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate}"

    class Meta:
        unique_together = ('voter', 'candidate')  # basic safety

