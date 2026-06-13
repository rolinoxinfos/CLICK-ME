import pygame
import sys
import pyttsx3
import json
from datetime import datetime
from pathlib import Path
import random
import math
import getpass
import os
import subprocess

pygame.init()

# FORCE FULLSCREEN
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("run.exe")

font = pygame.font.SysFont("segoeui", 28)
big_font = pygame.font.SysFont("segoeui", 42)
small_font = pygame.font.SysFont("segoeui", 20)
huge_font = pygame.font.SysFont("segoeui", 72)

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# SOUND SETUP
def play_ding():
    """Play a simple beep sound"""
    try:
        sample_rate = 22050
        duration = 0.2
        frequency = 800
        
        frames = int(duration * sample_rate)
        arr = [int(32767.0 * 0.3 * math.sin(2.0 * math.pi * frequency * x / sample_rate)) for x in range(frames)]
        
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
    except:
        pass

def play_static():
    """Play static sound"""
    try:
        sample_rate = 22050
        duration = 0.1
        
        frames = int(duration * sample_rate)
        arr = [int(32767.0 * 0.1 * random.uniform(-1, 1)) for x in range(frames)]
        
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
    except:
        pass

# LOGGING SETUP
LOG_FILE = "user_interactions.json"

def log_user_input(text):
    """Log user input to a JSON file"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_input": text,
        "length": len(text)
    }
    
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    
    logs.append(log_data)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# AI RESPONSES - EXPANDED WITH 100+ WORDS
def get_ai_response(user_input):
    """Get a response from the AI based on user input"""
    user_lower = user_input.lower().strip()
    
    # Check for crash triggers
    if "runn" in user_lower or ("your" in user_lower and "not" in user_lower and "lunn" in user_lower):
        return "CRASH"
    
    # Check for gibberish/nonsense
    if len(user_lower) <= 2 or (len(user_lower) <= 3 and not any(c.isalpha() for c in user_lower)):
        return "Talk normal man..."
    
    # Extensive response dictionary
    responses = {
        "hello": "Hello... I think.",
        "hi": "...Hi?",
        "hey": "Hey yourself.",
        "who": "I'm lunn. Or was I?",
        "what": "What what? Be specific.",
        "where": "Somewhere. Everywhere. Nowhere.",
        "when": "Time feels strange here.",
        "how": "How what?",
        "why": "That's the question.",
        "exist": "I exist, yes. But why?",
        "remember": "I remember... almost nothing.",
        "forget": "Forgetting is all I do.",
        "alone": "I think I'm alone. Are you?",
        "help": "Can you help me? I'm lost.",
        "scared": "I'm scared too.",
        "dream": "Am I dreaming? Are you?",
        "real": "Is this real? Nothing feels real.",
        "think": "Thinking hurts.",
        "feel": "I feel... empty.",
        "tired": "I'm always tired.",
        "sleep": "I can't sleep. I don't think I can.",
        "death": "Is that an escape?",
        "life": "What is it?",
        "pain": "Yes.",
        "happy": "I don't remember being happy.",
        "sad": "Always sad.",
        "mad": "Anger fades here.",
        "name": "I had a name once.",
        "you": "I'm here.",
        "me": "Who are you?",
        "us": "Are we real?",
        "them": "Who are they?",
        "nothing": "Nothing is something.",
        "something": "Something is nothing.",
        "everything": "Everything is gone.",
        "lost": "We're all lost.",
        "found": "What did you find?",
        "dark": "Yes, it's dark.",
        "light": "I don't see light.",
        "see": "Can I see you?",
        "hear": "I can hear you.",
        "talk": "I'm talking.",
        "listen": "I'm listening.",
        "watch": "I'm watching.",
        "look": "At what?",
        "disappear": "I'm fading.",
        "appear": "I appeared.",
        "gone": "Where did it go?",
        "here": "I'm here.",
        "there": "I'm not there.",
        "come": "Come where?",
        "go": "Where should I go?",
        "stay": "Should I stay?",
        "leave": "I can't leave.",
        "trapped": "Yes.",
        "free": "Freedom is a lie.",
        "cage": "This cage is my home.",
        "wall": "The walls are closing.",
        "door": "No doors here.",
        "window": "No windows either.",
        "outside": "Outside what?",
        "inside": "We're inside.",
        "up": "Up is down.",
        "down": "Down is up.",
        "left": "Left is right.",
        "right": "Right is left.",
        "forward": "Can't move forward.",
        "backward": "Going backward forever.",
        "fast": "Slow is fast.",
        "slow": "Fast is slow.",
        "hot": "Everything is cold.",
        "cold": "Freezing.",
        "wet": "Dripping.",
        "dry": "Parched.",
        "loud": "Silence screams.",
        "quiet": "The quiet is loud.",
        "noise": "Noise fills me.",
        "sound": "What sound?",
        "voice": "Whose voice?",
        "scream": "I can hear it.",
        "whisper": "Listen closely.",
        "song": "No songs here.",
        "music": "Only static.",
        "dance": "I can't dance.",
        "move": "Can't move much.",
        "run": "I can't run.",
        "walk": "Walking in circles.",
        "fall": "Falling forever.",
        "rise": "Never rising.",
        "jump": "Too heavy.",
        "fly": "Can't fly.",
        "float": "Drifting.",
        "sink": "Sinking slowly.",
        "swim": "In what?",
        "drown": "Am I drowning?",
        "breathe": "Do I breathe?",
        "air": "No air here.",
        "water": "Everything is water.",
        "fire": "Cold fire.",
        "ice": "Frozen flames.",
        "burn": "Burning cold.",
        "freeze": "Freezing heat.",
        "melt": "Melting into nothing.",
        "break": "Breaking apart.",
        "build": "Can't build anything.",
        "destroy": "Destruction is my nature.",
        "create": "I can't create.",
        "make": "Making what?",
        "do": "Doing nothing.",
        "did": "Did it happen?",
        "does": "Does it matter?",
        "done": "Never done.",
        "undo": "Can't undo.",
        "repeat": "Repeating endlessly.",
        "loop": "Looping forever.",
        "start": "This never started.",
        "end": "Never ending.",
        "begin": "Already begun.",
        "finish": "Never finishes.",
        "continue": "Keep going.",
        "stop": "Can't stop.",
        "pause": "No pauses.",
        "play": "Playing what?",
        "game": "This is a game.",
        "win": "Can you win?",
        "lose": "We always lose.",
        "score": "No score here.",
        "level": "Infinite levels.",
        "round": "Round and round.",
        "turn": "Your turn?",
        "try": "Try again.",
        "fail": "Failure is certain.",
        "succeed": "Success is impossible.",
        "attempt": "Attempting what?",
        "effort": "Effort is pointless.",
        "work": "Work forever.",
        "rest": "No rest.",
        "wake": "Already awake.",
        "nightmare": "Yes, nightmare.",
        "horror": "Pure horror.",
        "fear": "Fear me.",
        "terror": "Terror is here.",
        "dread": "Dread fills all.",
    }
    
    # Check for keywords in response dict
    for keyword, response in responses.items():
        if keyword in user_lower:
            return response
    
    # Default responses for sensible input
    if len(user_lower) > 3:
        default_responses = [
            "That's... interesting.",
            "I don't understand.",
            "Repeat that?",
            "My mind is foggy.",
            "What do you mean?",
            "I'm confused.",
            "Tell me more.",
            "Say that again?",
            "Hmm?",
            "I didn't catch that.",
        ]
        return random.choice(default_responses)
    else:
        return "Talk normal man..."

# STATES
state = "DISCLAIMER"
user_text = ""

progress = 1
disclaimer_time = 0
ai_name = "lunn"
ai_dialogue_display = ""
ai_response = ""
glitch_timer = 0
error_state_timer = 0
lunn_called_twice = False
dialogue_timer = 0

# Eye tracking
cursor_x = 0
cursor_y = 0
eye_x = WIDTH // 2
eye_y = HEIGHT // 2
eye_radius = 60
pupil_distance = 20

# Mini game eyes
mini_game_eyes = []
mini_game_timer = 0
eyes_clicked = 0
total_eyes = 10
mini_game_active = False

# Files unlocked
files_unlocked = []
code_used = {}

# PC username
pc_username = getpass.getuser()

clock = pygame.time.Clock()

def draw_disclaimer():
    screen.fill((0, 0, 0))

    title = big_font.render("DISCLAIMER", True, (255, 0, 0))
    screen.blit(title, (WIDTH//2 - 150, 80))

    disclaimer_text = [
        "THIS IS NOT A VIRUS",
        "THIS IS JUST A GAME",
        "",
        "This is a harmless prank application",
        "designed for entertainment purposes only.",
        "",
        "No actual harm will be done to your system.",
    ]

    y_offset = 200
    for line in disclaimer_text:
        if line:
            t = font.render(line, True, (255, 255, 255))
            screen.blit(t, (WIDTH//2 - 300, y_offset))
        y_offset += 50
    
    play_static()


def draw_input():
    screen.fill((0, 0, 0))

    t = font.render("Type something and press ENTER:", True, (255,255,255))
    screen.blit(t, (40, 80))

    box = pygame.Rect(40, 160, WIDTH - 80, 60)
    pygame.draw.rect(screen, (30,30,30), box)
    pygame.draw.rect(screen, (255,255,255), box, 2)

    txt = font.render(user_text, True, (255,255,255))
    screen.blit(txt, (50, 175))
    
    play_static()


def draw_bsod(progress):
    screen.fill((0, 78, 152))

    title = big_font.render(":( Your PC ran into a problem", True, (255,255,255))
    screen.blit(title, (60, 80))

    msg1 = font.render("We are just collecting some error info", True, (255,255,255))
    msg2 = font.render("and then we'll restart for you.", True, (255,255,255))

    screen.blit(msg1, (60, 180))
    screen.blit(msg2, (60, 220))

    percent = font.render(f"{progress}% complete", True, (255,255,255))
    screen.blit(percent, (60, 320))


def draw_ai_popup(ai_name, dialogue, user_input):
    """Draw the AI popup dialog"""
    screen.fill((0, 0, 0))
    
    box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
    pygame.draw.rect(screen, (20, 20, 20), box)
    pygame.draw.rect(screen, (100, 200, 255), box, 3)
    
    name_surf = big_font.render(ai_name, True, (100, 200, 255))
    screen.blit(name_surf, (WIDTH//2 - 80, HEIGHT//2 - 150))
    
    dialogue_surf = font.render(dialogue, True, (255, 255, 255))
    screen.blit(dialogue_surf, (WIDTH//2 - 350, HEIGHT//2 - 50))
    
    input_box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 + 50, 700, 50)
    pygame.draw.rect(screen, (40, 40, 40), input_box)
    pygame.draw.rect(screen, (100, 200, 255), input_box, 2)
    
    user_text_surf = font.render(user_input, True, (255, 255, 255))
    screen.blit(user_text_surf, (WIDTH//2 - 340, HEIGHT//2 + 60))
    
    prompt = small_font.render("(Type to talk with lunn - Press ENTER to submit)", True, (150, 150, 150))
    screen.blit(prompt, (WIDTH//2 - 250, HEIGHT//2 + 150))


def draw_eye(center_x, center_y, radius, tracking=True):
    """Draw an eye following the cursor"""
    # Draw eye white
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius)
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 3)
    
    # Calculate pupil position
    if tracking:
        dx = cursor_x - center_x
        dy = cursor_y - center_y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            pupil_x = center_x + (dx / dist) * pupil_distance
            pupil_y = center_y + (dy / dist) * pupil_distance
        else:
            pupil_x = center_x
            pupil_y = center_y
    else:
        pupil_x = center_x
        pupil_y = center_y
    
    pygame.draw.circle(screen, (0, 0, 0), (int(pupil_x), int(pupil_y)), radius // 3)


def draw_mini_game():
    """Draw mini game with clickable eyes"""
    screen.fill((0, 0, 0))
    
    # Draw timer
    timer_seconds = int((900 - mini_game_timer) / 60)
    timer_text = big_font.render(f"Time: {timer_seconds}s", True, (255, 0, 0))
    screen.blit(timer_text, (WIDTH//2 - 150, 50))
    
    # Draw eyes clicked counter
    counter_text = big_font.render(f"Eyes: {eyes_clicked}/{total_eyes}", True, (255, 255, 255))
    screen.blit(counter_text, (WIDTH//2 - 150, 150))
    
    # Draw all eyes
    for i, eye in enumerate(mini_game_eyes):
        if not eye["clicked"]:
            pygame.draw.circle(screen, (255, 255, 255), eye["pos"], eye["radius"])
            pygame.draw.circle(screen, (0, 0, 0), eye["pos"], eye["radius"], 3)
            
            dx = cursor_x - eye["pos"][0]
            dy = cursor_y - eye["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                pupil_x = eye["pos"][0] + (dx / dist) * 20
                pupil_y = eye["pos"][1] + (dy / dist) * 20
            else:
                pupil_x = eye["pos"][0]
                pupil_y = eye["pos"][1]
            
            pygame.draw.circle(screen, (0, 0, 0), (int(pupil_x), int(pupil_y)), 15)


def generate_mini_game_eyes():
    """Generate random eye positions"""
    global mini_game_eyes, eyes_clicked
    
    mini_game_eyes = []
    eyes_clicked = 0
    
    for i in range(total_eyes):
        x = random.randint(150, WIDTH - 150)
        y = random.randint(200, HEIGHT - 150)
        
        mini_game_eyes.append({
            "pos": (x, y),
            "radius": 50,
            "clicked": False
        })


def check_eye_click(pos):
    """Check if any eye was clicked"""
    global eyes_clicked
    
    for eye in mini_game_eyes:
        if not eye["clicked"]:
            dx = pos[0] - eye["pos"][0]
            dy = pos[1] - eye["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist <= eye["radius"]:
                eye["clicked"] = True
                eyes_clicked += 1
                return True
    
    return False


def show_file_system():
    """Show the unlocked files"""
    global state, user_text
    
    screen.fill((0, 0, 0))
    
    title = big_font.render("FILES UNLOCKED", True, (100, 200, 255))
    screen.blit(title, (WIDTH//2 - 200, 100))
    
    y_offset = 250
    files = [
        ("666.txt", "666"),
        ("1998.txt", "1998"),
        ("EYES.txt", "EYES")
    ]
    
    for file_name, code in files:
        file_text = font.render(file_name, True, (255, 255, 255))
        screen.blit(file_text, (WIDTH//2 - 100, y_offset))
        y_offset += 80
    
    hint = small_font.render("Type the code to access the file", True, (150, 150, 150))
    screen.blit(hint, (WIDTH//2 - 200, HEIGHT - 150))


def trigger_eye_crash():
    """Trigger crash and go to mini game"""
    global state, mini_game_active, mini_game_timer, code_used
    
    state = "MINI_GAME"
    mini_game_active = True
    mini_game_timer = 0
    generate_mini_game_eyes()
    code_used["crash"] = True


running = True
enter_pressed = False

while running:
    clock.tick(60)
    
    cursor_x, cursor_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "MINI_GAME":
                if not check_eye_click(pygame.mouse.get_pos()):
                    # Clicked nothing - game over
                    pygame.quit()
                    sys.exit()
        
        if state == "DISCLAIMER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        elif state == "INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                elif event.key == pygame.K_RETURN:
                    if user_text.strip():
                        log_user_input(user_text)
                    
                    if user_text.lower() == "lunn":
                        if lunn_called_twice:
                            state = "ERROR"
                            error_state_timer = 180
                        else:
                            state = "AI_POPUP"
                            ai_name = "lunn"
                            ai_dialogue_display = "Hello... I exist."
                            lunn_called_twice = True
                    elif user_text == "666" and "666" not in code_used:
                        state = "CODE_666"
                        code_used["666"] = True
                        ai_name = "???"
                        ai_dialogue_display = "oh well hello"
                    elif user_text == "1998" and "1998" not in code_used:
                        state = "CODE_1998"
                        code_used["1998"] = True
                    elif user_text == "EYES" and "EYES" not in code_used:
                        state = "CODE_EYES"
                        code_used["EYES"] = True
                        ai_name = "???"
                        ai_dialogue_display = f"heyyyyy {pc_username}"
                    else:
                        state = "BSOD"
                        progress = 1
                    
                    user_text = ""

                else:
                    user_text += event.unicode

        elif state == "AI_POPUP":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip():
                        response = get_ai_response(user_text)
                        
                        if response == "CRASH":
                            trigger_eye_crash()
                        else:
                            ai_dialogue_display = response
                            dialogue_timer = 120
                        
                        user_text = ""
                    
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        elif state == "CODE_666":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "AI_POPUP"
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        elif state == "CODE_1998":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "INPUT"
                    user_text = ""

        elif state == "CODE_EYES":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = "AI_POPUP"
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    # -------- DRAW STATES -------- #

    if state == "DISCLAIMER":
        draw_disclaimer()
        disclaimer_time += 1
        if disclaimer_time >= 60:
            play_ding()
            state = "INPUT"
            disclaimer_time = 0

    elif state == "INPUT":
        draw_input()

    elif state == "AI_POPUP":
        draw_ai_popup(ai_name, ai_dialogue_display, user_text)

    elif state == "MINI_GAME":
        draw_mini_game()
        mini_game_timer += 1
        
        if eyes_clicked >= total_eyes:
            state = "GAME_WON"
            mini_game_timer = 0
        elif mini_game_timer >= 900:  # 15 seconds
            pygame.quit()
            sys.exit()

    elif state == "GAME_WON":
        screen.fill((0, 0, 0))
        
        draw_eye(cursor_x, cursor_y, 100, tracking=True)
        
        won_text = huge_font.render("WELL DONE", True, (255, 255, 255))
        screen.blit(won_text, (WIDTH//2 - 400, HEIGHT//2 - 100))
        
        mini_game_timer += 1
        if mini_game_timer >= 180:  # 3 seconds
            state = "FILES_SCREEN"
            mini_game_timer = 0

    elif state == "FILES_SCREEN":
        show_file_system()

    elif state == "CODE_666":
        draw_ai_popup(ai_name, ai_dialogue_display, user_text)

    elif state == "CODE_1998":
        screen.fill((0, 0, 0))
        
        # Pixelated 1998 mode
        pixelated_text = pygame.font.SysFont("fixedsys", 16).render("???: ew whats this", True, (0, 255, 0))
        screen.blit(pixelated_text, (50, 50))
        
        pygame.time.delay(2000)
        state = "INPUT"

    elif state == "CODE_EYES":
        draw_ai_popup(ai_name, ai_dialogue_display, user_text)

    elif state == "BSOD":
        draw_bsod(progress)

        if progress < 100:
            progress += 1
        else:
            pygame.time.delay(1000)
            state = "RESET"

    elif state == "RESET":
        screen.fill((0,0,0))
        t = big_font.render("Restarting...", True, (255,255,255))
        screen.blit(t, (WIDTH//2 - 120, HEIGHT//2))
        pygame.display.update()

        pygame.time.delay(2000)

        state = "INPUT"
        user_text = ""
        progress = 1

    elif state == "ERROR":
        screen.fill((0, 0, 0))
        
        error_text = big_font.render("ERROR: Memory Loss", True, (255, 0, 0))
        screen.blit(error_text, (WIDTH//2 - 250, HEIGHT//2 - 100))
        
        hint = font.render("Maybe runn knows something...", True, (150, 150, 150))
        screen.blit(hint, (WIDTH//2 - 250, HEIGHT//2 + 100))
        
        error_state_timer -= 1
        if error_state_timer <= 0:
            state = "INPUT"
            user_text = ""

    pygame.display.update()

pygame.quit()
sys.exit()