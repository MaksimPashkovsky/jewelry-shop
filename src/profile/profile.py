from collections import defaultdict
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from database_service import DatabaseService

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static')
storage = DatabaseService()


@profile.route('/', methods=['GET'])
@login_required
def profile_page():
    return render_template('profile/profile.html')


@profile.route('/save', methods=['POST'])
@login_required
def save_profile_info():
    data = request.get_json()
    field, value = tuple(data.items())[0]

    if field != 'balance' and value in storage.get_user_column(field):
        return '', 500

    user = storage.get_user_by_id(current_user.id)
    setattr(user, field, value)
    storage.save(user)
    return '', 200


@profile.route('/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']

    user = storage.get_user_by_id(current_user.id)

    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        storage.save(user)
        return '', 200
    return '', 500


@profile.route('/history', methods=['GET'])
@login_required
def history_page():
    history_notes = storage.get_all_history_notes_by_user_id(current_user.id)
    d = [(note.date, note) for note in history_notes]
    res = defaultdict(list)
    for k, v in d:
        res[k].append(v)
    final = [{'date': k, 'items': v} for k, v in res.items()]
    final.sort(key=lambda x: x['date'], reverse=True)
    return render_template('profile/history.html', notes=final)