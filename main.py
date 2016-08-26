#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

def alphabet_position(letter):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return(alphabet.find(letter.lower()))


def rotate_character(char, rot):
    if(char.isalpha() != True):
        return char
    startList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    length = len(startList)
    index = alphabet_position(char)
    totalIteration = index + int(rot)
    rotated = startList[totalIteration % length]
    if(char == startList[index]):
        return rotated
    return rotated.upper()

def encrypt(text, rot):
    newString = ""
    for i in range(len(text)):
        newString = newString + rotate_character(text[i], rot)
    return newString

def user_input_is_valid(rot):
    if rot.isdigit():
        return True
    return False

# html boilerplate for the top of every page
#stylesheet didn't work
#gif file from http://giphy.com/gifs/code-gates-incunabula-cpIvoQSU8vC9O
page_header = """
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="styles.css"/>
        <title>Encryption</title>
    </head>
    <body style = "background-image: url(https://media.giphy.com/media/cpIvoQSU8vC9O/giphy.gif);
    background-size:cover">
        <h1 style="color:white">Encrypt Here</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
    </body>
</html>
"""

middle = """
    <form method="post">
        <label style="color:white">
            Rotate by how many?
            <input type="text" name="rot" value="%(rot)s">
        </label>
        <br>
        <br>
        <br>
        <textarea type="text" name="text" cols="80" rows="20">%(text)s</textarea>
        <div style="color:red">%(error)s</div>
        <br>
        <br>
        <input type="submit">
    </form>
    """

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", rot="0", text="Write your Text to encrypt here"):
        self.response.out.write(page_header + middle % {"error": error,
                                        "rot": cgi.escape(rot, quote = True),
                                        "text": cgi.escape(text, quote = True)}
                                        + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        user_rot = self.request.get('rot')
        user_text = self.request.get('text')
        escaped_text = cgi.escape(user_text, quote = True)
        validCheck = user_input_is_valid(user_rot)

        if validCheck:
            new_text = encrypt(escaped_text, user_rot)
            self.write_form("", user_rot, new_text)

        else:
            self.write_form("I need an integer in the 'Rotate' field", user_rot, user_text)



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
