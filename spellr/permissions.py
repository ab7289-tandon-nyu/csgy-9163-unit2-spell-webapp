from flask_principal import RoleNeed, Permission, Need
from collections import namedtuple
from functools import partial

# flask-login needs
user_need = RoleNeed("user")
admin_need = RoleNeed("admin")

# permissions
admin_perm = Permission(admin_need)

# granular access control
seeHistory = namedtuple("histories", ["method", "value"])
seeHistoryNeed = Need(seeHistory, "seeHistory")


class SeeHistoryPermission(Permission):
    def __init__(self, history_id):
        need = seeHistoryNeed(unicode(history_id))  # noqa : F821
        super(SeeHistoryPermission, self).__init__(need, admin_need)
