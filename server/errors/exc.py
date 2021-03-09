class UnknownId(Exception):
    name = ""

    def __str__(self):
        return "Unknown " + self.name + " id: " + str(self.args[0])


class TaskUnknownId(UnknownId):
    name = "task"


class CategoryUnknownId(UnknownId):
    name = "category"


class FileUnknownId(UnknownId):
    name = "file"


class UserUnknownId(UnknownId):
    name = "user"


class CategoryExistName(Exception):
    def __str__(self):
        return "Category name " + str(self.args[0]) + " already exist"


class InvalidSchema(Exception):
    def __str__(self):
        return "Invalid values"


class ForbiddenOperation(Exception):
    def __str__(self):
        return "Forbidden operation - ", str(self.args[0])