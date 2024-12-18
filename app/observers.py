class BonusObserver:
    def __init__(self, user):
        self.user = user

    def update_level(self):
        """Update the user's bonus level based on total spending."""
        total_spent = sum(t.amount for t in self.user.sent_transactions)
        if total_spent >= 1000:
            self.user.bonus_level = 3
        elif total_spent >= 500:
            self.user.bonus_level = 2
        elif total_spent >= 100:
            self.user.bonus_level = 1
        else:
            self.user.bonus_level = 0
