from flask import session, flash, redirect, url_for
from permission import Rule


class UserRule(Rule):
    def check(self):
        # """Check if there is a user signed in."""
        return 'user_id' in session

    def deny(self):
        # """When no user signed in, redirect to signin page."""
        flash('Sign in first.')
        return redirect(url_for('signin'))

class AdminOnly(Rule):
    def check(self, rank):
        if rank is 'Admin':
            return 'user_id' in session
        return self.deny()

    def deny(self):
        flash('Admins only.')
        return redirect(url_for('signin'))