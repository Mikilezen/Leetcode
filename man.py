#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
tel = {
    2116090154:"JTTC6L6I1f",
    1101335682:"motiAbe",
    1614807639:"net_amare"
}
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


import requests
import json
import requests
import json

import pandas as pd

df = pd.read_excel("m.xlsx")


mik = df.iloc[1][5:100]
ppp = mik.dropna().to_list()
simmmmmmm=[i for i in ppp if i != 'Two Pointer']
sim = []
for i in ppp:
    if i not in ['nan']:
        sim.append(i)
# print(sim)

import pandas as pd
import json

def format_worked_questions(file_path):
    """
    Reads the Excel (.xlsx) file, processes the student and submission data,
    and returns a dictionary in the format {'name': ['question_list,']}.

    :param file_path: The full path to the Excel file.
    :return: A dictionary of student names and their worked question list strings.
    """
    # Read the file using read_excel, specifying header=None and the engine
    try:
        # Assuming the data is on the first sheet (sheet_name=0)
        df = pd.read_excel(file_path, header=None, engine='openpyxl')
    except FileNotFoundError:
        return {"Error": ["Excel file not found at specified path. Please check the file name/path."]}
    except ImportError:
        return {"Error": ["The 'openpyxl' engine is required to read .xlsx files. Please run: pip install openpyxl"]}
    except Exception as e:
        return {"Error": [f"Failed to read Excel file: {e}"]}


    # The processing logic remains the same, as the data structure is consistent:
    
    # Row 2 (index 2) contains the question names.
    question_row = df.iloc[2]

    # 1. Find the question names and their column indices (columns 5, 7, 9, etc.)
    question_data = {}
    for col_idx in range(5, len(question_row)):
        if col_idx % 2 != 0:
            question_name = question_row.iloc[col_idx]
            if pd.notna(question_name):
                question_data[col_idx] = str(question_name).strip()

    # 2. Extract Student Names from Column 0, starting from Row 4 (index 4)
    student_names = df.iloc[4:, 0].dropna().unique().tolist()
    result_dict = {}

    # 3. Build the result dictionary
    for student_name in student_names:
        student_row_index = df[df.iloc[:, 0] == student_name].index

        if not student_row_index.empty:
            row_index = student_row_index[0]
            student_submissions = []
            submission_row = df.iloc[row_index]

            # Check submission status for each question
            for col_idx, question_name in question_data.items():
                cell_value = submission_row.iloc[col_idx]
                if pd.notna(cell_value):
                    student_submissions.append(question_name)

            # Format the output as requested: {'name': ['q1,q2,q3,']}
            worked_questions_str = ",".join(student_submissions) + ","
            result_dict[str(student_name)] = [worked_questions_str]

    return result_dict

def fetch_leetcode_profile(username):
    url = "https://leetcode.com/graphql"
    
    # GraphQL query to get the user's solved problem counts
    query = """
    query userSolvedProblems($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
      }
    }
    """
    
    variables = {"username": username}
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    payload = {
        "operationName": "userSolvedProblems",
        "variables": variables,
        "query": query
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=40)
        response.raise_for_status() # Raise an exception for bad status codes
        
        data = response.json()
        
        # Check if the user was found
        if data.get('data', {}).get('matchedUser') is None:
            return f"Error: User '{username}' not found."

        # Extracting solved counts
        ac_submissions = data['data']['matchedUser']['submitStats']['acSubmissionNum']
        
        solved_counts = {item['difficulty']: item['count'] for item in ac_submissions}
        
        return solved_counts

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    

import requests
import json

def fetch_leetcode_do(username):
    url = "https://leetcode.com/graphql"

    # GraphQL query for recent accepted submissions
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """

    variables = {"username": username, "limit": 25}

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    payload = {
        "operationName": "recentAcSubmissions",
        "variables": variables,
        "query": query
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=40)
        response.raise_for_status()

        data = response.json()

        # Extract submission list
        submissions = data.get("data", {}).get("recentAcSubmissionList", [])

        if not submissions:
            return f"⚠️ No submissions found for user '{username}'."
        l = []
        for i in submissions:
            l.append(i['title'])
        return l
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {e}"
def fetch_leetcode_all(usernames=tel.values()):
    sss = {} 

    url = "https://leetcode.com/graphql"

    # GraphQL query for recent accepted submissions
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """
    for i in usernames:
        variables = {"username": i, "limit": 25*4}

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        payload = {
            "operationName": "recentAcSubmissions",
            "variables": variables,
            "query": query
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=40)
            response.raise_for_status()

            data = response.json()

            # Extract submission list
            submissions = data.get("data", {}).get("recentAcSubmissionList", [])

            if not submissions:
                return f"⚠️ No submissions found for user '{i}'."
            l = []
            for j in submissions:
                l.append(j['title'])
        except requests.exceptions.RequestException as e:
            return f"❌ Error: {e}"
        m = 0
        un = []
        no = []
        for ii in simmmmmmm:
            if ii in l:
                un.append(ii)
                m+=1
            
        
        # p = tel.get(i)
        # print(p)
        # print(i)
        sss[i] = un
    return sss

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("My status", callback_data="1"),
            InlineKeyboardButton("analytics", callback_data="2"),
        ],
        [InlineKeyboardButton("get data", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    user =query.from_user
    if query.data == '1':
        username = tel[user.id]
        user_stats = fetch_leetcode_profile(username)
        await query.edit_message_text(
            text=f"CP list :  {query.data} \n Worked: {user_stats['All']} \n {user.first_name, user.last_name} \n {user.id}"
            )
    elif query.data == '2':
        username = tel[user.id]
        STA = fetch_leetcode_do(username)
        m = 0
        un = []
        no = []
        for i in simmmmmmm:
            if i in STA:
                un.append(i)
            else:
                no.append(i)
            if i in STA:m+=1
        
        
        t = ""
        s = ""
        for i in un:
            s+=i+"\n"
        for i in no:
            t+=i+"\n"
        await query.edit_message_text(
            text=f"Worked {m}\n List {s}\n ------------------- \nneed to work on {t}"
            )
    elif query.data == '3':
        file = df
        x = fetch_leetcode_all()
        await query.edit_message_text(
            text=f"{x}Selected option:"
            )
        # new_file_path_send_ = 0
        # await context.bot.send_document(
        # chat_id=update.effective_chat.id,
        # document=new_file_path_send_,
        # caption="Downloading from URL"
        # )




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("8250124120:AAHZkxj2iDBzBU-YYpL9paatJpjcASGf_10").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()