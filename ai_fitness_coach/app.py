from flask import Flask, render_template, request, redirect, url_for
from database import add_user, get_user, save_workout
from workout_generator import generate_workout
from chat_agent import chat_with_ai


app = Flask(__name__)

chat_memory = []

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=='POST':
        name = request.form["name"]
        age = int(request.form["age"])
        fitness_level=request.form["fitness_level"]
        goal = request.form["goal"]
        equipment=request.form["equipment"]
        add_user(name,age,fitness_level,goal,equipment)
        return redirect(url_for("workout",username=name))
    return render_template("register.html")


@app.route("/workout",methods=["POST","GET"])
def workout():
    if request.method=="POST":
        username=request.form["username"]
        return redirect(url_for("result",username=username))

    return render_template("workout.html")


@app.route("/workout/result/<username>")
def result(username):
    user = get_user(username)
    if not user:
        return f"User {username} not found",404
    
    workout_plan = generate_workout(
        user.fitness_level,
        user.goal,
        "30",
        user.equipment
    )

    save_workout(user.id,workout_plan)

    return render_template("result.html",user=user,workout=workout_plan)

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]  # Corrected the typo here
        response = chat_with_ai(user_input)
        chat_memory.append({"role": "user", "text": user_input})
        chat_memory.append({"role": "coach", "text": response})

        return render_template("chat.html", chat_history=chat_memory)
    return render_template("chat.html", chat_history=chat_memory) 

@app.route("/reset_chat")
def reset_chat():
    chat_memory.clear()
    return redirect("/chat")

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)


