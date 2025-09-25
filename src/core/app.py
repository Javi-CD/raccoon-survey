from flask import Flask, render_template  # type: ignore

app = Flask(__name__, template_folder="../ui/templates", static_folder="../ui/static")


@app.route("/", methods=["GET"])
def root() -> tuple:
    """Pagina principal

    Returns:
        tuple: Vista inciial y codigo de respuesta
    """
    return render_template("inicio.html"), 200


@app.route("/login", methods=["GET", "POST"])
def login() -> tuple:
    """Pagina del Login

    Returns:
        tuple: Formulario de ingreso y codigo de repuesta
    """

    return render_template("login.html"), 200


@app.route("/surveys", methods=["GET", "POST"])
def encuestas() -> tuple:
    """Pagina del Encuestas

    Returns:
        tuple: Vista de encuestas y codigo de repuesta
    """

    return render_template("encuestas.html"), 200


# Nueva ruta para el Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True, port=3000)  # noqa: S201
