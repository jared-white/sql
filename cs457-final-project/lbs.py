# Jared White
# Python code for the library mangement system
# Utilizes the pscycopg library for connection with the PostgreSQL database

import psycopg
from psycopg import sql
import sys
from datetime import datetime

# Global variable that holds what the current sign in is
sign_in_selection = 0
need_log_in = True

class General_Functions():
    def __init__(self):
        pass

    def login_menu(self):
        print("== WASHOE COUNTY LIBRARY SYSTEM ==")
        print("=========== LOGIN ===========")
        print("1. Member Login")
        print("2. Librarian Login")
        print("3. Manager Login")

    def login_select(self):
        global sign_in_selection
        choice = True
        while choice == True:
            self.login_menu()
            print("Welcome! Please enter your login type.")
            selection = int(input(""))
            if selection == 1:
                sign_in_selection = 1
                Member().member_menu()
                choice = False
            elif selection == 2:
                sign_in_selection = 2
                Librarian().librarian_menu()
                choice = False
            elif selection == 3:
                sign_in_selection = 3
                Manager().manager_menu()
                choice = False
            else:
                print("Please select one of the given options.")
    
    def sign_out(self):
        print("You have successfully been signed out.")
        exit_choice = input("Would you like to exit the program? (y/n) ").lower().strip()
        if exit_choice == 'y':
            sys.exit()
        else:
            global need_log_in 
            need_log_in = True
            self.login_select()
    
    def check_id(self, user_id):
        global sign_in_selection
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                if sign_in_selection == 1:
                    cur.execute("""SELECT EXISTS(SELECT 1 FROM library_member WHERE member_id = %s)""", (user_id,))
                    id = cur.fetchone()[0]
                    return id
                elif sign_in_selection == 2 or sign_in_selection == 3:
                    cur.execute("""SELECT EXISTS(SELECT 1 FROM librarian WHERE librarian_id = %s)""", (user_id,))
                    id = cur.fetchone()[0]
                    return id
    
class Member():
    def __init__(self):
        pass

    def display_member_menu(self):
        print("=========== MEMBER MENU ===========")
        print("1. View Your Book Issues")
        print("2. View all Books in the Library")
        print("3. Search for a Book off of a Title or Word")
        print("0. Sign Out")
        print("===================================")

    def member_menu(self):
        global need_log_in
        while need_log_in:
            member_id = int(input("Please enter your member ID: "))
            if General_Functions().check_id(member_id):
                print("You have been signed in!")
                need_log_in = False
                break
            else:
                print("This ID does not exist. Please try again.")

        choice = True
        while choice == True:
            self.display_member_menu()
            selection = int(input("Please make a selection: "))
            if selection == 1:
                Issuing().member_view(member_id)
            elif selection == 2:
                Book_Management().member_view_books()
            elif selection == 3:
                Book_Management().member_search_for_book()
            elif selection == 0:
                General_Functions().sign_out()
                need_log_in = True
                choice = False
            else:
                print("Please select one of the given options.")

class Librarian():
    def __init__(self):
        pass

    def display_librarian_menu(self):
        print("=========== LIBRARIAN MENU ===========")
        print("1. Manage Issue Logs")
        print("2. Manage Book Inventory")
        print("3. Manage Members")
        print("0. Sign Out")
        print("======================================")

    def librarian_menu(self):
        global need_log_in
        while need_log_in:
            lib_id = int(input("Please enter your employee ID: "))
            if General_Functions().check_id(lib_id):
                print("You have been signed in!")
                need_log_in = False
                break
            else:
                print("This ID does not exist. Please try again.")

        choice = True
        while choice == True:
            self.display_librarian_menu()
            selection = int(input("Please make a selection: "))
            if selection == 1:
                Issuing().librarian_view_issue_logs()
            elif selection == 2:
                Book_Management().manage_book_menu()
            elif selection == 3:
                self.manage_member_menu()
            elif selection == 0:
                General_Functions().sign_out()
                choice = False
            else:
                print("Please select one of the given options.")

    def manage_member_menu(self):
        print("=========== MANAGE MEMBERS ===========")
        print("1. Add a Member")
        print("2. Edit a Member's Information")
        print("3. See List of Members")
        print("0. Back")
        print("=========================================")
        global sign_in_selection
        global need_log_in
        selection = int(input("Please make a selection: "))
        choice = True
        while choice == True:
            if selection == 1:
                Member_Management().add_member()
                choice = False
            elif selection == 2:
                Member_Management().edit_member()
                choice = False
            elif selection == 3:
                Member_Management().view_members()
                choice = False
            elif selection == 0:
                choice = False
                if sign_in_selection == 2:
                    self.librarian_menu()
                    need_log_in = False
                elif sign_in_selection == 3:
                    Manager().manager_menu()
                    need_log_in = False
            else:
                print("Please select one of the given options.")

