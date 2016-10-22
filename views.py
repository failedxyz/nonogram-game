from flask import Blueprint

blueprint = Blueprint("views", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    return "Hello, world."
