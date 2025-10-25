import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import time

st.set_page_config(page_title="Ancient Tales", layout="wide")

# -----------------------
# Helper functions
# -----------------------
def load_image(img_path):
    if os.path.exists(img_path):
        return Image.open(img_path)
    else:
        st.warning(f"⚠️ Image not found: {img_path}")
        return None

def draw_text(img, text, position=(20,20), font_size=40, color=(255,255,255)):
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    draw.text(position, text, fill=color, font=font)
    return img_copy

def draw_hearts(img, hearts, position=(50,50), size=40):
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)
    heart_symbol = "❤️"
    empty_heart = "🤍"
    text = heart_symbol*hearts + empty_heart*(4-hearts)
    draw.text(position, text, fill=(255,0,0), font=ImageFont.load_default())
    return img_copy

def draw_score_time(img, score, remaining, position=(50,100)):
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)
    text = f"Score: {score} | Time left: {remaining}s"
    draw.text(position, text, fill=(255,255,0), font=ImageFont.load_default())
    return img_copy

# -----------------------
# Session state defaults
# -----------------------
if "page" not in st.session_state: st.session_state.page = "menu"
if "character" not in st.session_state: st.session_state.character = None
if "score" not in st.session_state: st.session_state.score = 0
if "hearts" not in st.session_state: st.session_state.hearts = 4
if "start_time" not in st.session_state: st.session_state.start_time = time.time()
if "crew_index" not in st.session_state: st.session_state.crew_index = 0
if "diving_step" not in st.session_state: st.session_state.diving_step = 0
if "pearl_index" not in st.session_state: st.session_state.pearl_index = 0
if "ship_question_index" not in st.session_state: st.session_state.ship_question_index = 0

# -----------------------
# MENU + CHARACTER SELECTION
# -----------------------
if st.session_state.page == "menu":
    bg = load_image("menu_background.png")
    if bg:
        # Draw big title
        bg = draw_text(bg, "🏝️ Welcome to Ancient Tales", position=(50,50), font_size=80, color=(255,255,0))
        
        # Overlay characters
        nayhan = load_image("nayhan.png")
        dhabia = load_image("dhabia.png")
        if nayhan:
            bg.paste(nayhan.resize((300,300)), (100,200), nayhan.convert("RGBA"))
        if dhabia:
            bg.paste(dhabia.resize((300,300)), (500,200), dhabia.convert("RGBA"))
        
        st.image(bg, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play as Nayhan"):
            st.session_state.character = "nayhan"
            st.session_state.page = "seacoast"
    with col2:
        if st.button("Play as Dhabia"):
            st.session_state.character = "dhabia"
            st.session_state.page = "seacoast"

# -----------------------
# SEA COAST SCENE
# -----------------------
elif st.session_state.page == "seacoast":
    bg = load_image("underwater_background.png")
    if bg:
        bg = draw_text(bg, "🤖 Welcome to the Seaside Adventure!", position=(50,50), font_size=50)
        st.image(bg, use_container_width=True)

    char_img = load_image(f"{st.session_state.character}.png")
    if char_img:
        st.image(char_img, width=150)
    robot = load_image("robot.png")
    if robot: st.image(robot, width=100)
    kids = load_image("kids.png")
    if kids: st.image(kids, width=200)

    kid_questions = [
        ("Which game are they playing?", ["Tila", "Qubba", "Salam bil Aqaal", "Khosah Biboosah"], "Tila"),
        ("And the second game?", ["Khosah Biboosah", "Tila", "Mawiyah", "Alghimayah"], "Khosah Biboosah")
    ]
    for i, (q, opts, ans) in enumerate(kid_questions):
        choice = st.radio(q, opts, key=f"kidq{i}")
        if st.button(f"Submit Answer {i+1}", key=f"submit_kid{i}"):
            if choice == ans:
                st.success("✅ Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {ans}")

    if st.button("Proceed to Ship"):
        st.session_state.page = "ship_intro"

# -----------------------
# SHIP INTRO (CREW ONE BY ONE)
# -----------------------
elif st.session_state.page == "ship_intro":
    bg = load_image("ship_background.png")
    if bg: st.image(bg, use_container_width=True)
    char_img = load_image(f"{st.session_state.character}.png")
    if char_img: st.image(char_img, width=150)

    crew = [
        ("naukhada.png", "Naukhada - Leader of the ship."),
        ("ghais.png", "Ghais - Main pearl diver, strong and can hold breath for long periods."),
        ("seeb.png", "Seeb - Surface assistant, pulls diver up with rope."),
        ("naham.png", "Naham - Ship entertainer, sings 'Oh Ya Mal' for communication and motivation."),
        ("jallas.png", "Jallas -  Pearl inspector, opens oysters with a knife called Sakaria."),
        ("skuni.png", "Skuni - Helmsman, steers the ship per Naukhada's orders."),
        ("cook.png", "Tabakh - Responsible for food."),
        ("radif.png", "Radif - Assists Seeb with light tasks, learning the trade.")
    ]

    idx = st.session_state.crew_index
    img_name, desc = crew[idx]
    img = load_image(img_name)
    if img:
        img_text = draw_text(img, desc, position=(10,10), font_size=30, color=(255,255,0))
        st.image(img_text, width=300)

    if st.button("Next"):
        if idx < len(crew)-1:
            st.session_state.crew_index += 1
        else:
            st.session_state.page = "diving_process"
            st.session_state.diving_step = 0

# -----------------------
# DIVING PROCESS
# -----------------------
elif st.session_state.page == "diving_process":
    steps = [
        "1. Diver places nose clip and holds rope tied to weight.",
        "2. Descends to sea bottom quickly with weight.",
        "3. Collects oysters and puts in basket.",
        "4. Seeb pulls diver up when air low.",
        "5. Diver rests and repeats dives."
    ]
    step = st.session_state.diving_step
    bg = load_image("underwater_background.png")
    if bg:
        step_img = draw_text(bg, steps[step], position=(50,50), font_size=40, color=(255,255,255))
        st.image(step_img, use_container_width=True)

    if st.button("Next"):
        if step < len(steps)-1:
            st.session_state.diving_step += 1
        else:
            st.session_state.page = "pearl_game"
            st.session_state.start_time = time.time()
            st.session_state.hearts = 4
            st.session_state.pearl_index = 0

# -----------------------
# PEARL GAME
# -----------------------
elif st.session_state.page == "pearl_game":
    pearl_data = [
        ("pearl1.png", "What is the knife used to open oysters called?", ["Sakaria", "Mafak", "Tasa"], "Sakaria"),
        ("pearl2.png", "Large white/pinkish pearl?", ["Danah", "Yaqooti", "Jiwan"], "Danah"),
        ("pearl3.png", "Smaller white shiny pearl?", ["Yaqooti", "Yika", "Mauz"], "Yaqooti"),
        ("pearl4.png", "Yellowish/blueish pearl?", ["Batniyah", "Qimashi", "Rasiyah"], "Qimashi")
    ]
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 120 - elapsed)
    idx = st.session_state.pearl_index
    if idx < len(pearl_data):
        pearl_img, question, options, answer = pearl_data[idx]
        img = load_image(pearl_img)
        if img:
            img = draw_hearts(img, st.session_state.hearts)
            img = draw_score_time(img, st.session_state.score, remaining)
            st.image(img, use_container_width=True)
        choice = st.radio(question, options, key=f"pearl_q{idx}")
        if st.button("Submit Answer"):
            if choice == answer:
                st.success("✅ Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {answer}")
            st.session_state.pearl_index += 1
    else:
        if st.button("Proceed to Ship Quiz"):
            st.session_state.page = "ship_quiz"
            st.session_state.ship_question_index = 0

