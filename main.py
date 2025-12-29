#import nest_asyncio
#nest_asyncio.apply()
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
API_BMS = "https://bookmyshow.the-zake.workers.dev/?url="


# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hello!\n\n"
        "🎬 Fetch Netflix / Prime posters\n\n"
        "/netflix\n"
        "/prime\n\n"
        "/bookmyshow\n\n"
        "Adding more soon......."
        "/appletv\n"
    )


# ---------- /netflix ----------
async def netflix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "netflix"
    await update.message.reply_text("Netflix Mode activated: ✅ \n\n<b>Send Netflix link</b>",parse_mode="HTML")


# ---------- /prime ----------
async def prime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "prime"
    await update.message.reply_text("Prime video Mode activated: ✅ \n\n<b>Send Prime Video link</b>",parse_mode="HTML")

# ---------- /book my show ----------
async def bookmyshow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "bookmyshow"
    await update.message.reply_text("Book my show Mode activated: ✅ \n\n<b>Send Book my show link</b>",parse_mode="HTML")

# ---------- Handle links ----------
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    mode = context.user_data.get("mode")

    # ===== NETFLIX =====
    if mode == "netflix":
        if "netflix.com/" not in link:
            await update.message.reply_text("❌ Invalid Netflix link")
            return

        data = requests.get(API_NETFLIX + link).json()
        poster = data.get("poster")

        if not poster:
            await update.message.reply_text("❌ Poster not found")
            return

        context.user_data["poster"] = poster
        context.user_data["link"] = poster

        keyboard = [
            [
                InlineKeyboardButton("🖼 Poster", callback_data="nf_poster"),
                InlineKeyboardButton("🖼+🔗 Poster + Link", callback_data="nf_both"),
                InlineKeyboardButton("🔗 Link", callback_data="nf_link"),
            ]
        ]

        await update.message.reply_text(
            "Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== PRIME VIDEO =====
    elif mode == "prime":
        if "primevideo.com/detail/" not in link:
            await update.message.reply_text("❌ Invalid Prime link")
            return

        data = requests.get(API_PRIME + link).json()
        landscape = data.get("landscape")
        portrait = data.get("portrait")

        if not portrait and not landscape:
            await update.message.reply_text("❌ No posters found")
            return
        elif not landscape:
            await update.message.reply_text("❌ Landscape poster not found")
            return
        elif not portrait:
            await update.message.reply_text("❌ Portrait poster not found")
            return

        context.user_data["landscape"] = landscape
        context.user_data["portrait"] = portrait
        context.user_data["link_land"] = landscape
        context.user_data["link_port"] = portrait

        keyboard = [
                [
                    InlineKeyboardButton("🖼 Landscape", callback_data="landscape_img"),
                    InlineKeyboardButton("🔗 Landscape Link", callback_data="landscape_link"),
                ],
                [
                    InlineKeyboardButton("🖼 Portrait", callback_data="portrait_img"),
                    InlineKeyboardButton("🔗 Portrait Link", callback_data="portrait_link"),
                ],
                [
                    InlineKeyboardButton("🖼 Both Photo", callback_data="both_photo"),
                    InlineKeyboardButton("🔗 Both link", callback_data="both_link"),
                ],
                [
                    InlineKeyboardButton("🖼 Both Photo & Link🔗", callback_data="both_link+photo"),
                ]
            ]


        await update.message.reply_text(
            "Choose poster:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== BOOK MY SHOW =====
    if mode == "bookmyshow":
        if "in.bookmyshow.com/" not in link:
            await update.message.reply_text("❌ Invalid Book my show link")
            return

        data = requests.get(API_BMS + link).json()
        poster_url = data.get("poster_url")

        if not poster_url:
            await update.message.reply_text("❌ Poster not found")
            return

        context.user_data["poster_url"] = poster_url
        context.user_data["link1"] = poster_url

        keyboard = [
            [
                InlineKeyboardButton("🖼 Poster", callback_data="bms_poster"),
                InlineKeyboardButton("🖼+🔗 Poster + Link", callback_data="bms_both"),
                InlineKeyboardButton("🔗 Link", callback_data="bms_link"),
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

    # ===== NETFLIX BUTTONS =====
    if query.data == "nf_poster":
        await query.message.reply_photo(poster)

    elif query.data == "nf_link":
        await query.message.reply_text(link,disable_web_page_preview=True)
        

    elif query.data == "nf_both":
        ddl = context.user_data.get("link1")
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
        await query.message.reply_photo(photo=landscape,caption="Here is the DDL link of Landscape: [Click me](" + ddl0 + ")",parse_mode="Markdown")
        await query.message.reply_photo(photo=portrait,caption="Here is the DDL link of Potrait: [Click me](" + ddl1 + ")",parse_mode="Markdown")
        
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



# ---------- Main ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("netflix", netflix))
app.add_handler(CommandHandler("prime", prime))
app.add_handler(CommandHandler("bookmyshow", bookmyshow))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button_handler))

async def set_commands(app):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("netflix", "Get Netflix poster"),
        BotCommand("prime", "Get Prime Video poster"),
        BotCommand("bookmyshow", "Get book my show poster"),
    ]
    await app.bot.set_my_commands(commands)

print("Bot running...")
app.post_init = set_commands
app.run_polling()
