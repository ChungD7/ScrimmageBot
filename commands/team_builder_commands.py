from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint, choice

# Foobar
team_names = []
# Foobar
players_queue = []

# Array of players
team_one_players = []
team_two_players = []

# Flag for drafting
teams_are_drafting = False

# Currently drafting player
currently_drafting_player = None

MINIMUM_PLAYERS_TO_START_TEAMS = 2


def init_team_builder() -> None:
    ''' Reset all global variables'''
    global team_names, players_queue, team_one_players, team_two_players, teams_are_drafting, currently_drafting_player
    # Foobar
    team_names = []
    # Foobar
    players_queue = []

    # Array of players
    team_one_players = []
    team_two_players = []

    # Flag for drafting
    teams_are_drafting = False

    # Currently drafting player
    currently_drafting_player = None

def get_players_as_string(players_list : list, enumerate_based_off_list_length = False, mention = False) -> str:
    '''Foobar'''
    msg = ""
    total_spots = 10 if not enumerate_based_off_list_length else len(players_list)
    for index in range(total_spots):
        if index < len(players_list):
            player_raw = players_list[index]
            player_name = player_raw if not mention else '@' + player_raw
        else:
            player_name = ""
        
        msg += f"{index + 1}. {player_name}"

        if index < total_spots - 1:
            msg += '\n'
    
    return msg


class StartTeam(BaseCommand):
    '''Foobar'''

    def __init__(self):
        description = "Create two teams and pass in team names."
        params = ["team one", "team two"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        global team_names, players_queue, MINIMUM_PLAYERS_TO_START_TEAMS

        # FOOBAR
        if len(players_queue) < MINIMUM_PLAYERS_TO_START_TEAMS:
            await message.channel.send(f"Oops, you need at least {MINIMUM_PLAYERS_TO_START_TEAMS} players in the queue to start team formation!")
            return

        try:
            team_one_name = str(params[0])
            team_two_name = str(params[1])
        except:
            await message.channel.send("Oops, something happened. Please try again.")
            return

        if team_one_name == team_two_name:
            await message.channel.send("Teams should probably have seperate names!")
            return
        
        team_names += [team_one_name, team_two_name]
        msg = ""
        for team in team_names:
            msg += team + ' '
        
        await message.channel.send(f"Teams: {msg}")
    
        choose_captain_command = ChooseCaptains()
        await choose_captain_command.handle(params, message, client)


class Join(BaseCommand):
    '''Foobar'''

    def __init__(self):
        description = "Join the queue for a team"
        params = []
        super().__init__(description, params)
    
    async def handle(self, params, message, client):
        global players_queue
        try:
            player_name = message.author.mention
        except:
            await message.channel.send("Oops, something happened. Please try again.")
            return
        
        if player_name in players_queue:
            await message.channel.send("Oops, you are already in the queue")
            return

        players_queue.append(player_name)

        await message.channel.send(f"{player_name} successfully joined the player queue!")
        return


class Draft(BaseCommand):
    '''Drafts a player from the players queue'''
    def __init__(self):
        description = "Draft a player from the queue"
        params = ["player name"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        global team_one_players, team_two_players, teams_are_drafting, players_queue, currently_drafting_player
        # Foobar
        player_issuing_command = message.author.mention
        
        # Foobar
        if not teams_are_drafting:
            await message.channel.send(f"Sorry, teams are not drafting right now!")
            return

        # Foobar
        if player_issuing_command != currently_drafting_player:
            await message.channel.send(f"Sorry, you are not up to draft right now!")
            return
        
        # Get player from the number passed in
        try:
            choosen_player_index = int(params[0])
            if not 1 <= choosen_player_index <= 10:
                raise ValueError
        except ValueError:
            await message.channel.send(f"Please enter a number 1-10")
            return
        
        try:
            chosen_player = players_queue[choosen_player_index - 1]
        except IndexError:
            await message.channel.send(f"Sorry, {choosen_player_index} is not a valid player in the queue!")
            return

        if chosen_player not in players_queue:
            await message.channel.send(f"Sorry, {chosen_player} is not in the players queue!")
            return

        # Debug 
        await message.channel.send(f"Available players: \n{get_players_as_string(players_queue)}")

        # Get which team the drafting player is on
        team = team_one_players if currently_drafting_player in team_one_players else team_two_players

        # Debug message
        await message.channel.send(f"{currently_drafting_player} drafted {chosen_player}!")
        
        team.append(chosen_player)
        players_queue.remove(chosen_player)

        # Switch drafting player
        other_team = team_one_players if team != team_one_players else team_two_players
        currently_drafting_player = other_team[0]


class ViewQueue(BaseCommand):
    '''Foobar'''

    def __init__(self):
        description = "debug command to print all players in queue"
        params = []
        super().__init__(description, params)
    
    async def handle(self, params, message, client):
        global players_queue

        if len(players_queue) == 0:
            msg = "No players in the queue"
        else:
            msg = f"Available players: \n{get_players_as_string(players_queue)}"

        await message.channel.send(msg)

class ViewTeams(BaseCommand):
    '''Foobar'''
    
    def __init__(self):
        description = "debug command to print both teams"
        params = []
        super().__init__(description, params)
    
    async def handle(self, params, message, client):
        global players_queue, team_one_players, team_two_players, team_names
        if len(team_names) < 2:
            await message.channel.send("You need to create teams first!")
            return

        team_one_name = team_names[0]
        team_two_name = team_names[1]
        
        if len(team_one_players) == 0:
            team_one_msg = f"No players on {team_one_name}"
        else:
            team_one_msg = f"{team_one_name} players: \n{get_players_as_string(team_one_players, True)}\n"
        
        if len(team_two_players) == 0:
            team_two_message = f"No players on {team_two_name}"
        else:
            team_two_message = f"{team_two_name} players: \n{get_players_as_string(team_two_players, True)}"

        await message.channel.send(team_one_msg + team_two_message)

class ChooseCaptains(BaseCommand):
    '''Foobar'''

    def __init__(self):
        description = "debug command to choose captains"
        params = []
        super().__init__(description, params)
    
    async def handle(self, params, message, client):
        global players_queue, team_one_players, team_two_players, currently_drafting_player, teams_are_drafting
        
        if len(players_queue) <= 2:
            message.channel.send("There are not enough players in the queue. Cannot select captains")
            return
        
        # Choose first captain and remove from the queue
        captain_one = choice(players_queue)
        players_queue.remove(captain_one)

        # Choose second captain and remove from the queue
        captain_two = choice(players_queue)
        players_queue.remove(captain_two)

        # Pass captains to individiual teams
        team_one_players.append(captain_one)
        team_two_players.append(captain_two)

        currently_drafting_player = captain_one
        teams_are_drafting = True

        msg = f"{captain_one}, {captain_two}"
        await message.channel.send(msg)

class Cancel(BaseCommand):
    ''' Foobar '''

    def __init__(self):
        description = "Stop creating teams"
        params = []
        super().__init__(description, params)
    
    async def handle(self, params, message, client):
        try:
            init_team_builder()
            await message.channel.send(f"Team creation stopped!")
        except:
            await message.channel.send(f"Something fucked up")
            return

