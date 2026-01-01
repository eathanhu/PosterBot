#import nest_asyncio
#nest_asyncio.apply() FOR GOOGLE COLLAB
#LINE 92 MAY BE BROKEN
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "1991174184:AAE4O-Hh8xBrX7uzczW2GgVCfmInPKd4nrs"
API_NETFLIX = "https://netflix.the-zake.workers.dev/?url="
API_PRIME = "https://primevideo.the-zake.workers.dev?url="
API_BMS = "https://bookmyshow.the-zake.workers.dev/?url=" #book my show
API_SPOTIFY = "https://spotifydl.the-zake.workers.dev/?url="
API_APPLETV = "https://appletv.the-zake.workers.dev/?url=" 
API_YOUTUBE = "https://youtubedl.the-zake.workers.dev/?url="


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        name = user.first_name if user.first_name else "there"
        name2= user.last_name if user.last_name else ""
        await update.message.reply_text(
        f"<b> Hello! </b> {name} {name2}\n\n"
        "I am a poster fetching bot, and I can easily fetch high-quality posters from platforms like Netflix, Prime Video, Apple TV, BookMyShow, and Spotify.\n"
        "<b>How to use:</b>\n"
        "<blockquote>"
        " 1. Select a mode (for example: <code>/netflix</code>)\n "
        "2. The selected mode will be activated, and the bot will tell you what to do next. \n "
        "To switch modes, simply send another command like <code>/prime</code></blockquote>\n\n"
        "<b>Available Modes:</b>\n"
        "/netflix\n"
        "/prime\n"
        "/bookmyshow\n"
        "/spotify\n"
        "/appletv\n"
        "/youtube\n\n"
        "<blockquote>"
        "This is a bot made by @Franited and @b_e_n_iben."
        "</blockquote>"
        'Join to suggest an idea! <a href="https://t.me/blender_discussion">Click me</a>',parse_mode="HTML",disable_web_page_preview=True)


# ---------- /netflix ----------
async def netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "netflix"
    await update.message.reply_text("Netflix mode activated. \n\n<b>Send the Netflix page link.</b>",parse_mode="HTML")


# ---------- /prime ----------
async def prime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "prime"
    await update.message.reply_text("Prime Video mode activated. \n\n<b>Send Prime Video page link.</b>",parse_mode="HTML")

# ---------- /book my show ----------
async def bookmyshow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "bookmyshow"
    await update.message.reply_text("BookMyShow mode activated. \n\n<b>Send the BookMyShow link.</b>",parse_mode="HTML")

# ---------- /spotify ----------
async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "spotify"
    await update.message.reply_text("Spotify mode activated. \n\n<b>Send the Spotify page link.</b>",parse_mode="HTML")

# ---------- /apple tv ----------
async def appletv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "appletv"
    await update.message.reply_text("Apple TV mode activated.\n\n<b>Send Apple TV page link.</b>",parse_mode="HTML")

# ---------- /youtube ----------
async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "youtube"
    await update.message.reply_text("YouTube mode activated.\n\n<b>Send the YouTube link.</b>",parse_mode="HTML")

# version(NOT SURE IF THIS IS CORRECT SYNTAX, MIGHT NEED TO ASK CHATGPT TO FIX)

