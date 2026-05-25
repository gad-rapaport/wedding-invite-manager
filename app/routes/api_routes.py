from flask import Blueprint, jsonify, request
from app.controllers import guest_controller, event_controller

api_bp = Blueprint("api", __name__)


# ── Guests ──────────────────────────────────────────────────────────────────

@api_bp.route("/guests", methods=["GET"])
def list_guests():
    group = request.args.get("group")
    status = request.args.get("status")
    sort = request.args.get("sort", "name")
    guests = guest_controller.get_all_guests(group, status, sort)
    return jsonify([g.to_dict() for g in guests])


@api_bp.route("/guests/<int:guest_id>", methods=["GET"])
def get_guest(guest_id):
    guest = guest_controller.get_guest_by_id(guest_id)
    return jsonify(guest.to_dict())


@api_bp.route("/guests", methods=["POST"])
def create_guest():
    data = request.get_json()
    guest = guest_controller.create_guest(data)
    return jsonify(guest.to_dict()), 201


@api_bp.route("/guests/<int:guest_id>", methods=["PUT"])
def update_guest(guest_id):
    data = request.get_json()
    guest = guest_controller.update_guest(guest_id, data)
    return jsonify(guest.to_dict())


@api_bp.route("/guests/<int:guest_id>", methods=["DELETE"])
def delete_guest(guest_id):
    guest_controller.delete_guest(guest_id)
    return jsonify({"deleted": guest_id})


# ── Send ─────────────────────────────────────────────────────────────────────

@api_bp.route("/send/invitations", methods=["POST"])
def send_invitations():
    data = request.get_json() or {}
    guest_ids = data.get("guest_ids")  # None = send to all uninvited
    result = guest_controller.send_invitations(guest_ids)
    return jsonify(result)


@api_bp.route("/send/reminders", methods=["POST"])
def send_reminders():
    data = request.get_json() or {}
    guest_ids = data.get("guest_ids")
    result = guest_controller.send_reminders(guest_ids)
    return jsonify(result)


# ── Event ─────────────────────────────────────────────────────────────────────

@api_bp.route("/event", methods=["GET"])
def get_event():
    event = event_controller.get_active_event()
    if not event:
        return jsonify({}), 404
    return jsonify(event.to_dict())


@api_bp.route("/event", methods=["PUT"])
def update_event():
    data = request.get_json()
    event = event_controller.create_or_update_event(data)
    return jsonify(event.to_dict())


# ── Health ────────────────────────────────────────────────────────────────────

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})
