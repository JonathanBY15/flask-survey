from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '734-154-693'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SECRET_KEY"] = "secret_key"

toolbar = DebugToolbarExtension(app)

# responses = []

@app.route('/')
def show_main_page():
    return render_template('base.html', survey=satisfaction_survey)

@app.route('/start_survey', methods=['GET', 'POST'])
def start_survey():
    session['responses'] = []  # Clear the session variable 'responses'
    return redirect('/questions/1')

@app.route('/questions/<int:question_num>')
def show_question(question_num):
    responses = session.get('responses', [])

    if question_num < 1 or question_num > len(responses) + 1:
        # If the question number is out of range, redirect to the correct URL
        if len(responses) == len(satisfaction_survey.questions):
            return redirect('/thanks')
        else:
            flash("You're trying to access an invalid question. You are being redirected.")
            return redirect(f'/questions/{len(responses) + 1}')
    elif len(responses) == len(satisfaction_survey.questions):
        # If all questions have been answered, redirect to the thank you page
        return redirect('/thanks')
    elif question_num == len(responses) + 1:
        # If the user is trying to access the next question, render the question page
        return render_template('question.html', question=satisfaction_survey.questions[question_num - 1], question_num=question_num)
    else:
        # If the user tries to access a question out of order, redirect to the next question
        # flash("You're trying to access an invalid question. You are being redirected.")
        return redirect(f'/questions/{len(responses) + 1}')


@app.route('/answer', methods=['POST'])
def handle_answer():
    responses = session.get('responses', [])
    answer = request.form.get('choice')  # Use get() to handle missing field
    if answer is not None:
        responses.append(answer)
        session['responses'] = responses

        if len(responses) == len(satisfaction_survey.questions):
            return redirect('/thanks')
        else:
            return redirect(f"/questions/{len(responses)}")
    else:
        # Handle case where 'answer' field is missing
        return "Bad request: 'answer' field is missing", 400

@app.route('/thanks')
def show_thanks():
    return render_template('thanks.html')