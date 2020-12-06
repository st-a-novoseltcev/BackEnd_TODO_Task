class IStorage:
    __counter = 0
    __default = 'None'
    tasks = []
    categories = []
    current_category = __default

    def __init__(self, path=''):
        """"INIT"""

    def append_task(self, title_task: str):
        """"APPEND task"""

    def append_category(self, category: str):
        """APPEND category"""

    def update_task_status(self, task_id: int):
        """CHANGE status"""

    def update_task_category(self, task_id: int, category: str):
        """"CHANGE category"""

    def remove_task(self, task_id: int):
        """"REMOVE"""

    def remove_category(self, category: str):
        """"REMOVE category"""

    def rename_category(self, destination: str, source: str):
        """RENAME"""
