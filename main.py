from functools import wraps
from get_result import pre_result
from get_result import post_result
from telegram.ext import *
from telegram import *
import logging
import html
import json
import traceback
import pytz
import datetime
import time
import csv
import os


semester=""
enrollment=""
stats_sem=''
stats_branch=''
enroll_regex='^([0-9]{4})([A-Z]|[a-z])(.{5})([0-9]{2}$)'

DEVELOPER_CHAT_ID = 1952690210   #Enter Your Chat Id, LOGS, ERRORS & Crash reports will be sent there.
BOT_TOKEN = "XXXXXX:xxxxxxxxxxxxxxxxxxxxxx" #Enter your Bot token Here 


try:
    API_TOKEN = os.environ["API_TOKEN"]
except:
    API_TOKEN = BOT_TOKEN


def get_date():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    dtime=str(current_time).split(" ")[0]
    return dtime

def get_time():
    curr_time = str(time.strftime("%H:%M:%S", time.localtime()))
    return curr_time

def csv_write(name , id , enroll , semester):
    curr_date = get_date()
    curr_time = get_time()
    with open("bot_data.csv" , "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([curr_date, curr_time, name, id, enroll, semester])
        #csv_writer.writerow(["Date", "Time", "UserName", "UserID", "Enrollment", "Semester"]) #for first time to write header of csv file, can use .writeheader too.


def get_stats(branch, sem, session):

    brancH_IT={

     'sem_2' :{
                  'june_2022':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2022`\n\n**Branch** - `IT`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 57\n\n**Pass** - 34 ( 31 + 3 Grace) 🥳\n\n**Fail** - 23 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601IT211021`   -  `8.29` 🥇\n2.   `0601IT211041`   -  `7.98` 🥈\n3.   `0601IT211012`   -  `7.95` 🥉\n4.   `0601IT211029`   -  `7.86`\n5.   `0601IT211018`   -  `7.60`\n\n\n #This is bot 🤖 generated data so there may be some error in it.',
                  'june_2023':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2023`\n\n**Branch** - `IT`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 61\n\n**Pass** - 32 ( 29 + 3 Grace) 🥳\n\n**Fail** - 29 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601IT221036`   -  `7.60` 🥇\n2.   `0601IT221016`   -  `7.41` 🥈\n3.   `0601IT221011`   -  `7.29` 🥉\n4.   `0601IT221051`   -  `7.24`\n5.   `0601IT221044`   -  `7.17`\n\n\n #This is bot 🤖 generated data so there may be some error in it.'
                  },
     'sem_3' :{}
    }

    brancH_EC={
     'sem_2' :{
                  'june_2022':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2022`\n\n**Branch** - `EC`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 51\n\n**Pass** - 18 ( 16 + 2 Grace) 🥳\n\n**Fail** - 33 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601EC211001`   -  `8.38` 🥇\n2.   `0601EC211039`   -  `8.10` 🥈\n3.   `0601EC211021`   -  `7.76` 🥉\n4.   `0601EC211025`   -  `7.48`\n5.   `0601EC211026`   -  `7.36`\n\n\n #This is bot 🤖 generated data so there may be some error in it.',
                  'june_2023':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2023`\n\n**Branch** - `EC`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 55\n\n**Pass** - 12 ( 10 + 2 Grace) 🥳\n\n**Fail** - 43 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601EC221013`   -  `7.48` 🥇\n2.   `0601EC221052`   -  `7.10` 🥈\n3.   `0601EC221058`   -  `7.00` 🥉\n4.   `0601EC221020`   -  `6.86`\n5.   `0601EC221025`   -  `6.84`\n\n\n #This is bot 🤖 generated data so there may be some error in it.'
                },
     'sem_3' :{}
    }

    brancH_EE={

     'sem_2' :{
                  'june_2022':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2022`\n\n**Branch** - `EE`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 41\n\n**Pass** - 20 ( 19 + 1 Grace) 🥳\n\n**Fail** - 21 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601EE211018`   -  `7.98` 🥇\n2.   `0601EE211024`   -  `7.91` 🥈\n3.   `0601EE211035`   -  `7.65` 🥉\n4.   `0601EE211028`   -  `7.24`\n5.   `0601EE211001`   -  `7.00`\n\n\n #This is bot 🤖 generated data so there may be some error in it.',
                  'june_2023' : f'coming soon'
                  },
     'sem_3' :{}
    }

    brancH_ME={

     'sem_2' :{
                  'june_2022':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2022`\n\n**Branch** - `ME`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 41\n\n**Pass** - 24 ( 22 + 2 Grace) 🥳\n\n**Fail** - 17 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601ME211012`   -  `7.83` 🥇\n2.   `0601ME211013`   -  `7.5` 🥈\n3.   `0601ME211040`   -  `7.41` 🥉\n4.   `0601ME211009`   -  `7.38`\n5.   `0601ME211011`   -  `7.38`\n\n\n #This is bot 🤖 generated data so there may be some error in it.',
                  'june_2023' : f'coming soon'
                  },
     'sem_3':{}


             }
    brancH_CE={

     'sem_2' :{
                  'june_2022':f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2022`\n\n**Branch** - `CE`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 52\n\n**Pass** - 31 ( 26 + 5 Grace) 🥳\n\n**Fail** - 21 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601CE211018`   -  `8.07` 🥇\n2.   `0601CE211040`   -  `8.07` 🥈\n3.   `0601CE211008`   -  `7.96` 🥉\n4.   `0601CE211056`   -  `7.91`\n5.   `0601CE211032`   -  `7.79`\n\n\n #This is bot 🤖 generated data so there may be some error in it.',
                  'june_2023' : f'▬▬▬▬ `Branch Statistics` ▬▬▬▬\n\n**Session** - `June - 2023`\n\n**Branch** - `CE`             Semester - `2`\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Total Results fetched** - 43\n\n**Pass** - 8 ( 4 + 4 Grace) 🥳\n\n**Fail** - 35 😕\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n**Top - 5 Ranks** 🏆 (according to **CGPA**)\n\n1.   `0601CE221008`   -  `7.26` 🥇\n2.   `0601CE221047`   -  `6.88` 🥈\n3.   `0601CE221045`   -  `6.62` 🥉\n4.   `0601CE221031`   -  `6.34`\n5.   `0601CE221029`   -  `6.31`\n\n\n #This is bot 🤖 generated data so there may be some error in it'
                  },
     'sem_3':{}


             }
    session = session.split("-")[1]
    try:

        if branch == "brancH_IT":         
            return brancH_IT[sem][session]
        if branch == "brancH_EC":         
            return brancH_EC[sem][session]
        if branch == "brancH_EE":         
            return brancH_EE[sem][session]
        if branch == "brancH_ME":         
            return brancH_ME[sem][session]
        if branch == "brancH_CE":         
            return brancH_CE[sem][session]
    except:
        return "`Coming Soon...`"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(constants.ChatAction.TYPING)

send_upload_action = send_action(constants.ChatAction.UPLOAD_DOCUMENT)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=constants.ParseMode.HTML
    )



