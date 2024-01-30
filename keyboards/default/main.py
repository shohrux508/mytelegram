from keyboards.default.admin import AdminKeyboard
from keyboards.default.user import UserKeyboard
from utils.db_api.manage import ManageUser



class StartKeyboard():
    def __init__(self, user_id):
        self.user_id = user_id

    def keyboard(self):
        if ManageUser(self.user_id).is_admin():
            return AdminKeyboard().main()
        else:
            return UserKeyboard().main()


