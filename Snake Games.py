import tkinter
import random

# ===== KONFIGURASI =====
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# ===== WARNA ACAK =====
def random_color():
    return random.choice([
        "lime", "cyan", "orange",
        "pink", "purple", "blue",
        "gold", "green"
    ])

# ===== WINDOW =====
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    highlightthickness=0
)
canvas.pack()
window.update()

# ===== CENTER WINDOW =====
window.geometry(
    f"{window.winfo_width()}x{window.winfo_height()}+"
    f"{(window.winfo_screenwidth()-window.winfo_width())//2}+"
    f"{(window.winfo_screenheight()-window.winfo_height())//2}"
)

# ===== GAME STATE =====
snake_x = 5 * TILE_SIZE
snake_y = 5 * TILE_SIZE
food_x = 10 * TILE_SIZE
food_y = 10 * TILE_SIZE

snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0

# ===== RESTART FUNCTION =====
def restart_game():
    global snake_x, snake_y, food_x, food_y
    global snake_body, velocityX, velocityY, game_over, score

    snake_x = 5 * TILE_SIZE
    snake_y = 5 * TILE_SIZE
    food_x = random.randint(0, COLS - 1) * TILE_SIZE
    food_y = random.randint(0, ROWS - 1) * TILE_SIZE
    snake_body.clear()
    velocityX = 0
    velocityY = 0
    score = 0
    game_over = False
    restart_btn.place_forget()

# ===== BUTTON =====
restart_btn = tkinter.Button(
    window,
    text="RESTART",
    font=("Arial", 12, "bold"),
    bg="white",
    command=restart_game
)

# ===== INPUT =====
def change_direction(e):
    global velocityX, velocityY
    if game_over:
        if e.keysym.lower() == "r":
            restart_game()
        return

    if e.keysym in ("Up", "w") and velocityY != 1:
        velocityX, velocityY = 0, -1
    elif e.keysym in ("Down", "s") and velocityY != -1:
        velocityX, velocityY = 0, 1
    elif e.keysym in ("Left", "a") and velocityX != 1:
        velocityX, velocityY = -1, 0
    elif e.keysym in ("Right", "d") and velocityX != -1:
        velocityX, velocityY = 1, 0

# ===== GAME LOOP =====
def draw():
    global snake_x, snake_y, food_x, food_y, game_over, score

    canvas.delete("all")

    if not game_over:
        # gerak buntut
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i]["x"] = snake_body[i - 1]["x"]
            snake_body[i]["y"] = snake_body[i - 1]["y"]

        if snake_body:
            snake_body[0]["x"] = snake_x
            snake_body[0]["y"] = snake_y

        snake_x += velocityX * TILE_SIZE
        snake_y += velocityY * TILE_SIZE

        # nabrak tembok
        if snake_x < 0 or snake_x >= WINDOW_WIDTH or snake_y < 0 or snake_y >= WINDOW_HEIGHT:
            game_over = True

        # nabrak badan
        for part in snake_body:
            if snake_x == part["x"] and snake_y == part["y"]:
                game_over = True

        # makan
        if snake_x == food_x and snake_y == food_y:
            snake_body.append({
                "x": snake_x,
                "y": snake_y,
                "color": random_color()
            })
            food_x = random.randint(0, COLS - 1) * TILE_SIZE
            food_y = random.randint(0, ROWS - 1) * TILE_SIZE
            score += 1

    # ===== DRAW =====
    canvas.create_rectangle(
        snake_x, snake_y,
        snake_x + TILE_SIZE, snake_y + TILE_SIZE,
        fill="yellow"
    )

    for part in snake_body:
        canvas.create_rectangle(
            part["x"], part["y"],
            part["x"] + TILE_SIZE, part["y"] + TILE_SIZE,
            fill=part["color"]
        )

    canvas.create_rectangle(
        food_x, food_y,
        food_x + TILE_SIZE, food_y + TILE_SIZE,
        fill="red"
    )

    canvas.create_text(80, 30, text=f"Score: {score}", fill="white")

    canvas.create_text(
        WINDOW_WIDTH - 10, 25,
        text="Mukhlish Abdullah Said",
        fill="white",
        anchor="ne"
    )
    canvas.create_text(
        WINDOW_WIDTH - 10, 50,
        text="X TEL 07",
        fill="white",
        anchor="ne"
    )

    if game_over:
        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 30,
            text=f"GAME OVER\nScore: {score}",
            fill="white",
            font=("Arial", 20)
        )

        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 20,
            text="Tekan tombol R untuk melanjutkan.",
            fill="white",
            font=("Arial", 12)
        )

        restart_btn.place(
            x=WINDOW_WIDTH // 2 - 45,
            y=WINDOW_HEIGHT // 2 + 50
        )

    window.after(90, draw)

# ===== START =====
window.bind("<KeyRelease>", change_direction)
draw()
window.mainloop()