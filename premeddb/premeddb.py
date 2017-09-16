from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, send_file # imports rendering functions
from docx import Document
from io import BytesIO

from docx.shared import Inches


# Flask app defined
app = Flask(__name__)


# Links to database which is created in config.py
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from models import *

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    result = Scheduler.query.all()
    if request.method == 'POST':
        if int(Scheduler.query.count()) < 6:
            file = request.files['inputfile']
            schedulename = request.form['schedulename']
            data = file.read()
            signature = Scheduler(schedulename=schedulename,schedule=file.filename, data=data)
            db.session.add(signature)
            db.session.commit()
            result = Scheduler.query.all()
    return render_template("scheduler.html", result=result)


@app.route('/academics', methods=['POST', 'GET'])
def academics():
    grades = Grades.query.all()
    result = Mcat.query.all()
    result1 = References.query.all()
    if request.method == 'POST':
        ogpa = request.form['ogpa']
        sgpa = request.form['sgpa']
        signature = Grades(ogpa=ogpa, sgpa=sgpa)
        db.session.add(signature)
        db.session.commit()
    return render_template("academics.html", result=result, result1=result1, grades=grades)


@app.route('/academicsdetails', methods=['POST', 'GET'])
def academicsdetails():
    result = References.query.filter_by(id=request.form['academicsdetails']).first()
    return render_template("academicsdetails.html", result=result)


@app.route('/academicsdetailsprocess', methods=['POST', 'GET'])
def academicsdetailsprocess():
    edit = References.query.filter_by(id=request.form['update']).first()
    edit.email = request.form['email']
    edit.type = request.form['type']
    edit.status = request.form['status']
    db.session.commit()
    return redirect(url_for('academics'))


@app.route('/mcat', methods=['POST', 'GET'])
def mcat():
    if request.method == 'POST':
        if request.form['examdate'] != '':
            examdate = request.form['examdate']
            overall = request.form['overall']
            cp = request.form['cp']
            cars = request.form['cars']
            bb = request.form['bb']
            ps = request.form['ps']
            signature = Mcat(examdate=examdate, overall=overall, cp=cp, cars=cars, bb=bb, ps=ps)
            db.session.add(signature)
            db.session.commit()
    return redirect(url_for('academics'))


@app.route('/references', methods=['POST', 'GET'])
def references():
    if request.method == 'POST':
        if request.form['name'] != '':
            name = request.form['name']
            email = request.form['email']
            type = request.form['type']
            status = request.form['status']
            signature = References(name=name, email=email, type=type, status=status)
            db.session.add(signature)
            db.session.commit()
    return redirect(url_for('academics'))


@app.route('/activities', methods=['POST', 'GET'])
def activities():
    result = Activities.query.all()
    if request.method == 'POST':
        if request.form['activity'] != '':
            activity = request.form['activity']
            type = request.form['type']
            reference = request.form['reference']
            hours = request.form['hours']
            signature = Activities(activity=activity, type=type, reference=reference, hours=hours)
            db.session.add(signature)
            db.session.commit()
            result = Activities.query.all()
    return render_template("activities.html", result=result)


@app.route('/activitiesdetails', methods=['POST', 'GET'])
def activitiesdetails():
    result = Activities.query.filter_by(id=request.form['activitiesdetails']).first()
    return render_template("activitiesdetails.html", result=result)


@app.route('/activitiesdetailsprocess', methods=['POST', 'GET'])
def activitiesdetailsprocess():
    edit = Activities.query.filter_by(id=request.form['update']).first()
    edit.type = request.form['type']
    edit.hours = request.form['hours']
    edit.reference = request.form['reference']
    edit.startdate = request.form['startdate']
    edit.enddate = request.form['enddate']
    edit.description = request.form['description']
    db.session.commit()
    return redirect(url_for('activities'))


@app.route('/status', methods=['POST', 'GET'])
def status():
    result = Status.query.all()
    if request.method == 'POST':
        if request.form['university'] != '':
            university = request.form['university']
            primary = request.form['primary']
            secondary = request.form['secondary']
            interview = request.form['interview']
            offer = request.form['offer']
            signature = Status(university=university, primary=primary, secondary=secondary, interview=interview, offer=offer)
            db.session.add(signature)
            db.session.commit()
    return render_template("status.html", result=result)


@app.route('/statusdetails', methods=['POST', 'GET'])
def statusdetails():
    result = Status.query.filter_by(id=request.form['statusdetails']).first()
    return render_template("statusdetails.html", result=result)


@app.route('/statusdetailsprocess', methods=['POST', 'GET'])
def statusdetailsprocess():
    edit = Status.query.filter_by(id=request.form['update']).first()
    edit.primary = request.form['primary']
    edit.secondary = request.form['secondary']
    edit.interview = request.form['interview']
    edit.offer = request.form['offer']
    edit.essay1p = request.form['essay1p']
    edit.essay1a = request.form['essay1a']
    edit.essay2p = request.form['essay2p']
    edit.essay2a = request.form['essay2a']
    edit.essay3p = request.form['essay3p']
    edit.essay3a = request.form['essay3a']
    edit.essay4p = request.form['essay4p']
    edit.essay4a = request.form['essay4a']
    edit.essay5p = request.form['essay5p']
    edit.essay5a = request.form['essay5a']
    db.session.commit()
    return redirect(url_for('status'))