# -----------------------
# SHIP QUIZ
# -----------------------
elif st.session_state.page == "ship_quiz":
    ship_questions = [
        ("What is the Naukhada's role?", ["Captain / Chief", "Main diver", "Assistant diver"], "Captain / Chief"),
        ("What is Naham's role?", ["Motivator and singer", "Main diver", "Pearl inspector", "Cook"], "Motivator and singer"),
        ("Who steers the ship?", ["Trainee", "Skuni", "Naham", "Seeb"], "Skuni"),
        ("'Oh Ya Mal' is sung during…", ["Pearl diving trips", "Fishing trips", "Exploration", "Short trips"], "Pearl diving trips"),
        ("Why was 'Oh Ya Mal' sung?", ["Beauty of the sea", "Communication / morale", "No reason"], "Communication / morale")
    ]
    idx = st.session_state.ship_question_index
    if idx < len(ship_questions):
        q, opts, ans = ship_questions[idx]
        st.write(q)
        choice = st.radio("Choose answer:", opts, key=f"ship_q{idx}")
        if st.button("Submit Answer"):
            if choice == ans:
                st.success("✅ Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {ans}")
            st.session_state.ship_question_index += 1
    else:
        if st.button("Finish Adventure"):
            st.session_state.page = "summary"

# -----------------------
# SUMMARY
# -----------------------
elif st.session_state.page == "summary":
    bg = load_image("menu_background.png")
    if bg:
        summary_text = f"🎉 Adventure Complete!\nWell done, {st.session_state.character.capitalize()}!\nYour total score: {st.session_state.score}"
        img = draw_text(bg, summary_text, position=(50,50), font_size=50)
        st.image(img, use_container_width=True)

    if st.button("Play Again"):
        st.session_state.page = "menu"
        st.session_state.score = 0
        st.session_state.hearts = 4
        st.session_state.character = None
        st.session_state.crew_index = 0
        st.session_state.diving_step = 0
        st.session_state.pearl_index = 0
        st.session_state.ship_question_index = 0

