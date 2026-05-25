import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.controllers import guest_controller, event_controller
from app.models.guest import Guest

ui_bp = Blueprint("ui", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Dashboard ─────────────────────────────────────────────────────────────────

@ui_bp.route("/")
def dashboard():
    from datetime import datetime
    total = Guest.query.count()
    invited = Guest.query.filter_by(invitation_sent=True).count()
    reminded = Guest.query.filter_by(reminder_sent=True).count()
    event = event_controller.get_active_event()
    days_left = None
    if event and event.wedding_date:
        days_left = (event.wedding_date - datetime.utcnow()).days
    return render_template(
        "dashboard.html",
        total=total, invited=invited, reminded=reminded,
        not_invited=total - invited, event=event, days_left=days_left,
    )


# ── Guests ────────────────────────────────────────────────────────────────────

@ui_bp.route("/guests")
def guests():
    group = request.args.get("group")
    status = request.args.get("status")
    sort = request.args.get("sort", "name")
    guests_list = guest_controller.get_all_guests(group, status, sort)
    return render_template("guests.html", guests=guests_list,
                           group=group, status=status, sort=sort)


@ui_bp.route("/guests/add", methods=["GET", "POST"])
def add_guest():
    if request.method == "POST":
        try:
            guest_controller.create_guest(request.form.to_dict())
            flash("האורח נוסף בהצלחה!", "success")
            return redirect(url_for("ui.guests"))
        except Exception as e:
            flash(f"שגיאה: {e}", "error")
    return render_template("guest_form.html", guest=None, action="הוסף")


@ui_bp.route("/guests/<int:guest_id>/edit", methods=["GET", "POST"])
def edit_guest(guest_id):
    guest = guest_controller.get_guest_by_id(guest_id)
    if request.method == "POST":
        guest_controller.update_guest(guest_id, request.form.to_dict())
        flash("האורח עודכן בהצלחה!", "success")
        return redirect(url_for("ui.guests"))
    return render_template("guest_form.html", guest=guest, action="עדכן")


@ui_bp.route("/guests/<int:guest_id>/delete", methods=["POST"])
def delete_guest(guest_id):
    guest_controller.delete_guest(guest_id)
    flash("האורח נמחק.", "info")
    return redirect(url_for("ui.guests"))


# ── Event settings ────────────────────────────────────────────────────────────

@ui_bp.route("/event", methods=["GET", "POST"])
def event_settings():
    event = event_controller.get_active_event()
    if request.method == "POST":
        data = request.form.to_dict()
        file = request.files.get("invitation_image")
        if file and allowed_file(file.filename):
            from flask import current_app
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            data["invitation_image_path"] = f"/static/uploads/{filename}"
        event_controller.create_or_update_event(data)
        flash("פרטי האירוע נשמרו!", "success")
        return redirect(url_for("ui.event_settings"))
    return render_template("event_settings.html", event=event)


# ── Send ──────────────────────────────────────────────────────────────────────

@ui_bp.route("/send", methods=["GET", "POST"])
def send_page():
    event = event_controller.get_active_event()
    result = None
    if request.method == "POST":
        action = request.form.get("action")
        selected = request.form.getlist("guest_ids")
        guest_ids = [int(i) for i in selected] if selected else None

        if action == "invitations":
            result = guest_controller.send_invitations(guest_ids)
        elif action == "reminders":
            result = guest_controller.send_reminders(guest_ids)

        flash(
            f"נשלחו {result.get('sent', 0)} הודעות. נכשלו: {result.get('failed', 0)}",
            "success" if result.get("failed", 0) == 0 else "warning",
        )

    uninvited = Guest.query.filter_by(invitation_sent=False).all()
    not_reminded = Guest.query.filter_by(invitation_sent=True, reminder_sent=False).all()
    return render_template("send_invitations.html", event=event,
                           uninvited=uninvited, not_reminded=not_reminded, result=result)
