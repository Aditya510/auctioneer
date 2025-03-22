from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=10)  # Original IPL team
    is_sold = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.team})"

class AuctionTeam(models.Model):
    name = models.CharField(max_length=100)
    total_points = models.IntegerField(default=1000)
    remaining_points = models.IntegerField(default=1000)
    
    def __str__(self):
        return self.name

class PlayerBid(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(AuctionTeam, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.name} sold to {self.team.name} for {self.amount}" 