import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>

"""

page_footer = """
</body>
</html>
"""
new_post = """
<!DOCTYPE html>
<html>
<head>
    <title>Unit 2 Signup</title>
</head>
<body>
    <h2>Welcome, {0}</h2>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    def get(self):
        self.redirect('/unit2/signup')

edit_header = "<h1>User-Signup</h1>"

login_form = """
<form action="/unit2/signup" method="post">
    <table>
        <tbody>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input name="username" type="text" value="{0}" required/>
                    <span class="error">{1}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input name="password" type="password" value="" required/>
                    <span class="error">{2}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="verify">Verify Password</label>
                </td>
                <td>
                    <input name="verify" type="password" value="" required/>
                    <span class="error">{3}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email">Email (Optional)</label>
                </td>
                <td>
                    <input name="email" type="email" value="{4}"/>
                    <span class="error">{5}</span>
                </td>
            </tr>
        </tbody>
    </table>
    <input type="submit">

</form>
"""



class Signup(webapp2.RequestHandler):
    def get(self):






        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''

        main_content = edit_header + login_form.format("","","","","","") + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        validusername = ""
        validemail = ""

        if valid_username(username):
            validusername = username

        if not valid_username(username):
            error_username = "That's not a valid username."

            have_error = True


        if not valid_password(password):
            error_password = "That wasn't a valid password."

            have_error = True

        if password != verify:
            error_verify = "Your passwords didn't match."

            have_error = True


        if valid_email(email):
            validemail = email


        if not valid_email(email):
            error_email = "That's not a valid email."

            have_error = True

        if have_error == False:
            self.redirect('/unit2/welcome?username=' + username)

        if have_error == True:

            main_content = edit_header + login_form.format(validusername, error_username, error_password, error_verify, validemail, error_email)
            content = page_header + main_content + page_footer
            self.response.write(content)
class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(new_post.format(username))
        else:
            self.redirect('/unit2/signup')




app = webapp2.WSGIApplication([
    ('/', Index),
    ('/unit2/signup', Signup),
    ('/unit2/welcome', Welcome)
], debug=True)
