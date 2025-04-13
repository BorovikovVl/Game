class Stats():
    """отслеживание статистики"""

    def __init__(self):
        """инициализирует статистику"""
        self.reset_stats()
        self.run_game = True
        with open('the_best_score.txt', 'r') as f:
            self.best_score = int(f.readline())

    def reset_stats(self):
        """статистика изменяющаяся во время игры"""
        self.starship_left = 2
        self.score = 0
