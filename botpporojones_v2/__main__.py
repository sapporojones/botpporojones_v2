# imports
import datetime as dt
import os
import random

import discord
import praw
import pytz
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# pull ins from the env file
token = os.getenv("DISCORD_TOKEN")
weather_key = os.getenv("API_KEY")
stockmarket_key = os.getenv("STOCKMARKET_KEY")

# reddit pull ins from the env file
reddit_clientID = os.getenv("CLIENT_ID")
reddit_clientSecret = os.getenv("CLIENT_SECRET")
reddit_password = os.getenv("PASSWORD")
reddit_username = os.getenv("USERNAME")

# bot command modifier
bot = commands.Bot(command_prefix="!")


# begin bot commands
@bot.command(
    name="d100", help="Roll the d100 to determine the fate of the alliance."
)
async def d100(ctx):
    roll = str(random.randint(1, 100))
    response = "You rolled a " + roll
    await ctx.send(response)


@bot.command(
    name="d",
    help="Roll the arbitrary sided die because you want to for some reason.",
)
async def d(ctx, en):
    roll = str(random.randint(1, int(en)))
    response = f"You rolled a {roll}"
    await ctx.send(response)


@bot.command(name="create-channel", help="creates a text channel.")
@commands.has_role("admin")
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f"Creating a new channel: {channel_name}")
        await guild.create_text_channel(channel_name)


@bot.command(
    name="weather",
    help="returns weather info for a given zip code (try not to doxx yourself)",
)
async def weather(ctx, zip_code):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = (
        f"{base_url}appid={weather_key}&zip={str(zip_code)}&units=imperial"
    )
    full_json = requests.get(complete_url).json()
    weather_description = full_json["weather"][0]["description"]
    weather_temp = full_json["main"]["temp"]
    response = (
        "The temperature at "
        + str(zip_code)
        + " is "
        + str(int(weather_temp))
        + " degrees fahrenheit, the weather conditions are described as "
        + weather_description
    )
    await ctx.send(response)


@bot.command(name="f", help="a fortune")
async def f(ctx):
    base_url = "http://yerkee.com/api/fortune/wisdom"
    fortune_raw = requests.get(base_url)
    fortune_json = fortune_raw.json()
    fortune_text = fortune_json["fortune"]
    await ctx.send(fortune_text)


@bot.command(name="stock", help="stock quote lookup")
async def stock(ctx, ticker):
    query = (
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="
        + ticker
        + "&apikey="
        + stockmarket_key
    )
    json_output = requests.get(query)
    data = json_output.json()
    response = (
        "Here's some information about that security you requested:\n"
        + "The current price is: "
        + data["Global Quote"]["05. price"]
        + "\n"
        + "The current change is: "
        + data["Global Quote"]["09. change"]
        + "\n"
        + "The change percent of that is: "
        + data["Global Quote"]["10. change percent"]
        + "\n"
        + "The security opened at: "
        + data["Global Quote"]["02. open"]
        + "\n"
        + "The security closed last at: "
        + data["Global Quote"]["08. previous close"]
    )
    await ctx.send(response)


@bot.command(name="ip", help="IP lookup info")
async def ip(ctx, address):
    base_url = "https://ipapi.co/"
    json_url = base_url + address + "/json"
    get_data = requests.get(json_url)
    bulk_data = get_data.json()
    response1 = "Looking up info regarding " + bulk_data["ip"] + "\n"
    response2 = "City: " + bulk_data["city"] + "\n"
    response3 = "State or Region: " + bulk_data["region"] + "\n"
    response4 = "Country: " + bulk_data["country_name"] + "\n"
    response5 = "Organization: " + bulk_data["org"] + "\n"
    full_reply = (
        "\n **HACKER MODE ENGAGED**\n"
        + response1
        + response2
        + response3
        + response4
        + response5
    )
    await ctx.send(full_reply)


@bot.command(name="r", help="returns posts from the specified subreddit")
async def r(ctx, sub_reddit):
    reddit = praw.Reddit(
        client_id=reddit_clientID,
        client_secret=reddit_clientSecret,
        password=reddit_password,
        user_agent="testscript by /u/sapporojones",
        username=reddit_username,
    )
    random_submission = reddit.subreddit(sub_reddit).random()
    if random_submission.over_18 == True:
        submission_url = "Adult content detected, not posting"
    else:
        submission_url = reddit.submission(random_submission).url
    await ctx.send(submission_url)