class Manager():
    def display_manager_menu(self):
        print("============ MANAGER MENU ===========")
        print("1. Manage Librarians")
        print("2. Manage Members")
        print("3. Manage Book Inventory")
        print("4. Manage Issue Logs")
        print("0. Sign Out")
        print("=====================================")
    
    def manager_menu(self):
        global need_log_in
        while need_log_in:
            man_id = int(input("Please enter your employee ID: "))
            if General_Functions().check_id(man_id):
                print("You have been signed in!")
                need_log_in = False
                break
            else:
                print("This ID does not exist. Please try again.")

        choice = True
        while choice == True:
            self.display_manager_menu()
            selection = int(input("Please make a selection: "))
            if selection == 1:
                self.manage_librarian_options()
                choice = False
            elif selection == 2:
                Librarian().manage_member_menu()
                choice = False
            elif selection == 3:
                Book_Management().manage_book_menu()
                choice = False
            elif selection == 4:
                Issuing().manager_view_issue_logs()
                choice = False
            elif selection == 0:
                General_Functions().sign_out()
                choice = False
                need_log_in = True
            else:
                print("Please select one of the given options.")
        
    def manage_librarian_options(self):
        choice = True
        while choice == True:
            print("=========== MANAGE LIBRARIANS ===========")
            print("1. Add a Librarian")
            print("2. Edit a Librarian's Information")
            print("3. See List of Librarians")
            print("0. Back")
            print("=========================================")
            selection = int(input("Please make a selection: "))
            if selection == 1:
                Librarian_Management().add_librarian()
            elif selection == 2:
                Librarian_Management().edit_librarian()
            elif selection == 3:
                Librarian_Management().view_librarians()
            elif selection == 0:
                self.manager_menu()
                choice = False
            else:
                print("Please select one of the given options.")

