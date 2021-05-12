import random
import time


class Game:
    PLAYS = {1: 'Rock', 2: 'Paper', 3: 'Scissors'}
    LOGIC = {
        'Rock': 'Paper',
        'Paper': 'Scissors',
        'Scissors': 'Rock',
    }

    def __init__(self, player, players_count=2):
        self.state = "Playing"
        self.left_over = []
        if players_count < 2 or players_count % 2 != 0:
            raise ValueError('An even number of players is required to play Rock/Paper/Scissors')
        if type(player) != str:
            raise TypeError('Player name must be a string')
        self.players_count = players_count
        self.player = player
        self.league = [[player, 'Bot 1']]
        self.winners = []
        self.opponent = "Bot 1"
        self.bot_num = 2
        self.sub_leagues = 0
        self.sub_leagues_determiner = self.players_count
        if self.players_count > 2:
            bracket = []
            for bot in range(0, players_count):
                bot_name = f'Bot {self.bot_num}'
                self.bot_num += 1
                if len(bracket) < 2:
                    bracket.append(bot_name)
                else:
                    self.league.append(bracket)
                    bracket = []
                    bracket.append(bot_name)
        while self.sub_leagues_determiner != 1:
            if self.sub_leagues_determiner % 2 == 0:
                self.sub_leagues_determiner //= 2
                self.sub_leagues += 1
            else:
                self.sub_leagues_determiner //= 2
                self.sub_leagues += 2

    def run(self):
        for sub_league in range(self.sub_leagues):
            if self.state == "Playing":
                self.show_league()
                self.play_bot_matches()
                self.play_match()
                time.sleep(5)
                self.update_stats()
            else:
                break
        if self.state == "Playing":
            print("Congratulations! You won the league.")
        if self.state == "Lose":
            print("You lost the game!")

    def show_league(self):
        print("\nCurrent League:")
        for match in self.league:
            if len(match) > 1:
                print(match[0] + ' - ' + match[1], end='  |  ')
            else:
                print(match[0])
        print("\n----------------")

    def play_match(self):
        play = self.PLAYS[int(input('What are you playing? Pick a number! 1. Rock | 2. Paper | 3. Scissors\n'))]
        bot_play = self.PLAYS[random.randint(1, 3)]
        if play == bot_play:
            print(f'DRAW!\nYou played: {play} \n' + f'{self.opponent} played: {bot_play} \n')
            print("Replay in...\n1..")
            time.sleep(1.5)
            print("2..")
            time.sleep(1.5)
            print("3..\n")
            self.play_match()

        winner = self.determine_winner(play=play, bot_play=bot_play)
        if winner == 'player':
            print(f"You win!\nYou played: {play}\nYour opponent played: {bot_play}")
            print("----------------")
            self.winners.append(self.player)
        elif winner == 'bot':
            print(f"You lose.\nYou played: {play}\nYour opponent played: {bot_play}")
            print("----------------")
            self.winners.append(self.opponent)

    def play_bot_matches(self):
        if len(self.league[1:]) > 1:
            print("Other matches:")
            for match in self.league[1:]:
                if len(match) > 1:
                    winner_index = random.randint(0, 1)
                    winner = match[winner_index]
                    if winner_index == 1:
                        print(f"- {winner} defeated {match[0]}")
                    else:
                        print(f"- {winner} defeated {match[1]}")
                    time.sleep(2)
                    self.winners.append(winner)
        else:
            print("There are no other matches.")
        print("----------------")

    def determine_winner(self, play, bot_play):
        for loser_play, winner_play in self.LOGIC.items():
            if play == loser_play and bot_play == winner_play:
                winner = 'bot'
                self.state = "Lose"
                return winner
            elif play == winner_play and bot_play == loser_play:
                winner = 'player'
                return winner

    def update_stats(self):
        self.league = self.winners[-1::-1]
        self.winners = []
        if len(self.league) % 2 != 0:
            self.left_over.append(self.league[-1])
        new_league = []
        bracket = []
        for _ in range(len(self.league)):
            if len(bracket) < 2:
                bracket.append(self.league[_])
            else:
                new_league.append(bracket)
                bracket = []
                bracket.append(self.league[_])
        if len(bracket) > 1:
            new_league.append(bracket)
        if len(self.left_over) != 0:
            new_league.append(self.left_over)
        self.league = new_league


a = Game('Faramarz', 12)
a.run()
