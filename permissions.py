from permission import Permission
from rules import UserRule, AdminRule


class UserPermission(Permission):
    #    """Only signin user has this permission."""
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    #    """Only admin user has this permission."""
    def rule(self):
        return AdminRule()
