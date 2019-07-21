from config import app
from controller_functions import index, process_user, process_login, wishes, make_wish, make_new_wish, edit_wish, process_edited_wish, delete_wish, grant_wish, logout

app.add_url_rule("/", view_func=index)
app.add_url_rule("/process_user", view_func=process_user, methods=["POST"])
app.add_url_rule("/process_login", view_func=process_login, methods=["POST"])
app.add_url_rule("/wishes", view_func=wishes)
app.add_url_rule("/make_wish", view_func=make_wish)
app.add_url_rule("/make_new_wish", view_func=make_new_wish, methods=["POST"])
app.add_url_rule("/edit_wish/<id>", view_func=edit_wish)
app.add_url_rule("/process_edited_wish/<id>", view_func=process_edited_wish, methods=["POST"])
app.add_url_rule("/delete_wish/<id>", view_func=delete_wish)
app.add_url_rule("/grant_wish/<id>", view_func=grant_wish)
app.add_url_rule("/logout", view_func=logout)