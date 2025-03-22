from django.contrib import admin
from .models import Player, AuctionTeam, PlayerBid

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'is_sold')
    search_fields = ('name', 'team')

@admin.register(AuctionTeam)
class AuctionTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_points', 'remaining_points')
    search_fields = ('name',)

@admin.register(PlayerBid)
class PlayerBidAdmin(admin.ModelAdmin):
    list_display = ('player', 'team', 'amount', 'timestamp')
    list_filter = ('team',)
    search_fields = ('player__name', 'team__name')