@app.route('/statusdetailsword', methods=['POST', 'GET'])
def statusdetailsword():
    edit = Status.query.filter_by(id=request.form['word']).first()
    document = Document()
    document.add_heading(edit.university, 0)
    #Essay 1
    document.add_heading('Prompt 1:', level=2)
    document.add_paragraph(edit.essay1p)
    document.add_heading('Essay 1:', level=2)
    document.add_paragraph(edit.essay1a)
    #Essay 2
    document.add_heading('Prompt 2:', level=2)
    document.add_paragraph(edit.essay2p)
    document.add_heading('Essay 2:', level=2)
    document.add_paragraph(edit.essay2a)
    #Essay 3
    document.add_heading('Prompt 3:', level=2)
    document.add_paragraph(edit.essay3p)
    document.add_heading('Essay 3:', level=2)
    document.add_paragraph(edit.essay3a)
    #Essay 4
    document.add_heading('Prompt 4:', level=2)
    document.add_paragraph(edit.essay4p)
    document.add_heading('Essay 4:', level=2)
    document.add_paragraph(edit.essay4a)
    #Essay 5
    document.add_heading('Prompt 5:', level=2)
    document.add_paragraph(edit.essay5p)
    document.add_heading('Essay 5:', level=2)
    document.add_paragraph(edit.essay5a)
    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Essays'
    f = BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    return send_file(f, as_attachment=True, attachment_filename='report.doc')


@app.route('/personalstatement', methods=['POST', 'GET'])
def personalstatement():
    result = Personal.query.all()
    if request.method == 'POST':
        if request.form['title'] != '':
            title = request.form['title']
            signature = Personal(title=title)
            db.session.add(signature)
            db.session.commit()
            result = Personal.query.all()
    return render_template("personalstatement.html", result=result)


@app.route('/personalstatementdetails', methods=['POST', 'GET'])
def personalstatementdetails():
    result = Personal.query.filter_by(id=request.form['personalstatementdetails']).first()
    return render_template("personalstatementdetails.html", result=result)


@app.route('/personalstatementdetailsprocess', methods=['POST', 'GET'])
def personalstatementdetailsprocess():
    edit = Personal.query.filter_by(id=request.form['update']).first()
    edit.essay = request.form['essay']
    db.session.commit()
    return redirect(url_for('personalstatement'))


# Deletion Routes

@app.route('/deletescheduler', methods=['POST', 'GET'])
def deletescheduler():
    if request.form['schedulerdelete'] != '':
        Scheduler.query.filter_by(id=int(request.form['schedulerdelete'])).delete()
        db.session.commit()
    return redirect(url_for('scheduler'))


@app.route('/deletegrades', methods=['POST', 'GET'])
def deletegrades():
    if request.form['gradesdelete'] != '':
        Grades.query.filter_by(id=int(request.form['gradesdelete'])).delete()
        db.session.commit()
    return redirect(url_for('academics'))


@app.route('/deletemcat', methods=['POST', 'GET'])
def deletemcat():
    if request.form['mcatdelete'] != '':
        Mcat.query.filter_by(id=int(request.form['mcatdelete'])).delete()
        db.session.commit()
    return redirect(url_for('academics'))


@app.route('/deletereferences', methods=['POST', 'GET'])
def deletereferences():
    if request.form['referencesdelete'] != '':
        References.query.filter_by(id=int(request.form['referencesdelete'])).delete()
        db.session.commit()
    return redirect(url_for('academics'))


@app.route('/deleteactivities', methods=['POST', 'GET'])
def deleteactivities():
    if request.form['activitiesdelete'] != '':
        Activities.query.filter_by(id=int(request.form['activitiesdelete'])).delete()
        db.session.commit()
    return redirect(url_for('activities'))


@app.route('/deletestatus', methods=['POST', 'GET'])
def deletestatus():
    if request.form['statusdelete'] != '':
        Status.query.filter_by(id=int(request.form['statusdelete'])).delete()
        db.session.commit()
    return redirect(url_for('status'))


@app.route('/deletepersonalstatement', methods=['POST', 'GET'])
def deletepersonalstatement():
    if request.form['personalstatementdelete'] != '':
        Personal.query.filter_by(id=int(request.form['personalstatementdelete'])).delete()
        db.session.commit()
    return redirect(url_for('personalstatement'))


# Makes Summary Word Doc
@app.route('/summary')
def summary():
    document = Document()
    document.add_heading("Sample Press Release", 0)
    document.add_paragraph('Intense quote', style='IntenseQuote')
    document.add_paragraph('first item in unordered list', style='ListBullet')
    document.add_paragraph('first item in ordered list', style='ListNumber')
    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    f = BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    return send_file(f, as_attachment=True, attachment_filename='report.doc')


# Flask app initialized
if __name__ == '__main__':
    app.run()
