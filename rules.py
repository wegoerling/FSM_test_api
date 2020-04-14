from os import abort

from flask import session, flash, redirect, url_for
from permission import Rule
from app import User


class UserRule(Rule):
    def check(self):
        # """Check if there is a user signed in."""
        return 'user_id' in session

    def deny(self):
        # """When no user signed in, redirect to signin page."""
        flash('Sign in first.')
        return redirect(url_for('signin'))


class AdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        user_id = int(session['user_id'])
        user = User.query.filter(User.id == user_id).first()
        return user and user.is_admin

    def deny(self):
        abort(403)