class Issuing():
    def __init__(self):
        pass

    def new_book_issue(self):
        print("=========== NEW BOOK ISSUE ===========")
        book_id = int(input("Please enter the ID of the book you are issuing: "))
        librarian_id = int(input("Please enter your employee ID: "))
        member_id = int(input("Please enter the ID of the member this book is being issued to: "))
        branch_id = int(input("Please enter your branch ID: "))
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""INSERT INTO book_issue (book_id, branch_id) VALUES (%s, %s)""".format())
                        cur.execute(query, (book_id, branch_id))
                        conn.commit()
                        print("New book issue created for book with the following ID:", book_id)
                        cur.execute("SELECT issue_id FROM book_issue ORDER BY issue_id DESC LIMIT 1")
                        issue_id = cur.fetchone()[0]
                        query = sql.SQL("""INSERT INTO issue_log (issue_id, issued_by, issued_to, issue_time) 
                                        SELECT issue_id, {librarian_id}, {member_id}, added_at 
                                        FROM book_issue WHERE issue_id = {issue_id}""").format(
                                            librarian_id = sql.Literal(librarian_id), member_id = sql.Literal(member_id), issue_id = sql.Literal(issue_id))
                        cur.execute(query)
                        conn.commit()
                        cur.execute("SELECT log_id FROM issue_log ORDER BY log_id DESC LIMIT 1")
                        log_id = cur.fetchone()[0]
                        print("This issue has been added to the log with log ID {}.".format(log_id))
                        query = sql.SQL("""UPDATE book SET issue_status = true WHERE book_id = {book_id}""").format(
                            book_id = sql.Literal(book_id))
                        cur.execute(query)
                        conn.commit()

    def add_return_time(self):
        print("=========== RETURN A BOOK ===========")
        log_id = int(input("Pleae enter the log ID for which this book is being returned: "))
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE issue_log SET return_time = CURRENT_TIMESTAMP WHERE log_id = {log_id}""").format(
                            log_id = sql.Literal(log_id)
                        )
                        cur.execute(query)
                        conn.commit()
                        print("The return time has been logged.")
                        query = sql.SQL("""SELECT b.book_id FROM issue_log i JOIN book_issue b ON i.issue_id = b.issue_id WHERE i.log_id = {log_id}""").format(
                            log_id = sql.Literal(log_id)
                        )
                        cur.execute(query)
                        book_id = cur.fetchone()[0]
                        query = sql.SQL("""UPDATE book SET issue_status = false WHERE book_id = {book_id}""").format(
                            book_id = sql.Literal(book_id))
                        cur.execute(query)
                        conn.commit()
                        print("The book has been returned and its issued status has been reset.")

    def librarian_view_issue_logs(self):
        choice = True
        while choice == True:
            print("=========== MANAGE ISSUE LOGS ===========")
            print("1. View by Member")
            print("2. View by 'Not Returned'")
            print("3. View All")
            print("4. Check out a Book/Create New Issue")
            print("5. Return a Book")
            print("0. Back")
            selection = int(input("Please make a selection: "))
            if selection == 1:
                self.view_member_logs()
            elif selection == 2:
                self.view_not_returned_logs()
            elif selection == 3:
                self.view_all_logs()
            elif selection == 4:
                self.new_book_issue()
            elif selection == 5:
                self.add_return_time()
            elif selection == 0:
                choice == False
                Librarian().librarian_menu()
            else:
                print("Please select one of the given options.")

    def manager_view_issue_logs(self):
        choice = True
        while choice == True:
            print("=========== MANAGE ISSUE LOGS ===========")
            print("1. View by Member")
            print("2. View by Librarian")
            print("3. View by Branch")
            print("4. View by 'Not Returned'")
            print("5. View All")
            print("6. Check out a Book/Create New Issue")
            print("7. Return a Book")
            print("0. Back")
            selection = int(input("Please make a selection: "))
            if selection == 1:
                self.view_member_logs()
            elif selection == 2:
                self.view_librarian_logs()
            elif selection == 3:
                self.view_branch_logs()
            elif selection == 4:
                self.view_not_returned_logs()
            elif selection == 5:
                self.view_all_logs()
            elif selection == 6:
                self.new_book_issue()
            elif selection == 7:
                self.add_return_time()
            elif selection == 0:
                Manager().manager_menu()
                choice = False
            else:
                print("Please select one of the given options.")

    def view_all_logs(self):
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT i.log_id, lb.branch_name, bk.title as book_title, mem_first_name.first_name, mem_last_name.last_name, lib_first_name.first_name, lib_last_name.last_name, i.issue_time, i.return_time
                                FROM book_issue b
                                JOIN issue_log i ON b.issue_id = i.issue_id
                                JOIN book bk ON b.book_id = bk.book_id
                                JOIN library_branch lb ON b.branch_id = lb.branch_id
                                JOIN library_member mem_first_name ON mem_first_name.member_id = i.issued_to
                                JOIN library_member mem_last_name ON mem_last_name.member_id = i.issued_to
                                JOIN librarian lib_first_name ON lib_first_name.librarian_id = i.issued_by
                                JOIN librarian lib_last_name ON lib_last_name.librarian_id = i.issued_by""")
                cur.execute(query)
                print("=========== ALL ISSUES ===========")
                print("Log ID, Branch, Book Title, Member, Librarian, Issue Time, Return Time")
                rows = cur.fetchall()
                for row in rows:
                    formatted_issue_time = row[7].strftime("%Y-%m-%d %H:%M:%S")
                    formatted_return_time  = row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else "Not Returned"
                    member_name = row[3] + ' ' + row[4]
                    librarian_name = row[5] + ' ' + row[6]
                    print(row[0], row[1], row[2], member_name, librarian_name, formatted_issue_time, formatted_return_time, sep=', ')

    def view_not_returned_logs(self):
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""SELECT i.log_id, lb.branch_name, bk.title as book_title, mem_first_name.first_name, mem_last_name.last_name, lib_first_name.first_name, lib_last_name.last_name, i.issue_time
                                    FROM book_issue b
                                    JOIN issue_log i ON b.issue_id = i.issue_id
                                    JOIN book bk ON b.book_id = bk.book_id
                                    JOIN library_branch lb ON b.branch_id = lb.branch_id
                                    JOIN library_member mem_first_name ON mem_first_name.member_id = i.issued_to
                                    JOIN library_member mem_last_name ON mem_last_name.member_id = i.issued_to
                                    JOIN librarian lib_first_name ON lib_first_name.librarian_id = i.issued_by
                                    JOIN librarian lib_last_name ON lib_last_name.librarian_id = i.issued_by
                                    WHERE return_time IS NULL""")
                    print("=========== ISSUES NOT RETURNED YET ===========")
                    print("Log ID, Branch, Book Title, Member, Libraian, Issue Time")
                    cur.execute(query)
                    rows = cur.fetchall()
                    for row in rows:
                        formatted_issue_time = row[7].strftime("%Y-%m-%d %H:%M:%S")
                        member_name = row[3] + ' ' + row[4]
                        librarian_name = row[5] + ' ' + row[6]
                        print(row[0], row[1], row[2], member_name, librarian_name, formatted_issue_time, sep=', ')

    def view_branch_logs(self):
        branch_id = int(input("Please enter the branch ID: "))
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""SELECT i.log_id, bk.title as book_title, mem_first_name.first_name, mem_last_name.last_name, lib_first_name.first_name, lib_last_name.last_name, i.issue_time, i.return_time
                                    FROM book_issue b
                                    JOIN issue_log i ON b.issue_id = i.issue_id
                                    JOIN book bk ON b.book_id = bk.book_id
                                    JOIN library_branch lb ON b.branch_id = lb.branch_id
                                    JOIN library_member mem_first_name ON mem_first_name.member_id = i.issued_to
                                    JOIN library_member mem_last_name ON mem_last_name.member_id = i.issued_to
                                    JOIN librarian lib_first_name ON lib_first_name.librarian_id = i.issued_by
                                    JOIN librarian lib_last_name ON lib_last_name.librarian_id = i.issued_by
                                    WHERE b.branch_id = {branch_id}""").format(
                        branch_id = sql.Literal(branch_id))
                    print("=========== ISSUES AT BRANCH {} ===========".format(branch_id))
                    print("Log ID, Book Title, Member, Libraian, Issue Time, Return Time")
                    cur.execute(query)
                    rows = cur.fetchall()
                    for row in rows:
                        formatted_issue_time = row[6].strftime("%Y-%m-%d %H:%M:%S")
                        formatted_return_time  = row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else "Not Returned"
                        member_name = row[2] + ' ' + row[3]
                        librarian_name = row[4] + ' ' + row[5]
                        print(row[0], row[1], member_name, librarian_name, formatted_issue_time, formatted_return_time, sep=', ')

    def view_librarian_logs(self):
        lib_id = int(input("Please enter the librarian ID: "))
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""SELECT i.log_id, lb.branch_name, bk.title as book_title, mem_first_name.first_name, mem_last_name.last_name, i.issue_time, i.return_time
                                    FROM book_issue b
                                    JOIN issue_log i ON b.issue_id = i.issue_id
                                    JOIN book bk ON b.book_id = bk.book_id
                                    JOIN library_branch lb ON b.branch_id = lb.branch_id
                                    JOIN library_member mem_first_name ON mem_first_name.member_id = i.issued_to
                                    JOIN library_member mem_last_name ON mem_last_name.member_id = i.issued_to
                                    WHERE issued_by = {lib_id}""").format(
                        lib_id = sql.Literal(lib_id))
                    print("=========== ISSUES BY LIBRARIAN {} ===========".format(lib_id))
                    print("Log ID, Branch, Book Title, Member, Issue Time, Return Time")
                    cur.execute(query)
                    rows = cur.fetchall()
                    for row in rows:
                        formatted_issue_time = row[5].strftime("%Y-%m-%d %H:%M:%S")
                        formatted_return_time  = row[6].strftime("%Y-%m-%d %H:%M:%S") if row[6] else "Not Returned"
                        member_name = row[3] + ' ' + row[4]
                        print(row[0], row[1], row[2], member_name, formatted_issue_time, formatted_return_time, sep=', ')

    def view_member_logs(self):
        mem_id = int(input("Please enter the member ID: "))
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""SELECT i.log_id, lb.branch_name, bk.title as book_title,  lib_first_name.first_name, lib_last_name.last_name, i.issue_time, i.return_time
                                    FROM book_issue b
                                    JOIN issue_log i ON b.issue_id = i.issue_id
                                    JOIN book bk ON b.book_id = bk.book_id
                                    JOIN library_branch lb ON b.branch_id = lb.branch_id
                                    JOIN librarian lib_first_name ON lib_first_name.librarian_id = i.issued_by
                                    JOIN librarian lib_last_name ON lib_last_name.librarian_id = i.issued_by
                                    WHERE issued_to = {mem_id}""").format(
                        mem_id = sql.Literal(mem_id))
                    print("=========== ISSUES FOR MEMBER {} ===========".format(mem_id))
                    print("Log ID, Branch Name, Book Title, Librarian, Issue Time, Return Time")
                    cur.execute(query)
                    rows = cur.fetchall()
                    for row in rows:
                        formatted_issue_time = row[5].strftime("%Y-%m-%d %H:%M:%S")
                        formatted_return_time  = row[6].strftime("%Y-%m-%d %H:%M:%S") if row[6] else "Not Returned"
                        librarian_name = row[3] + ' ' + row[4]
                        print(row[0], row[1], row[2], librarian_name, formatted_issue_time, formatted_return_time, sep=', ')
    
    def member_view(self, id):
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""SELECT bk.title as book_title, lb.branch_name, lib_first_name.first_name, lib_last_name.last_name, i.issue_time, i.return_time
                                    FROM book_issue b
                                    JOIN issue_log i ON b.issue_id = i.issue_id
                                    JOIN book bk ON b.book_id = bk.book_id
                                    JOIN library_branch lb ON b.branch_id = lb.branch_id
                                    JOIN librarian lib_first_name ON lib_first_name.librarian_id = i.issued_by
                                    JOIN librarian lib_last_name ON lib_last_name.librarian_id = i.issued_by
                                    WHERE issued_to = {id}""").format(
                        id = sql.Literal(id))
                    print("=========== YOUR ISSUES ===========")
                    print("Book Title, Branch, Librarian, Issue Time, Return Time")
                    cur.execute(query)
                    rows = cur.fetchall()
                    for row in rows:
                        formatted_issue_time = row[4].strftime("%Y-%m-%d %H:%M:%S")
                        formatted_return_time  = row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else "Not Returned"
                        librarian_name = row[2] + ' ' + row[3]
                        print(row[0], row[1], librarian_name, formatted_issue_time, formatted_return_time, sep=', ')

