from flask import flash


def get_flash_msg(error=None, success=None):
    if error is not None:
        return (error, "error")
    elif success is not None:
        return (success, "success")
    return None


def flash_errors(form, category="error"):
    """ convenience function to send form errors to the front end """
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)