@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", f'{user.full_name}')

    await update.message.reply_text(
        f"**Hello**! {user.full_name} 😊\n"
        "My name is `Professor` Bot. I will help you to find your B.Tech Result.\n\n"
        "**Send /result to find out your result.**\n\n"
        "**Send /statistics to find out Branch Statistics.**\n\n"
        "Send /help to display all commands\n\n\n"
        "Created by -  [@ml_024😎](http://instagram.com/ml_024)"

    ,parse_mode=constants.ParseMode.MARKDOWN)

    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=f"🔥New User🔥\n  User {user.full_name} id: `{user.id}` started the conversation.", parse_mode=constants.ParseMode.MARKDOWN)
    csv_write(user.full_name, user.id, "Start", "-")



@send_typing_action
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text("Ok, Hold on a second...")

    pre_result()
    keyboard = [
       [InlineKeyboardButton(" 1 ", callback_data="Semester_1"),
        InlineKeyboardButton(" 2 ", callback_data="Semester_2") ],
       
       [InlineKeyboardButton(" 3 ", callback_data="Semester_3"),
        InlineKeyboardButton(" 4 ", callback_data="Semester_4") ],
       
       [InlineKeyboardButton(" 5 ", callback_data="Semester_5"),
        InlineKeyboardButton(" 6 ", callback_data="Semester_6") ],
       
       [InlineKeyboardButton(" 7 ", callback_data="Semester_7"),
        InlineKeyboardButton(" 8 ", callback_data="Semester_8") ]        

         ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Select Semester:", reply_markup=reply_markup)



@send_typing_action
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    global semester,enrollment
    if len(update.message.text) == 12:
        global enrollment,enrollment_got
        if (semester == "") or (semester == None):
            await update.message.reply_text(f"Send /result to view another /result")
        else:
            await update.message.reply_text(f"You Entered: {update.message.text.upper()}")
            enrollment=update.message.text.upper()
            result=post_result(enrollment,semester)
            await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.TYPING)
        
            await update.message.reply_text(result,parse_mode=constants.ParseMode.MARKDOWN)
            try:
                if len(result) >= 50:
                    await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.UPLOAD_DOCUMENT)
                    await context.bot.send_document(chat_id=update.message.chat_id, document=open(f"pdf/{enrollment}.pdf","rb"))
                    await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.TYPING)
                    await update.message.reply_text("Send /result again to view someone else's result")
                    await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.TYPING)
                    await update.message.reply_text("`Thanks!`😊 \nPlease don't forget to give us /feedback",parse_mode=constants.ParseMode.MARKDOWN)
                    await context.bot.send_message(
                    chat_id=DEVELOPER_CHAT_ID, text=f"User {user.full_name} id: `{user.id}`. \n Semester: {semester} Enroll: {enrollment}", parse_mode=constants.ParseMode.MARKDOWN)
                    csv_write(user.full_name, user.id, enrollment, semester)
            
                #elif (len(result) == 0) or (result == None):
                #    await update.message.reply_text("Some error occurred, Please try again /result")
                else:
                    await update.message.reply_text('🥲')
                    await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.TYPING)
                    await update.message.reply_text('If you think it was a mistake please let us know by giving /feedback')
            
                semester=""
                
            except:
                await update.message.reply_text("Some error occurred, Please try again /result")
                semester=""