@bot.command(name="time", help="current time for a variety of timezones")
async def time(ctx):
    tz_london = pytz.timezone("Europe/London")
    tz_moscow = pytz.timezone("Europe/Moscow")
    tz_pac = pytz.timezone("America/Los_Angeles")
    tz_mtn = pytz.timezone("America/Denver")
    tz_cnt = pytz.timezone("America/Mexico_City")
    tz_est = pytz.timezone("America/New_York")
    tz_sydney = pytz.timezone("Australia/Sydney")

    now_obj = dt.datetime.now(pytz.utc)
    uk_obj = now_obj.astimezone(tz_london)
    rus_obj = now_obj.astimezone(tz_moscow)
    pac_obj = now_obj.astimezone(tz_pac)
    mtn_obj = now_obj.astimezone(tz_mtn)
    cnt_obj = now_obj.astimezone(tz_cnt)
    est_obj = now_obj.astimezone(tz_est)
    autz_obj = now_obj.astimezone(tz_sydney)

    l1 = f" \n **The Current Time Is:** \n"
    l2 = f"**Pacific (USTZ):** {str(pac_obj)[11:16]} \n"
    l3 = f"**Mountain (USTZ):** {str(mtn_obj)[11:16]} \n"
    l4 = f"**Central (USTZ):** {str(cnt_obj)[11:16]} \n"
    l5 = f"**Eastern (USTZ):** {str(est_obj)[11:16]} \n"
    l6 = f"**London:(GMT)** {str(uk_obj)[11:16]} \n"
    l7 = f"**Moscow (RUTZ):** {str(rus_obj)[11:16]} \n"
    l8 = f"**Sydney (AUTZ):** {str(autz_obj)[11:16]} \n"
    l9 = f"**EVE Time (UTC):** {str(now_obj)[11:16]} \n"

    response = l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9

    await ctx.send(response)


@bot.command(name="pilot", help="get various urls about a given pilot name")
async def pilot(ctx, characterName):
    char_srch = requests.get(
        f"https://esi.evetech.net/latest/search/?categories=character&datasource=tranquility"
        f"&language=en&search={characterName}&strict=true"
    )
    char_srch_json = char_srch.json()
    if len(char_srch_json) <= 0:
        raise Exception("Character not found")
    else:
        char_id = char_srch_json["character"][0]

    characterId = str(char_id)
    line1 = f"\n **PILOT SEARCH RESULTS:**" + "\n"
    line2 = (
        "**ZKB:** https://zkillboard.com/character/" + characterId + "/" + "\n"
    )
    line3 = (
        "**EVEWHO:** https://evewho.com/character/" + characterId + "/" + "\n"
    )
    line4 = (
        "**TEST Auth:** https://auth.pleaseignore.com/eve/character/"
        + characterId
        + "/"
        + "\n"
    )
    response = line1 + line2 + line3 + line4

    await ctx.send(response)


@bot.command(name="corp", help="get various urls about a given corp")
async def corp(ctx, corporationName):
    ### deprecating esipy usage for search functions due to slowness ###
    # client = SwaggerClient.from_url('https://esi.evetech.net/latest/swagger.json')
    # corpResults = client.Search.get_search(
    #     search=corporationName,
    #     categories=['corporation'],
    #     strict=True,
    # ).result()['corporation']

    corp_srch = requests.get(
        f"https://esi.evetech.net/latest/search/?categories=corporation&datasource=tranquility"
        f"&language=en&search={corporationName}&strict=true"
    )
    corp_srch_json = corp_srch.json()
    if len(corp_srch_json) <= 0:
        raise Exception("Corporation not found")
    else:
        corp_id = corp_srch_json["corporation"][0]

    # corporationId = corpResults[0]
    corporationId = str(corp_id)
    line1 = f"\n**CORP SEARCH RESULTS:**" + "\n"
    line2 = (
        "**ZKB:** https://zkillboard.com/corporation/"
        + corporationId
        + "/"
        + "\n"
    )
    line3 = (
        "**EVEWHO:** https://evewho.com/corporation/"
        + corporationId
        + "/"
        + "\n"
    )
    line4 = (
        "**DOTLAN:** http://evemaps.dotlan.net/corp/"
        + corporationId
        + "/"
        + "\n"
    )
    response = line1 + line2 + line3 + line4

    await ctx.send(response)


@bot.command(name="alice", help="get various urls about a given alliance")
async def alice(ctx, alice_name):
    alice_srch = requests.get(
        f"https://esi.evetech.net/latest/search/?categories=alliance&datasource=tranquility"
        f"&language=en&search={alice_name}&strict=true"
    )
    alice_srch_json = alice_srch.json()
    if len(alice_srch_json) <= 0:
        raise Exception("Alliance not found")
    else:
        alice_id = alice_srch_json["alliance"][0]

    line1 = f"\n **ALLIANCE SEARCH RESULTS:**" + "\n"
    line2 = f"**ZKB:** https://zkillboard.com/alliance/{alice_id}/ \n"
    line3 = f"**EVEWHO:** https://evewho.com/alliance/{alice_id}/ \n"
    line4 = f"**DOTLAN:** http://evemaps.dotlan.net/alliance/{alice_id}/ \n"
    response = line1 + line2 + line3 + line4

    await ctx.send(response)


@bot.command(
    name="shlookup",
    help="Deprecated, visit http://shlookup.sunkenrlyeh.com to use the shlookup!",
)
async def shlookup(ctx, pilot_name):
    response = "go to http://shlookup.sunkenrlyeh.com to use the shlookup!"
    await ctx.send(response)


############################################
# code goes above here
############################################
bot.run(token)
