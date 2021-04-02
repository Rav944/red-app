from flask import jsonify


def make_error(status_code, error_type, message):
    response = jsonify({
        'status': status_code,
        'type': error_type,
        'message': message,
    })
    response.status_code = status_code
    return response

