from functools import wraps
from flask import Markup, flash, url_for, redirect
from flask_login import current_user


# 让用户必须确认账户的装饰器
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                "请先确认您的账号"
                "没有收到确认邮件？"
                "<a class='alert-link' href='%s'>重新发送确认邮件</a>" % url_for("auth.resend_confirm_mail")
            )
            flash(message, "warning")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)
    return decorated_function

