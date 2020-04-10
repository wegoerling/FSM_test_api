from permission import Permission
from rules import UserRule, AdminOnly


class UserPermission(Permission):
#    """Only signin user has this permission."""
    def rule(self):
        return UserRule()

class AdminPermission(Permission):
#    """Only signin user has this permission."""
    def rule(self):
        return AdminOnly()