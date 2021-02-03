from flask import Flask
from server.task import task_blueprint
from server.category import category_blueprint
from server.file import file_blueprint


app = Flask(__name__)
app.template_folder = "static/templates"
app.register_blueprint(task_blueprint, url_prefix="/task")
app.register_blueprint(category_blueprint, url_prefix="/category")
app.register_blueprint(file_blueprint, url_prefix="/file")
