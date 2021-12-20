import uuid
from functools import wraps
from unittest import TestCase
from unittest.mock import Mock
from server.services.user.service import UserService, UserRepo
from server.services.user.abstract import UserInputData
from server.services.user.entity import *


def example_user(id: int, name: str, status: EmailStatus, role: Role):
    user = User(
        name,
        f'{name}@domen.com',
        generate_password_hash("password"),
        role,
        status,
        datetime.fromisocalendar(2020, 10, 4),
        id
    )
    return user


users = (
    example_user(1, "st.a.novoseltcev", EmailStatus.CONFIRMED, Role.OWNER),
    example_user(2, "admin", EmailStatus.CONFIRMED, Role.ADMIN),
    example_user(3, "new_admin", EmailStatus.REFUSED, Role.ADMIN),
    example_user(4, "conf_user", EmailStatus.CONFIRMED, Role.USER),
    example_user(5, "ref_user", EmailStatus.REFUSED, Role.USER),
    example_user(6, "new_user", EmailStatus.NOT_CONFIRMED, Role.USER),
)
users_by_id = {user.id: user for user in users}
users_by_name = {user.name: user for user in users}
users_by_email = {user.email: user for user in users}
users_by_uuid = {uuid.uuid4(): user for user in users}


def load_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise NotFoundError()

    return wrapper


class UsersMock(UserRepo, Mock):
    @classmethod
    @load_wrapper
    def from_id(cls, user_id):
        return users_by_id[user_id]

    @classmethod
    def all(cls):
        return users

    @classmethod
    @load_wrapper
    def from_uuid(cls, token):
        return users_by_uuid[token]

    @classmethod
    @load_wrapper
    def from_email(cls, email):
        return users_by_email[email]

    @classmethod
    @load_wrapper
    def from_name(cls, name):
        return users_by_name[name]

    @classmethod
    def create(cls, user):
        pass

    @classmethod
    def update(cls, id: int, user: User) -> NoReturn:
        pass

    @classmethod
    @load_wrapper
    def delete(cls, user_id):
        _ = users_by_id[user_id]


class UserServiceTestCase(TestCase):
    def setUp(self):
        UserService.Users = UsersMock

    def tearDown(self):
        UserService.Users = UserRepo

    def test_get_account(self):
        for id in range(-1, 100):
            if id in users_by_id.keys():
                self.assertEqual(UserService.get_account(id=id), users_by_id[id])
            else:
                self.assertRaises(NotFoundError, UserService.get_account, id)

    def test_get_accounts(self):
        for admin_id in range(-1, 100):
            if admin_id in users_by_id.keys():
                user = users_by_id[admin_id]
                if user.role == Role.OWNER or user._role == Role.ADMIN and user._email_status == EmailStatus.CONFIRMED:
                    self.assertEqual(UserService.get_accounts(admin_id=admin_id), users)
                else:
                    self.assertRaises(AdminRequiredError, UserService.get_accounts, admin_id)
            else:
                self.assertRaises(NotFoundError, UserService.get_accounts, admin_id)

    def test_update_account(self):  # TODO
        for id in range(-1, 100):
            if id in users_by_id.keys():
                user = users_by_id[id]
                UserService.update_account(id, UserInputData(name=user.name))
            else:
                self.assertRaises(NotFoundError, UserService.update_account, id, UserInputData)
        # UserService.update_account

    def test_delete_account(self):
        for id in range(-1, 100):
            if id in users_by_id.keys():
                UserService.delete_account(id=id)
            else:
                self.assertRaises(NotFoundError, UserService.delete_account, id)

    def test_register(self):  # TODO
        pass
        # UserService.register

    def test_login_by_name(self):
        self.assertRaises(LoginError, UserService.login, UserInputData(name="invalid", password="password", email=""))
        self.assertRaises(LoginError, UserService.login, UserInputData(name="invalid", password="invalid", email=""))
        for name in users_by_name:
            user = users_by_name[name]
            self.assertRaises(LoginError, UserService.login, UserInputData(name=name, password="invalid", email=user.email))
            self.assertRaises(LoginError, UserService.login, UserInputData(name=name, password="invalid", email=""))
            if user.email_status == EmailStatus.CONFIRMED:
                self.assertEqual(UserService.login(UserInputData(name=name, password="password", email="")), user.id)
                self.assertEqual(UserService.login(UserInputData(name=name, password="password", email=user.email)), user.id)
            else:
                self.assertRaises(
                    UnconfirmedEmailError,
                    UserService.login,
                    UserInputData(name=name, password="password", email="")
                )

    def test_login_by_email(self):
        self.assertRaises(LoginError, UserService.login, UserInputData(email="invalid", password="password", name=""))
        self.assertRaises(LoginError, UserService.login, UserInputData(email="invalid", password="invalid", name=""))
        for email in users_by_email:
            user = users_by_email[email]
            self.assertRaises(LoginError, UserService.login, UserInputData(email=email, password="invalid", name=""))
            self.assertRaises(LoginError, UserService.login, UserInputData(email=email, password="invalid", name=user.name))
            if user.email_status == EmailStatus.CONFIRMED:
                self.assertEqual(
                    UserService.login(UserInputData(email=email, password="password", name="")),
                    user.id
                )
                self.assertEqual(
                    UserService.login(UserInputData(email=email, password="password", name=user.name)),
                    user.id
                )
            else:
                self.assertRaises(
                    UnconfirmedEmailError,
                    UserService.login,
                    UserInputData(email=email, password="password")
                )

    def test_reset_password(self):  # TODO
        pass
        # UserService.reset_password

    def test_confirm_email(self):  # TODO
        pass
        # UserService.confirm_email
