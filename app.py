from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/api/robot", methods=["GET", "POST"])
def post_route_robot():
    print(request.json)
    return {"data": "success"}

@app.route("/view/student_side")
def view_student_side():
    return render_template("student_side.html")

@app.route("/view/company_side")
def view_company_side():
    return render_template("company_side.html")

if __name__ == "__main__":
    app.run(debug=True)
