"""
    @file   direct_work_database.py
    @brief
        Handling direct conflict process including database.
"""

import pymysql
import datetime as d
from server_dir.slack_message_sender import *
from server_dir.conflict_flag_enum import Conflict_flag
from chat_bot_server_dir.work_database import work_database
from server_dir.server_config_loader import load_database_connection_config
import itertools
import json

class direct_work_database:
    # Constructor
    def __init__(self):
        # Load mysql database connection config
        host, user, password, db, charset = load_database_connection_config()

        # get mysql database connection
        self.conn = pymysql.connect(host     = host,
                                    user     = user,
                                    password = password,
                                    db       = db,
                                    charset  = charset)

        # get cursor
        self.cursor = self.conn.cursor()

    # Delete User working data
    def delete_user_data(self, user_name):
        try:
            sql = "delete " \
                  "from working_table " \
                  "where user_name = '%s'" % (user_name)

            # execute sql
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            self.conn.rollback()
            print("ERROR : delete user data")

        return

    # Detect Direct Conflict
    def detect_direct_conflict(self, project_name, working_list, user_name):
        print("\n" + "#### START detect direct conflict logic ####")
        w_db = work_database()

        self.delete_direct_conflict_list()

        remove_lock_list = w_db.prev_remove_lock_list()
        if remove_lock_list:
            message = get_message('feat_send_all_user_auto_unlock.txt').format(file_name=", ".join(remove_lock_list))
            send_all_user_message(message)
            # send_remove_lock_channel("code-conflict-chatbot", remove_lock_list)
        w_db.auto_remove_lock_list()

        user_slack_code = w_db.convert_git_id_to_slack_code(user_name)
        inform_unlock_list = w_db.read_oldest_lock_history_list(user_slack_code, remove_lock_list)
        for file in inform_unlock_list:
            if(user_slack_code != file[2]):
                send_lock_request_button_message(file[2], file[1], file[3])

        lock_file_list = w_db.inform_lock_file_direct(project_name, working_list, user_name)
        lock_noticed_user_list = w_db.check_lock_noticed_user(project_name, lock_file_list, user_name)

        # final lock_file_list 뽑아내는거 함수로 구현하기. / indirect도
        if lock_file_list and not lock_noticed_user_list:
            send_lock_message(lock_file_list, user_name)
            w_db.add_lock_notice_list(project_name, lock_file_list, user_name)

        elif lock_file_list and lock_noticed_user_list:
            already_noticed_lock_file_list = []
            for lfl in lock_file_list:
                for lnul in lock_noticed_user_list:
                   if lfl[1] == lnul[1]:
                       already_noticed_lock_file_list.append(lfl)

            for anlfl in already_noticed_lock_file_list:
                lock_file_list.remove(anlfl)

            if lock_file_list:
                send_lock_message(lock_file_list, user_name)
                w_db.add_lock_notice_list(project_name, lock_file_list, user_name)

        print("working list : ", working_list)

        slack_code =  w_db.convert_git_id_to_slack_code(user_name)

        direct_conflict_list = self.search_working_table(project_name, working_list, user_name)
        # direct_conflict_list, approve_file_list = w_db.classify_direct_conflict_approved_list(slack_code, direct_conflict_list)
        w_db.close()

        print("direct_conflict_list : ", direct_conflict_list)

        # Conflict
        if direct_conflict_list:

            print("\n#### Direct Conflict !!! ####")

            already_direct_conflict_table = self. search_already_direct_conflict_list(project_name, direct_conflict_list, working_list, user_name)
            first_direct_conflict_list, already_direct_conflict_list = self.classify_direct_conflict_list(direct_conflict_list, already_direct_conflict_table)
            print("already_direct_conflict_table : ", already_direct_conflict_table)
            print("first_direct_conflict_list : ", first_direct_conflict_list)
            print("already_direct_conflict_list : ", already_direct_conflict_list)

            # Already conflicted
            if already_direct_conflict_table:

                print("\n#### Already Direct Conflict !!! ####")

                # Search the best value of severity and return list
                best_direct_conflict_list = self.search_best_direct_conflict(project_name, already_direct_conflict_list, working_list, user_name)

                # Compare current conflict and database conflict
                # Send the conflict message
                # Update conflict database
                self.compare_current_direct_conflict_and_db(already_direct_conflict_table, best_direct_conflict_list)

            # First conflict
            if first_direct_conflict_list:

                print("\n#### First Direct Conflict !!! ####")

                # Search the best value of severity and return list
                best_direct_conflict_list = self.search_best_direct_conflict(project_name, first_direct_conflict_list, working_list, user_name)
                self.update_first_best_conflict_list(best_direct_conflict_list)

        # Non-conflict
        non_direct_conflict_list = self.search_non_direct_conflict_list(project_name, user_name, direct_conflict_list)
        print("non_direct_conflict_list : ", non_direct_conflict_list)

        if non_direct_conflict_list:
            print("\n#### Non-Direct Conflict !!! ####")
            self.non_direct_conflict_logic(project_name, user_name, non_direct_conflict_list)

        return

    # Delete conflict list
    def delete_direct_conflict_list(self):
        try:
            sql = "delete " \
                  "from direct_conflict_table " \
                  "where alert_count >= 3 " \
                  "and TIMEDIFF(now(),log_time) > 24*60*60"
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            self.conn.rollback()
            print("ERROR : delete direct conflict list")

        return

    # Search same project and same file from working table
    def search_working_table(self, project_name, working_list, user_name):

        all_raw_set = set()

        # ["file_name", "logic_name", "work_line", "work_amount"]
        for temp_work in working_list:
            if temp_work[3] == -1:
                temp_work[1] = "in"
            try:
                sql = "select * " \
                      "from working_table " \
                      "where project_name = '%s' " \
                      "and file_name = '%s' " \
                      "and user_name != '%s'" % (project_name, temp_work[0], user_name)
                print(sql)
                self.cursor.execute(sql)
                self.conn.commit()

                raw_list = list(self.cursor.fetchall())
                for raw in raw_list:
                    all_raw_set.add(raw)
                print ("select from working_table : ", raw_list)

            except:
                self.conn.rollback()
                print("ERROR : search working table")

        return list(all_raw_set)

    def search_non_direct_conflict_list(self, project_name, user_name, direct_conflict_list):
        non_direct_conflict_list = []

        try:
            sql = "select * " \
                  "from direct_conflict_table " \
                  "where project_name = '%s' " \
                  "and user1_name = '%s'" % (project_name, user_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_list = list(self.cursor.fetchall())
            non_direct_conflict_list = raw_list[:]

            # [ project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, alert_count, severity, log_time ]
            for rl in raw_list:
                # [ project_name, file_name, logic_name, user_name, work_line, work_amount, log_time ]
                for dcl in direct_conflict_list:
                    if rl[1] == dcl[1] and rl[3] == dcl[2] and rl[5] == dcl[3] and rl[4] == user_name:
                        non_direct_conflict_list.remove(rl)

        except:
            self.conn.rollback()
            print("ERROR : search non direct conflict list")

        return non_direct_conflict_list

    def search_already_direct_conflict_list(self, project_name, conflict_list, working_list, user_name):
        all_raw_set = set()

        # [ project_name, file_name, logic_name, user_name, work_line, work_amount, log_time]
        for temp_other_work in conflict_list:
            # ["file_name", "logic_name", "work_line", "work_amount"]
            for temp_user_work in working_list:
                try:
                    sql = "select * " \
                          "from direct_conflict_table " \
                          "where project_name = '%s' " \
                          "and file_name = '%s' " \
                          "and user1_name = '%s' " \
                          "and user2_name = '%s'" % (project_name, temp_user_work[0], user_name, temp_other_work[3])
                    print(sql)
                    self.cursor.execute(sql)
                    self.conn.commit()

                    raw_list = list(set(self.cursor.fetchall()))
                    for raw in raw_list:
                        all_raw_set.add(raw)

                except:
                    self.conn.rollback()
                    print("ERROR : search already direct conflict table")

        all_raw_list = list(all_raw_set)

        return all_raw_list

    def classify_direct_conflict_list(self, whole_direct_conflict_list, already_direct_conflict_table):
        # first_direct_conflict_list = whole_direct_conflict_list - already_direct_conflict_list
        first_direct_conflict_list = whole_direct_conflict_list[:]
        already_direct_conflict_list = []
        # [ project_name, file_name, logic_name, user_name, work_line, work_amount, log_time ]
        for temp_whole_direct_conflict_list in whole_direct_conflict_list:
            # [ project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, alert_count, severity, log_time ]
            for temp_already_direct_conflict_table in already_direct_conflict_table:
                if (temp_whole_direct_conflict_list[0] == temp_already_direct_conflict_table[0] and
                        temp_whole_direct_conflict_list[1] == temp_already_direct_conflict_table[1] and
                        temp_whole_direct_conflict_list[3] == temp_already_direct_conflict_table[5]):
                    already_direct_conflict_list.append(temp_whole_direct_conflict_list)
                    first_direct_conflict_list.remove(temp_whole_direct_conflict_list)
                    break

        return first_direct_conflict_list, already_direct_conflict_list

    def search_best_direct_conflict(self, project_name, conflict_list, working_list, user_name):
        best_direct_conflict_dict = dict()
        all_severity_list = []

        # working_list == this user's work.
        # conflict_list == other users' work.
        # [ project_name, file_name, logic_name, user_name, work_line, work_amount, log_time ]
        for temp_other_work in conflict_list:
            # [ file_name, logic_name, work_line, work_amount ]
            for temp_user_work in working_list:
                # Same file name
                if temp_other_work[1] == temp_user_work[0]:
                    # Calculate severity of the current conflict
                    # Same logic name => search best conflict
                    if temp_other_work[2] == temp_user_work[1]:
                        if temp_user_work[1][:8] == "function":
                            print("same function direct conflict : 3")
                            severity = 3
                        elif temp_user_work[1][:5] == "class":
                            print("same def in same class direct conflict : 3")
                            severity = 3
                        else:
                            print("same in direct conflict : 1")
                            severity = 1
                    # Different logic name
                    else:
                        if ((temp_user_work[1][:5] == "class") and (temp_other_work[2][:5] == "class")
                        and (temp_user_work[1].split(':')[1] == temp_other_work[2].split(':')[1])):
                            print("same class direct conflict : 2")
                            severity = 2
                        else:
                            print("just in direct conflict : 1")
                            severity = 1

                    # key: file name / key: other user's name / value: severity conflict list
                    temp_conflict_list = []
                    temp_conflict_list.append(severity)
                    temp_conflict_list.append(project_name)  # project_name
                    temp_conflict_list.append(temp_user_work[0])  # file_name
                    temp_conflict_list.append(temp_user_work[1])  # logic1_name
                    temp_conflict_list.append(temp_other_work[2])  # logic2_name
                    temp_conflict_list.append(user_name)  # user1_name
                    temp_conflict_list.append(temp_other_work[3])  # user2_name

                    if temp_user_work[0] in best_direct_conflict_dict:
                        if temp_other_work[3] in best_direct_conflict_dict[temp_user_work[0]]:
                            best_direct_conflict_dict[temp_user_work[0]][temp_other_work[3]].append(temp_conflict_list)

                        else:
                            best_direct_conflict_dict[temp_user_work[0]][temp_other_work[3]] = []
                            best_direct_conflict_dict[temp_user_work[0]][temp_other_work[3]].append(temp_conflict_list)

                    else:
                        best_direct_conflict_dict[temp_user_work[0]] = dict()
                        best_direct_conflict_dict[temp_user_work[0]][temp_other_work[3]] = []
                        best_direct_conflict_dict[temp_user_work[0]][temp_other_work[3]].append(temp_conflict_list)

        print("best_direct_conflict_dict : ", best_direct_conflict_dict)

        for temp_key in best_direct_conflict_dict.keys():
            for user_key in best_direct_conflict_dict[temp_key].keys():
                temp_best_conflict = max(best_direct_conflict_dict[temp_key][user_key])
                print("temp_key : ", temp_key, "\nuser_key : ", user_key, "\nmax : ", temp_best_conflict)
                all_severity_list.append(temp_best_conflict)

        return all_severity_list

    def compare_current_direct_conflict_and_db(self, already_direct_conflict_list, best_direct_conflict_list):
        # [project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, alert_count, severity, log_time]
        for temp_already in already_direct_conflict_list:
            # [severity, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name]
            for temp_best in best_direct_conflict_list:
                conflict_flag = 0
                severity_flag = 0

                # Compare severity
                # same user and same project and same logic
                if temp_already[0] == temp_best[1] and temp_already[1] == temp_best[2] and temp_already[5] == temp_best[6]:
                    user_percentage, other_percentage = self.calculate_percentage(temp_best)
                    current_percentage = round((user_percentage + other_percentage) / 2, 2)
                    previous_percentage = round(self.get_percentage_of_direct_conflict(temp_best), 2)

                    # Severity_percentage
                    # Criterion : 5 %
                    if abs(current_percentage - previous_percentage) > 5:
                        if current_percentage > previous_percentage:
                            print("direct : getting severity_percentage")
                            conflict_flag = Conflict_flag.getting_severity_percentage.value

                        else:
                            print("direct : lower severity_percentage")
                            conflict_flag = Conflict_flag.lower_severity_percentage.value

                    else:
                        print("direct : same severity_percentage")
                        conflict_flag = Conflict_flag.same_severity_percentage.value

                    # Severity Position
                    if temp_already[7] < temp_best[0]:
                        print("direct : getting severity")
                        severity_flag = Conflict_flag.getting_severity.value

                    elif temp_already[7] > temp_best[0]:
                        print("direct lower severity")
                        severity_flag = Conflict_flag.lower_severity.value

                    elif temp_already[7] == temp_best[0]:
                        print("direct same severity")
                        severity_flag = Conflict_flag.same_severity.value

                    if conflict_flag != 0 and not (conflict_flag == 7 and severity_flag == 4):
                        send_direct_conflict_message(conflict_flag=conflict_flag,
                                                     conflict_project=temp_best[1],
                                                     conflict_file=temp_best[2],
                                                     conflict_logic=temp_best[3],
                                                     user1_name=temp_best[5],
                                                     user2_name=temp_best[6],
                                                     user1_percentage=user_percentage,
                                                     user2_percentage=other_percentage,
                                                     previous_percentage=previous_percentage,
                                                     current_severity=temp_best[0],
                                                     severity_flag=severity_flag)

                        self.update_conflict_data(project_name=temp_best[1],
                                                  file_name=temp_best[2],
                                                  logic1_name=temp_best[3],
                                                  logic2_name=temp_best[4],
                                                  user1_name=temp_best[5],
                                                  user2_name=temp_best[6],
                                                  severity=temp_best[0],
                                                  severity_percentage=current_percentage)

                    # After 30 minutes => send direct message
                    if ((d.datetime.today() - temp_already[9] > d.timedelta(minutes=30))
                        and (temp_already[6] == 1) and (conflict_flag == Conflict_flag.same_severity.value)):
                        send_direct_conflict_message(conflict_flag=conflict_flag,
                                                     conflict_project=temp_best[1],
                                                     conflict_file=temp_best[2],
                                                     conflict_logic=temp_best[3],
                                                     user1_name=temp_best[5],
                                                     user2_name=temp_best[6])

                        self.increase_alert_count(project_name=temp_best[1],
                                                  file_name=temp_best[2],
                                                  logic1_name=temp_best[3],
                                                  logic2_name=temp_best[4],
                                                  user1_name=temp_best[5],
                                                  user2_name=temp_best[6])

                    # After 60 minutes => send channel message
                    # elif((d.datetime.today() - temp_already[8] > d.timedelta(minutes=60))
                    #     and (temp_already[6] == 2)
                    #     and (conflict_flag == Conflict_flag.same_severity.value)):
                    #     send_conflict_message_channel(conflict_file=temp_best[2],
                    #                                   conflict_logic=temp_best[3],
                    #                                   user1_name=temp_best[5],
                    #                                   user2_name=temp_best[6])
                    #     self.increase_alert_count(project_name=temp_best[1],
                    #                               file_name=temp_best[2],
                    #                               logic1_name=temp_best[3],
                    #                               logic2_name=temp_best[4],
                    #                               user1_name=temp_best[5],
                    #                               user2_name=temp_best[6])
                    #
                    #     self.increase_alert_count(project_name=temp_best[1],
                    #                               file_name=temp_best[2],
                    #                               logic1_name=temp_best[4],
                    #                               logic2_name=temp_best[3],
                    #                               user1_name=temp_best[6],
                    #                               user2_name=temp_best[5])

        return

    def update_first_best_conflict_list(self, best_conflict_list):
        # [severity, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name]
        print("#### update first best conflict list #####")
        print(best_conflict_list)
        for temp_best in best_conflict_list:
          #  user_percentage, other_percentage = self.calculate_percentage(temp_best)
            user_percentage=0
            other_percentage=0
            self.insert_conflict_data(project_name=temp_best[1],
                                      file_name=temp_best[2],
                                      logic1_name=temp_best[3],
                                      logic2_name=temp_best[4],
                                      user1_name=temp_best[5],
                                      user2_name=temp_best[6],
                                      severity=temp_best[0],
                                      severity_percentage=round((user_percentage + other_percentage) / 2, 2))

            if(temp_best[3] == temp_best[4]
                and temp_best[3][:5] == "class"
                and temp_best[4][:5] == "class"):
                # same class and same function
                conflict_flag = Conflict_flag.same_function.value

            elif(temp_best[3] == temp_best[4]
                and temp_best[3][:8] == "function"
                and temp_best[4][:8] == "function"):
                # same function
                conflict_flag = Conflict_flag.same_function.value

            elif(temp_best[3] != temp_best[4]
                and temp_best[3][:5] == "class"
                and temp_best[4][:5] == "class"
                and temp_best[3].split(':')[1] == temp_best[4].split(':')[1]):
                # just same class
                conflict_flag = Conflict_flag.same_class.value

            else:
                # just in
                conflict_flag = Conflict_flag.file_in.value

            send_direct_conflict_message(conflict_flag=conflict_flag,
                                         conflict_project=temp_best[1],
                                         conflict_file=temp_best[2],
                                         conflict_logic=temp_best[3],
                                         user1_name=temp_best[5],
                                         user2_name=temp_best[6],
                                         user1_percentage=user_percentage,
                                         user2_percentage=other_percentage)

        return

    def calculate_percentage(self, best_conflict):
        user_edit_amount = tuple()
        other_edit_amount = tuple()
        file_total_lines = tuple()

        try:
            sql = "select total_plus, total_minus " \
                  "from edit_amount " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  "and user_name = '%s'" \
                  % (best_conflict[1], best_conflict[2], best_conflict[5])

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            user_edit_amount = self.cursor.fetchone()

        except:
            self.conn.rollback()
            print("ERROR : update first best conflict list")

        try:
            sql = "select total_plus, total_minus " \
                  "from edit_amount " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  "and user_name = '%s'" \
                  % (best_conflict[1], best_conflict[2], best_conflict[6])

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            other_edit_amount = self.cursor.fetchone()

        except:
            self.conn.rollback()
            print("ERROR : update first best conflict list")

        try:
            sql = "select total_lines " \
                  "from file_information " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  % (best_conflict[1], best_conflict[2])

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            file_total_lines = self.cursor.fetchone()

        except:
            self.conn.rollback()
            print("ERROR : update first best conflict list")

        user_percentage = 0

        if user_edit_amount[0] == 0:
            user_percentage = (100 * user_edit_amount[1]) / file_total_lines[0]
        elif user_edit_amount[1] == 0:
            user_percentage = (100 * user_edit_amount[0]) / (file_total_lines[0] + user_edit_amount[0])
        elif user_edit_amount[0] > user_edit_amount[1]:
            user_percentage = (100 * user_edit_amount[0]) / (file_total_lines[0] + user_edit_amount[0] - user_edit_amount[1])
        elif user_edit_amount[0] <= user_edit_amount[1]:
            user_percentage = (100 * user_edit_amount[1]) / (file_total_lines[0])

        other_percentage = 0

        if other_edit_amount[0] == 0:
            other_percentage = (100 * other_edit_amount[1]) / file_total_lines[0]
        elif other_edit_amount[1] == 0:
            other_percentage = (100 * other_edit_amount[0]) / (file_total_lines[0] + other_edit_amount[0])
        elif other_edit_amount[0] > other_edit_amount[1]:
            other_percentage = (100 * other_edit_amount[0]) / (file_total_lines[0] + other_edit_amount[0] - other_edit_amount[1])
        elif other_edit_amount[0] <= other_edit_amount[1]:
            other_percentage = (100 * other_edit_amount[1]) / (file_total_lines[0])

        return round(user_percentage, 2), round(other_percentage, 2)

    def get_percentage_of_direct_conflict(self, best_conflict):
        # best_conflict
        # [severity, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name]
        try:
            sql = "select severity_percentage " \
                  "from direct_conflict_table " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  "and user1_name = '%s' " \
                  "and user2_name = '%s'" \
                  % (best_conflict[1], best_conflict[2], best_conflict[5], best_conflict[6])

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            percentage_of_direct_conflict = self.cursor.fetchone()

        except:
            self.conn.rollback()
            print("ERROR : update first best conflict list")

        return percentage_of_direct_conflict[0]

    def non_direct_conflict_logic(self, project_name, user_name, non_direct_conflict_list):
        print("non_direct_conflict_logic : ", non_direct_conflict_list)

        # [ project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, alert_count, severity, log_time ]
        for raw_temp in non_direct_conflict_list:

            send_direct_conflict_message(conflict_flag=Conflict_flag.direct_conflict_finished.value,
                                         conflict_project=project_name,
                                         conflict_file=raw_temp[1],
                                         conflict_logic=raw_temp[2],
                                         user1_name=user_name,
                                         user2_name=raw_temp[5])

            send_direct_conflict_message(conflict_flag=Conflict_flag.direct_conflict_finished.value,
                                         conflict_project=project_name,
                                         conflict_file=raw_temp[1],
                                         conflict_logic=raw_temp[2],
                                         user1_name=raw_temp[5],
                                         user2_name=user_name)

        # [ project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, alert_count, severity, log_time ]
        for ndcl in non_direct_conflict_list:
            try:
                sql = "delete " \
                      "from direct_conflict_table " \
                      "where project_name = '%s' " \
                      "and file_name = '%s' " \
                      "and logic1_name = '%s' " \
                      "and logic2_name = '%s' " \
                      "and user1_name = '%s' " \
                      "and user2_name = '%s' " \
                      % (ndcl[0], ndcl[1], ndcl[2], ndcl[3], ndcl[4], ndcl[5])
                print(sql)
                self.cursor.execute(sql)
                self.conn.commit()

            except:
                self.conn.rollback()
                print("ERROR : delete user direct conflict data1")

            try:
                sql = "delete " \
                      "from direct_conflict_table " \
                      "where project_name = '%s' " \
                      "and file_name = '%s' " \
                      "and logic1_name = '%s' " \
                      "and logic2_name = '%s' " \
                      "and user1_name = '%s' " \
                      "and user2_name = '%s' " \
                      % (ndcl[0], ndcl[1], ndcl[3], ndcl[2], ndcl[5], ndcl[4])
                print(sql)
                self.cursor.execute(sql)
                self.conn.commit()

            except:
                self.conn.rollback()
                print("ERROR : delete user direct conflict data2")

        return

    # Insert User data to working_table
    def insert_user_data(self, project_name, working_list, user_name):
        for temp_work in working_list:
            print("temp_work : ",temp_work)
            try:
                if temp_work[3] == -1:
                    temp_work[1] = "in"
                sql = "insert into working_table " \
                      "(project_name, file_name, logic_name, user_name, work_line, work_amount) " \
                      "value ('%s', '%s', '%s', '%s', %d, %d)" % (project_name, temp_work[0], temp_work[1], user_name, temp_work[2], temp_work[3])
                print(sql)
                self.cursor.execute(sql)
                self.conn.commit()
            except:
                self.conn.rollback()
                print("ERROR : insert user data")


    # Insert conflict data
    def insert_conflict_data(self, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, severity, severity_percentage):
        try:
            if "in" == logic1_name or "in" == logic2_name:
                severity = 1
            sql = "insert into direct_conflict_table " \
                  "(project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, severity, severity_percentage) " \
                  "value ('%s', '%s', '%s', '%s', '%s', '%s', %d, %f)" % (project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, severity, severity_percentage)
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("ERROR : insert direct conflict data")

        return

    # update conflict data
    def update_conflict_data(self, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name, severity, severity_percentage):
        try:
            sql = "update direct_conflict_table " \
                  "set logic1_name = '%s', logic2_name = '%s', severity = %d, severity_percentage = %f " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  "and user1_name = '%s' " \
                  "and user2_name = '%s'" % (logic1_name, logic2_name, severity, severity_percentage, project_name, file_name, user1_name, user2_name)
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("ERROR : update direct direct_conflict_table")

        return

    def increase_alert_count(self, project_name, file_name, logic1_name, logic2_name, user1_name, user2_name):
        try:
            sql = "update direct_conflict_table " \
                  "set alert_count = alert_count + 1 " \
                  "where project_name = '%s' " \
                  "and file_name = '%s' " \
                  "and logic1_name = '%s' " \
                  "and logic2_name = '%s' " \
                  "and user1_name = '%s' " \
                  "and user2_name = '%s'" % (project_name, file_name, logic1_name, logic2_name, user1_name, user2_name)
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("ERROR : increase direct alert count")

        return

    # prediction part
    def check_necessity_prediction(self, project_name, working_list, user_name):
        user_working_db = set()

        try:
            sql = "select file_name " \
                  "from working_table " \
                  "where project_name = '%s' " \
                  "and user_name = '%s'" % (project_name, user_name)
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_tuple = self.cursor.fetchall()
            for raw in raw_tuple:
                user_working_db.add(raw[0])

        except:
            self.conn.rollback()
            print("ERROR : check_necessity_prediction")

        current_working_db = set()

        for temp_work in working_list:
            current_working_db.add(temp_work[0])

        if current_working_db - user_working_db:
            return True
        else:
            return False

    def get_git_log_name_only(self, project_name):
        log_file_list = []

        try:
            sql = "select * " \
                  "from git_log_name_only " \
                  "where project_name = '%s'" % (project_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_list = list(self.cursor.fetchall())
            for raw in raw_list:
                log_file_list.append(set(json.loads(raw[2])))

        except:
            self.conn.rollback()
            print("ERROR : get_git_log_name_only")

        return log_file_list

    def predict_conflict(self, project_name, user_name):
        git_log_name_only_list = self.get_git_log_name_only(project_name)
        user_working_file_set = self.get_user_working_file(project_name, user_name)
        other_user_working_file_dict = self.get_other_user_working_file(project_name, user_name)

        user_related_row = self.get_user_related_row(git_log_name_only_list, user_working_file_set)
        num_user_related_row = len(user_related_row)
        related_file_set_dict = self.get_related_file_set_dict(git_log_name_only_list, user_working_file_set)
        user_combination_row = self.make_combination(user_related_row, user_working_file_set)
        user_combination_row_set = set(user_combination_row)

        probability_dict = dict()
        probability_per_file_dict = dict()
        probability_per_file_dict['all'] = dict()
        # Using only for check
        both_user_working_file_dict = dict()
        both_user_combination_row_dict = dict()
        other_user_related_row_dict = dict()
        num_other_user_related_row_dict = dict()
        other_user_combination_row_dict = dict()
        other_user_combination_row_set_dict = dict()
        for other_user, other_user_working_file_set in other_user_working_file_dict.items():
            both_user_working_file_dict[other_user] = []
            both_user_working_file_dict[other_user].append(user_working_file_set & other_user_working_file_dict[other_user])
            both_user_combination_row_dict[other_user] = set(self.make_combination(both_user_working_file_dict[other_user]))

            other_user_related_row_dict[other_user] = self.get_user_related_row(git_log_name_only_list, other_user_working_file_set)
            num_other_user_related_row_dict[other_user] = len(other_user_related_row_dict[other_user])
            other_user_combination_row_dict[other_user] = self.make_combination(other_user_related_row_dict[other_user], other_user_working_file_dict[other_user])
            other_user_combination_row_set_dict[other_user] = set(other_user_combination_row_dict[other_user])
            probability_per_file_dict[other_user] = dict()
            probability_dict[other_user] = self.calculate_probability(num_user_related_row,
                                                                      num_other_user_related_row_dict[other_user],
                                                                      user_combination_row,
                                                                      other_user_combination_row_dict[other_user],
                                                                      (user_combination_row_set &
                                                                       other_user_combination_row_set_dict[
                                                                           other_user]) -
                                                                      both_user_combination_row_dict[other_user],
                                                                      probability_per_file_dict,
                                                                      other_user)

            print("Probability with {} : ".format(other_user), probability_dict[other_user])

        for key, value in probability_per_file_dict.items():
            probability_per_file_dict[key] = sorted(value.items(), key=lambda x: x[1], reverse=True)[:5]
        self.update_prediction_list(project_name, user_name, probability_per_file_dict, related_file_set_dict)

        send_prediction_message(project_name=project_name,
                                user_name=user_name,
                                probability_dict=probability_dict)

    def get_user_working_file(self, project_name, user_name):
        user_working_file = set()
        # file_name include (project_name - '.git') + '/'
        # so -3 because -4 + 1
        project_name_len = len(project_name) - 3

        try:
            sql = "select file_name " \
                  "from working_table " \
                  "where project_name = '%s' " \
                  "and user_name = '%s'" % (project_name, user_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_tuple = self.cursor.fetchall()
            for raw in raw_tuple:
                user_working_file.add(raw[0][project_name_len:])

        except:
            self.conn.rollback()
            print("ERROR : get_user_working_file")

        return user_working_file

    def get_other_user_working_file(self, project_name, user_name):
        other_user_working_file = dict()
        # file_name include (project_name - '.git') + '/'
        # so -3 because -4 + 1
        project_name_len = len(project_name) - 3

        try:
            sql = "select git_id " \
                  "from user_table " \
                  "where repository_name = '%s' " \
                  "and git_id != '%s'" % (project_name, user_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_tuple = self.cursor.fetchall()
            for raw in raw_tuple:
                other_user_working_file[raw[0]] = set()

        except:
            self.conn.rollback()
            print("ERROR : get_user_working_file")

        try:
            sql = "select user_name, file_name " \
                  "from working_table " \
                  "where project_name = '%s' " \
                  "and user_name != '%s'" % (project_name, user_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

            raw_tuple = self.cursor.fetchall()
            for raw in raw_tuple:
                other_user_working_file[raw[0]].add(raw[1][project_name_len:])

        except:
            self.conn.rollback()
            print("ERROR : get_user_working_file")

        return other_user_working_file

    def get_user_related_row(self, git_log_name_only_list, user_working_file_set):
        user_related_row_list = []
        for temp in git_log_name_only_list:
            if temp & user_working_file_set:
                user_related_row_list.append(temp)

        return user_related_row_list

    def get_related_file_set_dict(self, git_log_name_only_list, user_working_file_set):
        related_file_set_dict = dict()
        for temp_set in git_log_name_only_list:
            if temp_set & user_working_file_set:
                temp_list = list(temp_set)
                common_set = temp_set & user_working_file_set
                for temp in temp_list:
                    if temp not in related_file_set_dict:
                        related_file_set_dict[temp] = set()
                    related_file_set_dict[temp] |= common_set

        return related_file_set_dict

    def make_combination(self, row_list, working_file_set=set()):
        working_combination_list = []
        for i in range(len(working_file_set)):
            working_combination_list += list(itertools.combinations(working_file_set, i + 1))

        combination_list = []
        for row_temp in row_list:
            for i in range(len(row_temp)):
                combination_list += list(itertools.combinations(row_temp, i + 1))
            if working_file_set - row_temp:
                combination_temp_list = working_combination_list[:]
                set_temp = working_file_set & row_temp
                for j in range(len(set_temp)):
                    combination_temp_list = list(set(combination_temp_list) - set(list(itertools.combinations(set_temp, j + 1))))
                combination_list += combination_temp_list

        return combination_list

    def calculate_probability(self, num_user_related_row, num_other_user_related_row, user_combination_row, other_user_combination_row, common_combination_row, probability_per_file_dict, other_user):
        probability = 0

        # Using only for check
        probability_dict = dict()

        for common_combination_temp in common_combination_row:
            num_user_combination = user_combination_row.count(common_combination_temp)
            num_other_user_combination = other_user_combination_row.count(common_combination_temp)
            probability_dict[common_combination_temp] = (num_other_user_combination / num_other_user_related_row) * (num_user_combination / num_user_related_row)
            if len(common_combination_temp) & 1:
                probability += (num_other_user_combination / num_other_user_related_row) * (num_user_combination / num_user_related_row)
                if len(common_combination_temp) == 1:
                    temp_percentage = round(((num_other_user_combination / num_other_user_related_row) * (num_user_combination / num_user_related_row)) * 100)
                    if temp_percentage:
                        probability_per_file_dict['all'][other_user + ":" + common_combination_temp[0]] = temp_percentage
                        probability_per_file_dict[other_user][other_user + ":" + common_combination_temp[0]] = temp_percentage
            else:
                probability -= (num_other_user_combination / num_other_user_related_row) * (num_user_combination / num_user_related_row)

        print(probability)
        return str(round(probability * 100)) + '%'

    def update_prediction_list(self, project_name, user_name, probability_per_file_dict, related_file_set_dict):
        try:
            sql = "delete from prediction_list " \
                  "where project_name = '%s' " \
                  "and user_name = '%s'" % (project_name, user_name)

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            self.conn.rollback()
            print("ERROR : delete_prediction_list")

        try:
            sql = "replace into prediction_list " \
                  "(project_name, user_name, target, other_name, order_num, file_name, percentage, related_file_list) " \
                  "values "

            for other_user, file_list in probability_per_file_dict.items():
                for i, temp in enumerate(file_list):
                    related_file_list = "\n".join(list(related_file_set_dict[temp[0][temp[0].rfind(':') + 1:]]))
                    if other_user == 'all':
                        sql += "('%s', '%s', '%s', '%s', %d, '%s', %d, '%s'), " \
                               % (project_name, user_name, 'all', temp[0][:temp[0].rfind(':')], i + 1, temp[0][temp[0].rfind(':') + 1:], temp[1], related_file_list)
                    else:
                        sql += "('%s', '%s', '%s', '%s', %d, '%s', %d, '%s'), " \
                               % (project_name, user_name, other_user, other_user, i + 1, temp[0][temp[0].rfind(':') + 1:], temp[1], related_file_list)
            sql = sql[:-2]

            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

        except:
            self.conn.rollback()
            print("ERROR : update_prediction_list")


    # Close Database connection and cursor
    def close_db(self):
        self.cursor.close()
        self.conn.close()