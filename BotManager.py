import configs.defaultConfig as defaultConfig

import asyncio
import requests
import json
import discord
from discord.ext import commands

def update_score(user, points):
    url = 'http://127.0.0.1:8000/api/score/update/'
    new_score = {'name': user, 'points': points}
    x = requests.post(url, data=new_score)
    return

def get_score():
    leaderboard = []
    id = 1
    response = requests.get("http://127.0.0.1:8000/api/score/leaderboard/")
    json_data = json.loads(response.text)

    for item in json_data:
        leaderboard.append(f"{id}. {item['name']} - {item['points']} points")
        id += 1
    return leaderboard

def get_question():
    qs = ''
    id = 1
    correct_answers = []
    response = requests.get("http://127.0.0.1:8000/api/random")
    json_data = json.loads(response.text)
    points = json_data[0]['points']

    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        qs += str(id) + ". " + item['answer'] + "\n"
        if item['is_correct']:
            correct_answers.append(id)
        id += 1
    
    return (qs, correct_answers, points)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

user_quiz_states = {}

@bot.event
async def on_ready():
    print("Bot is online.")

@bot.command(aliases=["quiz"])
async def question(ctx):
    await ctx.send("How many questions would you like to answer?")
    
    def check(m):
        return m.author == ctx.author and m.content.isdigit()
    
    try:
        num_of_questions_msg = await bot.wait_for('message', check=check, timeout=30.0)
        num_of_questions = int(num_of_questions_msg.content)
        
        if num_of_questions <= 0:
            await ctx.send("Please enter a valid number of questions (greater than 0).")
            return


        user_quiz_states[ctx.author.id] = {
            "questions_left": num_of_questions,
            "correct_answers_count": 0,
            "total_questions": num_of_questions  
        }

        await ask_question(ctx)
    
    except asyncio.TimeoutError:
        await ctx.send('Sorry, you took too long to respond. Please start again by typing `$question`.')

async def ask_question(ctx):
    user_id = ctx.author.id
    quiz_state = user_quiz_states.get(user_id)

    if quiz_state and quiz_state["questions_left"] > 0:
        # Fetch a question
        qs, correct_answers, points = get_question()

        # Step 3: Ask the question
        await ctx.send(qs)

        def check_answer(m):
            return m.author == ctx.author and all(x.isdigit() for x in m.content.replace(',', '').replace(' ', ''))

        try:

            guess = await bot.wait_for('message', check=check_answer, timeout=30.0)
            user_answers = guess.content.replace(' ', '').split(',')
            user_answers = list(map(int, user_answers))  

            if sorted(user_answers) == sorted(correct_answers):
                user = guess.author
                await ctx.send('Correct answer! 🎉')
                update_score(user, points)
                quiz_state["correct_answers_count"] += 1
            else:
                await ctx.send('Wrong answer. 😢')

            quiz_state["questions_left"] -= 1

            if quiz_state["questions_left"] > 0:
                await ask_question(ctx)  
            else:

                total_correct = quiz_state["correct_answers_count"]
                total_questions = quiz_state["total_questions"] 
                await ctx.send(f"Quiz complete! You answered {total_correct}/{total_questions} questions correctly.")
                del user_quiz_states[user_id] 

        except asyncio.TimeoutError:
            await ctx.send('Sorry, you took too long to respond. Please start again by typing `$question`.')

@bot.command()
async def leaderboard(ctx):
    leaderboard_data = get_score()

    leaderboard_embed = discord.Embed(
        title="🏆 Quiz Leaderboard 🏆",
        description="Here are the top scorers:",
        color=discord.Color.gold()
    )

    leaderboard_embed.set_thumbnail(url="https://image.shutterstock.com/image-vector/trophy-icon-vector-gold-award-260nw-1785668225.jpg")

    if leaderboard_data:
        for rank in leaderboard_data:
            leaderboard_embed.add_field(name="", value=rank, inline=False)
    else:
        leaderboard_embed.add_field(name="Leaderboard", value="No scores yet.", inline=False)

    await ctx.send(embed=leaderboard_embed)
@bot.command()
async def rules(ctx):
    rules_embed = discord.Embed(
        title="📜 Quiz Rules 📜",
        description="Here are the rules for the quiz:",
        color=discord.Color.blue()
    )

    rules_embed.add_field(
        name="⏱️ Time Limit",
        value="You have 30 seconds to answer each question.",
        inline=False
    )

    rules_embed.add_field(
        name="✔️ Partial Marking",
        value="For questions with multiple correct answers, partial marking applies if you get some of them right. The answers must be reported as Comma Seperated Values i.e if both 1 and 2 are correct the answer reported must be 1,2",
        inline=False
    )

    rules_embed.add_field(
        name="🚫 Restricted Answering",
        value="Only the person who starts the quiz can answer the questions.",
        inline=False
    )

    rules_embed.set_footer(text="Good luck with the quiz!")

    await ctx.send(embed=rules_embed)

bot.run(defaultConfig.DISCORD_SDK)
