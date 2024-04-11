from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import bcrypt
from urllib.parse import parse_qs, urlparse
from database import Database

class NoteApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # customers
        if self.path == '/user':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('user.html', 'rb') as file:
                self.wfile.write(file.read())

        if self.path == '/user/reservation':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('reservationForm.html', 'rb') as file:
                    self.wfile.write(file.read())

        if self.path.startswith('/user/reservations'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            db = Database()
            print(db.fetch_allReservations())
            reservationsData = db.fetch_allReservations()
            formatted_data = []
            for row in reservationsData:
                formatted_data.append({
                    'email': row[1],
                    'numGuests': row[2],
                    'date': row[3],
                    'time': row[4]
                })
            print("formatData", formatted_data)
            table_rows_html = ""
            for item in formatted_data:
                table_rows_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(item['email'], item['numGuests'], item['date'], item['time'])
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>All Reservations</title>
</head>
<body>
    <h1>All Reservations</h1>
    <table style="width:100%">
        <tr>
            <th>Email</th>
            <th>Number of Guests</th> 
            <th>Date</th>
            <th>Time</th>
        </tr>
        {}
    </table>
</body>
</html>
"""
            rendered_html = html_template.format(table_rows_html)
            self.wfile.write(rendered_html.encode())

            with open('reservations.html', 'rb') as file:
                self.wfile.write(file.read())

        if self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as file:
                self.wfile.write(file.read())

        # system
        if self.path == '/system':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('system.html', 'rb') as file:
                self.wfile.write(file.read())

        if self.path == '/user/updateReservation':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('updateReservation.html', 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        # user
        if self.path == '/user':
            content_length = int(self.headers['content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            print("form:", form_data)

            email, password, firstname = "", "", ""
            lastname, phonenumber = "", ""

            email = form_data["email"]
            password = form_data["password"]
            firstname = form_data["firstname"]
            lastname = form_data["lastname"]
            phonenumber = form_data["phonenumber"]

            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)

            db = Database()
            if(db.fetch_one(email)):
                print("Email already taken")
            else:
                db.create_user(email, hashed, firstname, lastname, phonenumber)

            self.send_response(201)
            self.end_headers()
        
        if self.path == '/login':
            content_length = int(self.headers['content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            email, password, firstname = "", "", ""
            lastname, phonenumber = "", ""

            email = form_data.get("email", [None])[0]
            password = form_data.get("psw", [None])[0]
            firstname = form_data.get("firstname", [None])[0]
            lastname = form_data.get("lastname", [None])[0]
            phonenumber = form_data.get("phonenumber", [None])[0]

            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)

            db = Database()
            if(db.fetch_one(email)):
                print("Email already taken")
                self.send_response(409)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('email_taken.html', 'rb') as file:
                    self.wfile.write(file.read())
                return
            else:
                db.create_user(email, hashed, firstname, lastname, phonenumber)

            self.send_response(201)
            self.end_headers()
            with open('login.html', 'rb') as file:
                self.wfile.write(file.read())

        if self.path.startswith('/user/reservation'):
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)
            print("resform:", form_data)

            self.send_response(201)
            self.end_headers()

            email = form_data.get("email", [None])[0]
            password = form_data.get("psw", [None])[0]

            db = Database()
            if (db.fetch_one(email)):
                self.user = db.fetch_one(email)
                print("selfTemp IN POST:", self.user)
                with open('reservationForm.html', 'rb') as file:
                    self.wfile.write(file.read())
            else:
                with open('login.html', 'rb') as file:
                    self.wfile.write(file.read())

        if self.path.startswith('/user/MadeReservation'):
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)

            email = form_data.get("email", [None])[0]
            numGuests = form_data.get("guests", [None])[0]
            date = form_data.get("date", [None])[0]
            time = form_data.get("time", [None])[0]

            db = Database()
            db.create_reservation(email, numGuests, date, time)

            self.send_response(201)
            self.end_headers()

            with open('reservationForm.html', 'rb') as file:
                    self.wfile.write(file.read())

        if self.path == ('/user/updatedReservation'):
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)

            email = form_data.get("email", [None])[0]
            numGuests = form_data.get("guests", [None])[0]
            date = form_data.get("date", [None])[0]
            time = form_data.get("time", [None])[0]

            db = Database()
            db.update_reservation(numGuests, date, time, email)

            self.send_response(201)
            self.end_headers()

            with open('reservationForm.html', 'rb') as file:
                    self.wfile.write(file.read())
        
        if self.path == ('/user/updateReservation'):
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)

            email = form_data.get("email", [None])[0]
            numGuests = form_data.get("guests", [None])[0]
            date = form_data.get("date", [None])[0]
            time = form_data.get("time", [None])[0]

            db = Database()
            db.update_reservation(numGuests, date, time, email)

            self.send_response(201)
            self.end_headers()

            with open('reservationForm.html', 'rb') as file:
                    self.wfile.write(file.read())

        if self.path == '/system/reservations':
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)

            self.send_response(201)
            self.end_headers()

            db = Database()
            reservationsData = db.fetch_allReservations()
            formatted_data = []
            for row in reservationsData:
                formatted_data.append({
                    'email': row[1],
                    'numGuests': row[2],
                    'date': row[3],
                    'time': row[4]
                })
            print("formatData", formatted_data)
            table_rows_html = ""
            for item in formatted_data:
                table_rows_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(item['email'], item['numGuests'], item['date'], item['time'])
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>All Reservations</title>
</head>
<body>
    <h1>All Reservations</h1>
    <table style="width:100%">
        <tr>
            <th>Email</th>
            <th>Number of Guests</th> 
            <th>Date</th>
            <th>Time</th>
        </tr>
        {}
    </table>
</body>
</html>
"""
            rendered_html = html_template.format(table_rows_html)
            self.wfile.write(rendered_html.encode())

            with open('systemReservations.html', 'rb') as file:
                    self.wfile.write(file.read())
            

    def do_PUT(self):
        if self.path.startswith('/user/reservation'):
            content_length = int(self.headers['content-Length'])
            get_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(get_data)
            db = Database()
            db.update_reservation();

            self.send_response(204)
            self.end_headers()


            self.send_response(201)
            self.end_headers()

        # if self.path.startswith('/user/reservations?'):
        #     reservation = str(self.path.split('/')[-1])
        #     content_length = int(self.headers['content-Length'])
        #     put_data = self.rfile.read(content_length).decode('utf-8')
        #     data = json.loads(put_data) 

        #     date, time, numOfGuest = "", "", ""

        #     date = data["date"]
        #     time = data["time"]
        #     numOfGuest = data["numOfGuest"]

        #     #password_bytes = password.encode('utf-8')
        #     salt = bcrypt.gensalt()
        #     #hashed = bcrypt.hashpw(password_bytes, salt)

        #     db = Database()
        #     #db.update_user(username, hashed, firstname, lastname, gender, bloodtype, dateofbirth, address, city, province, postalcode)

        #     self.send_response(200)
        #     self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/user/reservation'):
            db = Database()
            db.delete_reservation()

            self.send_response(204)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=NoteApiHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd server..')


if __name__ == '__main__':
    run()