@send_typing_action
async def select_semester(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    global semester
    semester=query.data.split("_")[1]
    await query.edit_message_text(text=f"Selected Option: {semester}")
    
    await query.message.reply_text(f"{user.first_name} Enter your Enrollment Number: ")
    



@send_typing_action
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(
        "I can help you to find out your B.Tech result.You can control me by sending these commands:\n\n"
        "/result -> get your Result\n"
        "/statistics -> branch stats(Only for **IGEC**)\n"
        "/feedback -> To give feedback to us\n"
        "/help -> To view all commands\n\n"
        "`More features coming soon, Stay tuned with us...❤`"
    ,parse_mode=constants.ParseMode.MARKDOWN)


@send_typing_action
async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(
        "`If you want to share your thoughts or report any bug please feel free to contact us 🙏 at -`\n\n"
        "**Telegram** - [@ml_024](t.me/ml_024)\n\n"
        "**Instagram** - [Click here](http://instagram.com/ml_024)\n"

    ,parse_mode=constants.ParseMode.MARKDOWN , disable_web_page_preview=True)
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=f"User {user.full_name} id: `{user.id}`. is AT /feedback", parse_mode=constants.ParseMode.MARKDOWN)


@send_typing_action
async def statistics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text("Ok, Stats are only available for IGEC Sagar...")

    keyboard = [
        [ InlineKeyboardButton("IT", callback_data="brancH_IT") ],
        [ InlineKeyboardButton("EC", callback_data="brancH_EC") ],
        [ InlineKeyboardButton("EE", callback_data="brancH_EE") ],
        [ InlineKeyboardButton("ME", callback_data="brancH_ME") ],
        [ InlineKeyboardButton("CE", callback_data="brancH_CE") ]
             ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Select Branch:", reply_markup=reply_markup)
    
    

@send_typing_action
async def statistics_2nd_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    global stats_branch
    await query.edit_message_text(text=f"Selected Option: {query.data.split('_')[1]}")
    stats_branch=query.data
    keyboard = [
       #[InlineKeyboardButton(" 1 ", callback_data="sem_1"),
        [InlineKeyboardButton(" 2 ", callback_data="sem_2") ],
       
       [InlineKeyboardButton(" 3 ", callback_data="sem_3"),
        InlineKeyboardButton(" 4 ", callback_data="sem_4") ],
       
       [InlineKeyboardButton(" 5 ", callback_data="sem_5"),
        InlineKeyboardButton(" 6 ", callback_data="sem_6") ],
       
       [InlineKeyboardButton(" 7 ", callback_data="sem_7")]
        #InlineKeyboardButton(" 8 ", callback_data="sem_8") ]        

              ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select Semester:", reply_markup=reply_markup)


@send_typing_action
async def statistics_3rd_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    global stats_sem
    await query.edit_message_text(text=f"Selected Option: {query.data.split('_')[1]}")
    stats_sem=query.data

    if stats_sem=="sem_2" or stats_sem=="sem_4" or stats_sem=="sem_6":
        keyboard = [
            [InlineKeyboardButton("June-2022", callback_data="ses-june_2022")],
            [InlineKeyboardButton("June-2023", callback_data="ses-june_2023")]
                   ]


    if stats_sem=="sem_3" or stats_sem=="sem_5" or stats_sem=="sem_7":
        keyboard = [
           [InlineKeyboardButton(" Dec-2022", callback_data="ses-dec_2022")],
            [InlineKeyboardButton("Dec-2023", callback_data="ses-dec_2023")]
                   ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select Session: ", reply_markup=reply_markup)





    
@send_typing_action
async def statistics_final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.callback_query.from_user
    query = update.callback_query
    await query.answer()
    global stats_sem , stats_branch, stats_session
    await query.edit_message_text(text=f"Selected Option: {query.data.split('-')[1]}")
    stats_session=query.data
    
    reply_text=get_stats(stats_branch , stats_sem, stats_session)
    await query.message.reply_text(text =reply_text   , parse_mode=constants.ParseMode.MARKDOWN )
    
    await query.message.reply_text(text=f'`"You always PASS failure on your way to SUCCESS."`\n                                          - Mickey Rooney',parse_mode=constants.ParseMode.MARKDOWN)
    await query.message.reply_text("`Thanks!`😊 \nPlease don't forget to give us /feedback",parse_mode=constants.ParseMode.MARKDOWN)
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=f"User {user.full_name} id: `{user.id}`. is AT /statistics {stats_branch}  {stats_sem}", parse_mode=constants.ParseMode.MARKDOWN)




@send_typing_action
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.message.chat_id ,action=constants.ChatAction.TYPING)
    await update.message.reply_text(
        ''.join([l.upper() if i % 2 == 0 else l for (i, l) in enumerate(update.message.text)])
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_TOKEN).build()    

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("result", result))
    application.add_handler(MessageHandler(filters.Regex(enroll_regex), message))
    application.add_handler(CallbackQueryHandler(select_semester , pattern='^(Semester_)([1-8])'))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(CommandHandler("statistics", statistics_command))
    application.add_handler(CallbackQueryHandler(statistics_2nd_keyboard , pattern='^(brancH_)'))
    application.add_handler(CallbackQueryHandler(statistics_3rd_keyboard, pattern='^(sem_)([1-8])$'))
    application.add_handler(CallbackQueryHandler(statistics_final, pattern='^(ses-)'))
    
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(enroll_regex), echo))

    
    # ...and the error handler
    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