class Librarian_Management():
    def __init__(self):
        pass

    def add_librarian(self):
        print("=========== ADD A LIBRARIAN ===========")
        first_name = input("Please enter the librarian's first name: ")
        last_name = input("Please enter the librarian's last name: ")
        branch_id = input("Please enter the branch ID for the branch the librarian works at: ")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""INSERT INTO librarian (first_name, last_name, branch_id) VALUES (%s,%s,%s)""".format())
                cur.execute(query, (first_name, last_name, branch_id))
                conn.commit()
    
    def edit_lib_menu(self):
        print("=========== EDIT A LIBRARIAN ===========")
        print("1. First Name")
        print("2. Last Name")
        print("3. Branch ID")
        print("4. Employment Status")
        print("0. Back")

    def edit_librarian(self):
        choice = True
        while choice == True:
            self.edit_lib_menu()
            selection = int(input("Please make a selection: "))
    
            if selection == 1:
                id = int(input("Please enter the ID number of the librarian you would like to edit: "))
                name = input("Please enter the corrected first name: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE librarian SET first_name = {name} WHERE librarian_id = {id} """).format(
                            name = sql.Literal(name), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("First name updated.")
                choice = False

            elif selection == 2:
                id = int(input("Please enter the ID number of the librarian you would like to edit: "))
                name = input("Please enter the corrected last name: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE librarian SET last_name = {name} WHERE librarian_id = {id} """).format(
                            name = sql.Literal(name), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Last name updated.")
                choice = False

            elif selection == 3:
                id = int(input("Please enter the ID number of the librarian you would like to edit: "))
                branch = input("Please enter the corrected branch ID: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE librarian SET branch_id = {branch} WHERE librarian_id = {id} """).format(
                            branch = sql.Literal(branch), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Branch ID updated.")
                choice = False
            
            elif selection == 4:
                id = int(input("Please enter the ID number of the librarian you would like to edit: "))
                status = input("Please enter 'True' for currently employed or 'False' for no longer employed: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE librarian SET employment_status = {status} WHERE librarian_id = {id} """).format(
                            status = sql.Literal(status), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Employment status updated.")
                choice = False

            elif selection == 0:
                Manager().manage_librarian_options()
                choice = False

            else:
                print("Please select one of the given options.")
    
    def view_librarians(self):
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT * FROM librarian ORDER BY last_name""")
                print("=========== LIBRARIANS ===========")
                print("Librarian ID, First Name, Last Name, Branch ID, Employment Status")
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    
class Member_Management():
    def __init__(self):
        pass

    def add_member(self):
        print("=========== ADD A MEMBER ===========")
        first_name = input("Please enter the member's first name: ")
        last_name = input("Please enter the member's last name: ")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""INSERT INTO library_member (first_name, last_name) VALUES (%s,%s)""".format())
                cur.execute(query, (first_name, last_name))
                conn.commit()
                print("This member has been added.")
                Librarian().manage_member_menu()
    
    def edit_mem_menu(self):
        print("=========== EDIT A MEMBER ===========")
        print("1. First Name")
        print("2. Last Name")
        print("3. Member Status")
        print("0. Back")

    def edit_member(self):
        global sign_in_selection
        choice = True
        while choice == True:
            self.edit_mem_menu()
            selection = int(input("Please make a selection: "))

            if selection == 1:
                id = int(input("Please enter the ID number of the member you would like to edit: "))
                name = input("Please enter the corrected first name: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE library_member SET first_name = {name} WHERE member_id = {id} """).format(
                            name = sql.Literal(name), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("First name updated.")

            elif selection == 2:
                id = int(input("Please enter the ID number of the member you would like to edit: "))
                name = input("Please enter the corrected last name: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE library_member SET last_name = {name} WHERE member_id = {id} """).format(
                            name = sql.Literal(name), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Last name updated.")

            elif selection == 3:
                id = int(input("Please enter the ID number of the member you would like to edit: "))
                status = input("Please enter 'True' for active or 'False' for inactive: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE library_member SET member_status = {status} WHERE member_id = {id} """).format(
                            status = sql.Literal(status), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Member status updated.")

            elif selection == 0:
                if sign_in_selection == 2:
                    Librarian().librarian_menu()
                elif sign_in_selection == 3:
                    Manager().manager_menu()
            
            else:
                print("Please select one of the given options.")
    
    def view_members(self):
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT * FROM library_member ORDER BY member_id ASC""")
                print("=========== MEMBERS ===========")
                print("First name, last name, member ID")
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    
class Book_Management():
    def __init__(self):
        pass

    def manage_book_menu(self):
        choice = True
        while choice == True:
            print("=========== MANAGE BOOK INVENTORY ===========")
            print("1. Add a New Book")
            print("2. Edit an Existing Book")
            print("3. Search for a Book")
            print("4. View All Books")
            print("0. Back")
            print("=============================================")
            selection = int(input("Please make a selection: "))
            if selection == 1:
                Book_Management().add_book()
            elif selection == 2:
                Book_Management().edit_book()
            elif selection == 3:
                Book_Management().employee_search_for_book()
            elif selection == 4:
                Book_Management().employee_view_books()
            elif selection == 0:
                choice = False
                if sign_in_selection == 2:
                    Librarian().librarian_menu()
                elif sign_in_selection == 3:
                    Manager().manager_menu()
            else:
                print("Please select one of the given options.")

    def add_book(self):
        # Set the following variables to none so if no value is given, it is inserted as NULL
        isbn = None
        num_pages = None
        lang = None
        publisher = None

        print("=========== ADD A BOOK ===========")
        title = input("Please enter the title of the book you need to add: ")
        author = input("Please enter the author(s) of the book: ")
        lang = input("*OPTIONAL* Please enter the language of the book (i.e. eng, fre, esp, etc.): ")
        num_pages = input("*OPTIONAL* Please enter the number of pages: ")
        publisher = input("*OPTIONAL* Please enter the publisher: ")
        isbn = input("*OPTIONAL* Please enter the ISBN: ")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                with conn.cursor() as cur:
                    query = sql.SQL("""INSERT INTO book (title, authors, isbn, language_code, num_pages, publisher) VALUES (%s,%s,%s,%s,%s,%s)""".format())
                    cur.execute(query, (title, author, isbn, lang, num_pages, publisher))
                    conn.commit()
                    cur.execute("SELECT book_id FROM book ORDER BY book_id DESC LIMIT 1")
                    book_id = cur.fetchone()[0]
        print("This book ({}) has been added to the library!".format(book_id))

    def edit_book_menu(self):
        print("=========== EDIT A BOOK ===========")
        print("1. Title")
        print("2. Author(s)")
        print("3. ISBN")
        print("4. Language")
        print("5. Number of Pages")
        print("6. Publisher")
        print("0. Back")

    def edit_book(self):
        global sign_in_selection
        choice = True
        while choice == True:
            self.edit_book_menu()
            selection = int(input("Please make a selection: "))

            if selection == 1:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                title = input("Please enter the corrected title: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET title = {title} WHERE book_id = {id} """).format(
                            title = sql.Literal(title), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Title updated.")

            elif selection == 2:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                author = input("Please enter the corrected author(s): ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET authors = {author} WHERE book_id = {id} """).format(
                            author = sql.Literal(author), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Author(s) updated.")

            elif selection == 3:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                isbn = input("Please enter the ISBN: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET isbn = {isbn} WHERE book_id = {id} """).format(
                            isbn = sql.Literal(isbn), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("ISBN updated.")
            
            elif selection == 4:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                lang = input("Please enter the language (i.e., eng, esp, fre, etc.): ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET language_code = {lang} WHERE book_id = {id} """).format(
                            lang = sql.Literal(lang), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Language updated.")

            elif selection == 5:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                num_pages = input("Please enter the number of pages: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET num_pages = {num_pages} WHERE book_id = {id} """).format(
                            num_pages = sql.Literal(num_pages), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Number of pages updated.")

            elif selection == 6:
                id = int(input("Please enter the ID number of the book you would like to edit: "))
                publisher = input("Please enter the publisher: ")
                with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
                    with conn.cursor() as cur:
                        query = sql.SQL("""UPDATE book SET publisher = {publisher} WHERE book_id = {id} """).format(
                            publisher = sql.Literal(publisher), id = sql.Literal(id))
                        cur.execute(query)
                        conn.commit()
                print("Publisher updated.")

            elif selection == 0:
                choice = False
                if sign_in_selection == 2:
                    Librarian().librarian_menu()
                elif sign_in_selection == 3:
                    Manager().manager_menu()

            else:
                print("Please select one of the given options.")

    def employee_view_books(self):
        print("=========== BOOKS ===========")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT * FROM book ORDER BY book_id ASC""")
                cur.execute(query)
                print("Book ID, Title, Author(s), ISBN, Language Code, Number of Pages, Publisher, Issue Status")
                rows = cur.fetchall()
                for i, row in enumerate(rows, start=1):
                    print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], sep=', ')
                    if i % 200 == 0:
                        user_input = input("Hit enter to show more or 'q' to quit ")
                        if user_input.lower() == 'q':
                            break

    def member_view_books(self):
        print("=========== BOOKS ===========")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT book_id, title, authors, language_code, num_pages FROM book ORDER BY book_id ASC""")
                cur.execute(query)
                print("Book ID, Title, Author(s), Language Code, Number of Pages")
                rows = cur.fetchall()
                for i, row in enumerate(rows, start=1):
                    print(row[0], row[1], row[2], row[3], row[4], sep=', ')
                    if i % 200 == 0:
                        user_input = input("Hit enter to show more or 'q' to quit ")
                        if user_input.lower() == 'q':
                            break

    def employee_search_for_book(self):
        print("=========== BOOK SEARCH ===========")
        word = input("Please enter the title or phrase/word in a title you would like to search for: ")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT * FROM book WHERE title ILIKE '%' || {} || '%'""").format(sql.Literal(word))
                cur.execute(query)
                print("Book ID, Title, Author(s), ISBN, Language Code, Number of Pages, Publisher, Issue Status")
                rows = cur.fetchall()
                for row in rows:
                    print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], sep=', ')

    def member_search_for_book(self):
        print("=========== BOOK SEARCH ===========")
        word = input("Please enter the title or phrase/word in a title you would like to search for: ")
        with psycopg.connect("dbname=final_project user=postgres password=0520") as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT book_id, title, authors, language_code, num_pages FROM book WHERE title ILIKE '%' || {} || '%'""").format(sql.Literal(word))
                cur.execute(query)
                print("Book ID, Title, Author(s), Language Code, Number of Pages")
                rows = cur.fetchall()
                for row in rows:
                    print(row[0], row[1], row[2], row[3], row[4], sep=', ')

def main():
    General_Functions().login_select()

if __name__ == '__main__':
    main()