from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

chats = {}
chat_counter = 1

# Login

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        print(email, password)

        if email == "test@test.com" and password == "1234":

            session["user"] = email

            return redirect("/")
    return render_template("login.html")

# Signup

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        print(request.form)

        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]

        level = request.form.get("niveau")

        if not level:
            return "Veuillez choisir un niveau"

        print(firstname, lastname, email, password)

        session["user"] = firstname + " " + lastname
        session["level"] = level

        return redirect("/")

    return render_template("signup.html")

# Desconnection

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/login")

# Index_test (Chat)

@app.route("/", methods=["GET","POST"])
def index():

    if "user" not in session:
        return redirect("/login")

    global chat_counter

    # Texte de recherche
    search = request.args.get("search","").lower()

    chat_id = session.get("chat_id")

    # pas du chat, creer un neoveau
    if chat_id not in chats:

        chats[chat_counter] = {
            "title": f"Chat {chat_counter}",
            "messages": []
        }

        # sauvergar chat actuelle en session
        session["chat_id"] = chat_counter
        chat_id = chat_counter
        chat_counter += 1

# Envoi des menssages

    if request.method == "POST":

        
        user_message = request.form["message"]

       
        if chats[chat_id]["title"].startswith("Chat"):
            chats[chat_id]["title"] = user_message[:30]

        
        chats[chat_id]["messages"].append({
            "role": "Usuario",
            "content": user_message
        })

        
        ai_response = fake_ai_response(user_message)
        chats[chat_id]["messages"].append({
            "role": "IA",
            "content": ai_response
        })

    # Menssages chat actuelle
    messages = chats[chat_id]["messages"]

    # Filtre chats
    filtered_chats = {
        id: chat for id, chat in chats.items()
        if search in chat["title"].lower()
    }

    # Rendre page principal
    return render_template(
        "index_test.html",
        messages=messages,
        chats=filtered_chats if search else chats,
        current_chat=chat_id, 
          user=session.get("user"),
    level=session.get("level")
    )

# Creer un chat

@app.route("/new_chat")
def new_chat():

    global chat_counter

    
    chats[chat_counter] = {
        "title": f"Chat {chat_counter}",
        "messages": []
    }

    session["chat_id"] = chat_counter
    chat_counter += 1

    return redirect("/")

# Ejecute chat

@app.route("/chat/<int:chat_id>")
def open_chat(chat_id):

    # nom chat
    if chat_id in chats:
        session["chat_id"] = chat_id

    return redirect("/")

# Responds IA (fake)

def fake_ai_response(text):

    # Texte
    text = text.lower()

    
    if "salut" in text:
        return "salut! Comment puis-je vous aider ?"

    if "merci" in text:
        return "De rien!"

    return "J’analyse votre question."


if __name__ == "__main__":
    app.run(debug=True)