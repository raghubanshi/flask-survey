from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY']='praveen'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

# responses = []

@app.route('/')
def show_home_page():
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def show_start_survey():
    """Clear the session of responses."""
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "questions.html", question_num=qid, question=question)

@app.route('/answer', methods=["POST"])
def start_survey():
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    responses.append(choice)
    if (len(responses) == len(survey.questions)):
        return 'redirect("/complete")'
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")