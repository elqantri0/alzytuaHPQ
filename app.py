from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# =========================
# إعداد التطبيق
# =========================
app = Flask(__name__)
app.secret_key = "secret-key-change-this"  # ضروري للـ flash messages

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
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# إنشاء الجداول عند أول تشغيل
# =========================
with app.app_context():
    db.create_all()

# =========================
# صفحة المستخدم
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("question", "").strip()
        if text:
            try:
                q = Question(text=text)
                db.session.add(q)
                db.session.commit()
                flash("تم إرسال السؤال بنجاح!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"حدث خطأ في حفظ السؤال: {e}", "danger")
        else:
            flash("لا يمكن إرسال سؤال فارغ!", "warning")
        return redirect(url_for("index"))

    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("index.html", questions=questions)

# =========================
# صفحة الأدمن (بدون تسجيل دخول)
# =========================
@app.route("/admin")
def admin():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("admin.html", questions=questions)

# =========================
# تشغيل التطبيق
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