async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("<b>Bot is running version 1.0.5!</b>\n",parse_mode="HTML")
    await update.message.reply_text(" Major Changes:\n- YouTube mode added\n- Spotify audio downloading added\n- English enhanced\n- Added version command",parse_mode="HTML")
   
   # ---------- Handle links ----------
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    mode = context.user_data.get("mode")

    # ------Handle links when user dont select mode and paste link ---------
    if mode==None:
        await update.message.reply_text("<b>No mode activated</b> \n\nPlease select a mode and then share your link",parse_mode="HTML")
        return

    # ===== NETFLIX =====
    if mode == "netflix":
        if "netflix.com/" not in link:
            process=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process.delete()
            await update.message.reply_text("Invalid Netflix link. Please make sure you sent the correct link, and that you linked to a movie/show page.")
            return

        data = requests.get(API_NETFLIX + link).json()
        poster = data.get("poster")

        if not poster:
            await update.message.reply_text("Poster not found.")
            return

        context.user_data["poster"] = poster
        context.user_data["link"] = poster

        keyboard = [
            [
                InlineKeyboardButton("Poster", callback_data="nf_poster"),
                InlineKeyboardButton("Poster+Link", callback_data="nf_both"),
                InlineKeyboardButton("Link", callback_data="nf_link"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== PRIME VIDEO =====
    elif mode == "prime":
        if "primevideo.com/detail/" not in link:
            process=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process.delete()
            await update.message.reply_text("Invalid Prime Video link. Please make sure you sent a Prime Video link.")
            return

        data = requests.get(API_PRIME + link).json()
        landscape = data.get("landscape")
        portrait = data.get("portrait")

        if not portrait and not landscape:
            await update.message.reply_text("Unfortunatly, no posters were found.")
            return
        elif not landscape:
            await update.message.reply_text("Landscape poster was not found.")
            return
        elif not portrait:
            await update.message.reply_text("Portrait poster was not found.")
            return

        context.user_data["landscape"] = landscape
        context.user_data["portrait"] = portrait
        context.user_data["link_land"] = landscape
        context.user_data["link_port"] = portrait

        keyboard = [
                [
                    InlineKeyboardButton("Landscape", callback_data="landscape_img"),
                    InlineKeyboardButton("Landscape Link", callback_data="landscape_link"),
                ],
                [
                    InlineKeyboardButton("Portrait", callback_data="portrait_img"),
                    InlineKeyboardButton("Portrait Link", callback_data="portrait_link"),
                ],
                [
                    InlineKeyboardButton("Both Photos", callback_data="both_photo"),
                    InlineKeyboardButton("Both Links", callback_data="both_link"),
                ],
                [
                    InlineKeyboardButton("Photo+Link", callback_data="both_link+photo"),
                ]
            ]


        await update.message.reply_text(
            "Choose your poster:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== BOOK MY SHOW =====
    if mode == "bookmyshow":
        if "in.bookmyshow.com/" not in link:
            process=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process.delete()
            await update.message.reply_text("Invalid BookMyShow link. Please make sure you sent the correct link.")
            return

        data = requests.get(API_BMS + link).json()
        poster_url = data.get("poster_url")

        if not poster_url:
            await update.message.reply_text("Poster was not found.")
            return

        context.user_data["poster_url"] = poster_url
        context.user_data["link1"] = poster_url

        keyboard = [
            [
                InlineKeyboardButton("Poster", callback_data="bms_poster"),
                InlineKeyboardButton("Poster+Link", callback_data="bms_both"),
                InlineKeyboardButton("Link", callback_data="bms_link"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== SPOTIFY =====
    if mode == "spotify":
        if "open.spotify.com/artist" in link:
            process1=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process1.delete()
            await update.message.reply_text("This is an artist Spotify link. \n Please send a track link.")
            return
        if "open.spotify.com/track" not in link:
            process2=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process2.delete()
            await update.message.reply_text("Invalid Spotify link. Did you send a track link? ")
            return

        data = requests.get(API_SPOTIFY + link).json()
        medias = data.get("data", {}).get("medias", [])

        if not medias:
            await update.message.reply_text("Poster was not found.")
            return
        media = medias[0]
        url = media.get("url")
        if not url:
            await update.message.reply_text("Song URL was not found.")
            return
        context.user_data["url"] = media.get("url")
        context.user_data["quality"] = media.get("quality")
        context.user_data["extension"] = media.get("extension")
        context.user_data["type"] = media.get("type")
        context.user_data["source"] = data.get("data", {}).get("source")
        context.user_data["duration"] = data.get("data", {}).get("duration")
        context.user_data["title"] = data.get("data", {}).get("title")
        context.user_data["author"] = data.get("data", {}).get("author")
        context.user_data["thumbnail"] = data.get("data", {}).get("thumbnail")

        keyboard = [
            [
                InlineKeyboardButton("Poster", callback_data="spotify_poster"),
                InlineKeyboardButton("Poster+Link", callback_data="spotify_both"),
                InlineKeyboardButton("Link", callback_data="spotify_link"),
                InlineKeyboardButton("Song", callback_data="spotify_song"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
     # ===== APPLE TV =====
    if mode == "appletv":
        if "tv.apple.com/" not in link:
            process=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process.delete()
            await update.message.reply_text("Invalid Apple TV link. Did you link to the wrong website?")
            return

        data = requests.get(API_APPLETV + link).json()
        poster2 = data.get("poster")
        name = data.get("display_title")

        if not poster2:
            await update.message.reply_text("Poster was not found.")
            return

        context.user_data["poster2"] = poster2
        context.user_data["display_title"] = name

        keyboard = [
            [
                InlineKeyboardButton("Poster", callback_data="atv_poster"),
                InlineKeyboardButton("Poster+Link", callback_data="atv_both"),
                InlineKeyboardButton("Link", callback_data="atv_link"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
     # ===== YOUTUBE =====
    if mode == "youtube":
        if "youtu.be/" not in link and "youtube.com/" not in link:
            process=await update.message.reply_text("Processing link...")
            await asyncio.sleep(2)
            await process.delete()
            await update.message.reply_text("Invalid YouTube link.")
            return

        data = requests.get(API_YOUTUBE + link).json()
        thumbnail2 = data.get("thumbnail")

        if not thumbnail2:
            await update.message.reply_text("Poster was not found.")
            return

        context.user_data["thumbnail2"] = thumbnail2

        keyboard = [
            [
                InlineKeyboardButton("Poster", callback_data="yt_poster"),
                InlineKeyboardButton("Poster+Link", callback_data="yt_both"),
                InlineKeyboardButton("Link", callback_data="yt_link"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ---------- Button handler ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Netflix
    poster = context.user_data.get("poster")
    link = context.user_data.get("link")

    # Prime
    landscape = context.user_data.get("landscape")
    portrait = context.user_data.get("portrait")

    # Book my show
    poster_url = context.user_data.get("poster_url")
    link1 = context.user_data.get("link1")

    # spotify
    url = context.user_data.get("url")
    quality = context.user_data.get("quality")
    source = context.user_data.get("source")
    extension = context.user_data.get("extension")
    type = context.user_data.get("type")
    duration = context.user_data.get("duration")
    title = context.user_data.get("title")
    author = context.user_data.get("author")
    thumbnail = context.user_data.get("thumbnail")

    # appletv
    name2 = context.user_data.get("display_title")
    poster2 = context.user_data.get("poster2")

    #youtube
    thumbnail2 = context.user_data.get("thumbnail2")

    # ===== NETFLIX BUTTONS =====
    if query.data == "nf_poster":
        await query.message.reply_photo(poster)

    elif query.data == "nf_link":
        await query.message.reply_text(link,disable_web_page_preview=True)


    elif query.data == "nf_both":
        ddl = context.user_data.get("link")
        await query.message.reply_photo(photo=poster,caption="Here is the DDL link: [Click me](" + ddl + ")",parse_mode="Markdown")

    # ===== PRIME BUTTONS =====
    elif query.data == "landscape_img":
        await query.message.reply_photo(landscape)

    elif query.data == "portrait_img":
        await query.message.reply_photo(portrait)

    elif query.data == "both_photo":
        await query.message.reply_photo(landscape)
        await query.message.reply_photo(portrait)

    elif query.data == "both_link":
        await query.message.reply_text(landscape,disable_web_page_preview=True)
        await query.message.reply_text(portrait,disable_web_page_preview=True)

    elif query.data == "both_link+photo":
        ddl0 = context.user_data.get("link_land")
        ddl1 = context.user_data.get("link_port")
        await query.message.reply_photo(photo=landscape,caption="Here is the DDL link of your landscape poster: [Click me](" + ddl0 + ")",parse_mode="Markdown")
        await query.message.reply_photo(photo=portrait,caption="Here is the DDL link of your potrait poster: [Click me](" + ddl1 + ")",parse_mode="Markdown")

    elif query.data == "landscape_link":
        await query.message.reply_text(landscape,disable_web_page_preview=True)

    elif query.data == "portrait_link":
        await query.message.reply_text(portrait,disable_web_page_preview=True)

    # ===== BOOK MY SHOW BUTTONS =====
    if query.data == "bms_poster":
        await query.message.reply_photo(poster_url)

    elif query.data == "bms_link":
        await query.message.reply_text(link1,disable_web_page_preview=True)


    elif query.data == "bms_both":
        ddl2 = context.user_data.get("link1")
        await query.message.reply_photo(photo=poster_url,caption="Here is the DDL link: [Click me](" + ddl2 + ")",parse_mode="Markdown")

     # ===== SPOTIFY BUTTONS =====
    if query.data == "spotify_poster":
        await query.message.reply_photo(thumbnail)

    elif query.data == "spotify_link":
        await query.message.reply_text(thumbnail,disable_web_page_preview=True)

    elif query.data == "spotify_both":
        ddl3 = context.user_data.get("thumbnail")
        await query.message.reply_photo(photo=thumbnail,caption="Here is the DDL link: [Click me](" + ddl3 + ")\n\n",parse_mode="Markdown")

    if query.data == "spotify_song":
        minutes, seconds = duration.split(":")
        status = await query.message.reply_text("Downloading audio...")
        await status.edit_text("Uploading audio to Telegram...")
        await query.message.reply_audio(url,caption=f"\n Extention: {extension}\nSource: {source}\nQuality: {quality}\nDuration: {minutes} minutes and {seconds} seconds\nArtist: {author}\nTitle: {title}\nType: {type}\n")
        upload=await status.edit_text("Upload complete!")
        await asyncio.sleep(10)
        await upload.delete()

    # ===== APPLE TV BUTTONS =====
    if query.data == "atv_poster":
        await query.message.reply_photo(photo=poster2,caption=f"Name: {name2}\n")

    elif query.data == "atv_link":
        await query.message.reply_text(poster2,disable_web_page_preview=True)

    elif query.data == "atv_both":
        ddl4 = context.user_data.get("poster2")
        await query.message.reply_photo(photo=poster2,caption="Here is the DDL link: [Click me](" + ddl4 + ")\n\n",parse_mode="Markdown")

    # ===== YOUTUBE BUTTONS =====
    if query.data == "yt_poster":
        await query.message.reply_photo(thumbnail2)

    elif query.data == "yt_link":
        await query.message.reply_text(thumbnail2,disable_web_page_preview=True)

    elif query.data == "yt_both":
        ddl5 = context.user_data.get("thumbnail2")
        await query.message.reply_photo(photo=thumbnail2,caption="Here is the DDL link: [Click me](" + ddl5 + ")\n\n",parse_mode="Markdown")



# ---------- Main ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("netflix", netflix))
app.add_handler(CommandHandler("prime", prime))
app.add_handler(CommandHandler("bookmyshow", bookmyshow))
app.add_handler(CommandHandler("spotify", spotify))
app.add_handler(CommandHandler("version", version))
app.add_handler(CommandHandler("appletv", appletv))
app.add_handler(CommandHandler("youtube", youtube))
app.add_handler(CommandHandler("version", version))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button_handler))

async def set_commands(app):
    commands = [
        BotCommand("start", "Starts the bot, and gives usage instructions."),
        BotCommand("version", "Tells you what version the bot is running."),
        BotCommand("netflix", "Gets a Netflix poster."),
        BotCommand("prime", "Gets a Prime Video poster."),
        BotCommand("bookmyshow", "Gets a BookMyShow poster."),
        BotCommand("spotify", "Gets a Spotify poster. You can also download audio directly from Spotify(for free) using this mode."),
        BotCommand("appletv", "Gets an Apple TV poster."),
        BotCommand("youtube", "Gets a YouTube poster. The poster comes from the video's thumbnail, so it may not be high quality."),
    ]
    await app.bot.set_my_commands(commands)
print("Bot running...")
app.post_init = set_commands
app.run_polling()
