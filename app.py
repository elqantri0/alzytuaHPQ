from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# =========================
# إعداد قاعدة البيانات
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL غير معرف")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# تعريف جدول الأسئلة
# =========================
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# صفحة المستخدم
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("question", "").strip()
        if text:
            q = Question(text=text)
            db.session.add(q)
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

# =========================
# صفحة الأدمن
# =========================
@app.route("/admin")
def admin():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("admin.html", questions=questions)

# =========================
# تشغيل التطبيق
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ينشئ الجدول تلقائياً إذا لم يكن موجوداً
    app.run(host="0.0.0.0", port=5000, debug=True)
