import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Player, AuctionTeam, PlayerBid
from django.http import JsonResponse

def setup(request):
    if request.method == 'POST':
        team_count = int(request.POST.get('team_count', 0))
        points_per_team = int(request.POST.get('points_per_team', 1000))
        
        # Clear existing teams
        AuctionTeam.objects.all().delete()
        PlayerBid.objects.all().delete()
        Player.objects.update(is_sold=False)
        
        # Create teams
        for i in range(team_count):
            team_name = request.POST.get(f'team_name_{i}')
            AuctionTeam.objects.create(
                name=team_name,
                total_points=points_per_team,
                remaining_points=points_per_team
            )
        
        return redirect('auction')
    
    return render(request, 'auction/setup.html')

def auction(request):
    teams = AuctionTeam.objects.all()
    
    if not teams:
        messages.error(request, "Please set up teams first")
        return redirect('setup')
    
    # Calculate minimum bid (5% of total points)
    total_points = teams.first().total_points
    min_bid = round(total_points * 0.05)
    
    # Process POST requests
    if request.method == 'POST':
        # Get the player ID from the form
        player_id = request.POST.get('player_id')
        action = request.POST.get('action', '')
        
        # Look up the player by ID to ensure we're working with the correct player
        try:
            current_player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            messages.error(request, "Player not found!")
            current_player = None
            
        if current_player and action == 'unsold':
            # Mark player as processed but not sold to any team
            current_player.is_sold = True
            current_player.save()
            messages.info(request, f"{current_player.name} marked as unsold")
            return redirect('auction')
            
        elif current_player and action == 'finish':
            # Finalize the auction for this player
            winning_team_id = request.POST.get('current_bidder')
            bid_amount = int(request.POST.get('current_bid', 0))
            
            if winning_team_id and bid_amount > 0:
                winning_team = AuctionTeam.objects.get(id=winning_team_id)
                
                # Create bid
                PlayerBid.objects.create(
                    player=current_player,
                    team=winning_team,
                    amount=bid_amount
                )
                
                # Update team points
                winning_team.remaining_points -= bid_amount
                winning_team.save()
                
                # Mark player as sold
                current_player.is_sold = True
                current_player.save()
                
                messages.success(request, f"{current_player.name} sold to {winning_team.name} for {bid_amount}")
            else:
                messages.warning(request, "No valid bid placed, player remains unsold")
                
            return redirect('auction')
    
    # Get next player for auction
    remaining_players = Player.objects.filter(is_sold=False)
    
    if not remaining_players.exists():
        messages.info(request, "All players have been auctioned!")
        return redirect('results')
    
    # Select a random player for auction
    current_player = random.choice(remaining_players)
    
    # Get bidding history
    team_players = {}
    for team in teams:
        bids = PlayerBid.objects.filter(team=team)
        players = [(bid.player, bid.amount) for bid in bids]
        team_players[team] = players
    
    return render(request, 'auction/auction.html', {
        'teams': teams,
        'current_player': current_player,
        'min_bid': min_bid,
        'team_players': team_players,
        'remaining_count': remaining_players.count(),
    })

def results(request):
    teams = AuctionTeam.objects.all()
    team_players = {}
    
    for team in teams:
        bids = PlayerBid.objects.filter(team=team)
        players = [(bid.player, bid.amount) for bid in bids]
        team_players[team] = players
    
    return render(request, 'auction/results.html', {
        'teams': teams,
        'team_players': team_players,
    }) 