import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego CLICKERVELOZ")

# Colores
BACK = (200, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 150)
BLUE = (80, 80, 255)

# Fuente
FONT = 'verdana'

# Reloj
CLOCK = pygame.time.Clock()
FPS = 40

# Parámetros del juego
NUM_CARDS = 4
CARD_WIDTH, CARD_HEIGHT = 70, 100
CARD_SPACING = 100
START_X = 70
START_Y = 170

TIME_LIMIT = 10  # segundos
WIN_SCORE = 3

# Clase base para áreas
class Area:
    def __init__(self, x, y, width, height, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def set_color(self, color):
        self.fill_color = color

    def draw_fill(self):
        if self.fill_color:
            pygame.draw.rect(WINDOW, self.fill_color, self.rect)

    def draw_outline(self, color, thickness=1):
        pygame.draw.rect(WINDOW, color, self.rect, thickness)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

# Clase para etiquetas de texto
class Label(Area):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, width, height, color)
        self.text = ""
        self.font_size = 12
        self.text_color = (0, 0, 0)
        self.image = None

    def set_text(self, text, size=12, color=(0, 0, 0)):
        self.text = text
        self.font_size = size
        self.text_color = color
        font = pygame.font.SysFont(FONT, size)
        self.image = font.render(text, True, color)

    def draw(self, shift_x=0, shift_y=0):
        self.draw_fill()
        if self.image:
            WINDOW.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# Crear tarjetas
cards = []
for i in range(NUM_CARDS):
    x = START_X + i * CARD_SPACING
    card = Label(x, START_Y, CARD_WIDTH, CARD_HEIGHT, YELLOW)
    card.set_text(" ", 26)
    cards.append(card)

# Etiquetas de UI
time_label = Label(0, 0, 200, 50, BACK)
time_label.set_text("Tiempo:", 40, DARK_BLUE)

score_label = Label(380, 0, 200, 50, BACK)
score_label.set_text("Puntaje:", 40, DARK_BLUE)

timer_display = Label(50, 55, 100, 40, BACK)
timer_display.set_text("0", 40, DARK_BLUE)

score_display = Label(470, 55, 100, 40, BACK)
score_display.set_text("0", 40, DARK_BLUE)

# Variables del juego
start_time = pygame.time.get_ticks() / 1000  # en segundos
score_value = 0
wait_timer = 0
current_target = 0
game_over = False
victory = False

# Bucle principal
running = True
while running:
    dt = CLOCK.tick(FPS) / 1000  # delta time en segundos
    current_time = pygame.time.get_ticks() / 1000
    elapsed_time = int(current_time - start_time)

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            pos = event.pos
            for i, card in enumerate(cards):
                if card.collidepoint(pos):
                    if i == current_target:
                        card.set_color(GREEN)
                        score_value += 1
                    else:
                        card.set_color(RED)
                        score_value = max(0, score_value - 1)  # No bajar de 0
                    card.draw_fill()
                    wait_timer = 1  # Forzar actualización inmediata

    # --- Lógica del juego ---
    if not game_over:
        # Generar nueva tarjeta objetivo
        if wait_timer <= 0:
            wait_timer = 20  # ~0.5 segundos a 40 FPS
            current_target = random.randint(0, NUM_CARDS - 1)
            for i, card in enumerate(cards):
                card.set_color(YELLOW)
                if i == current_target:
                    card.set_text("CLICK", 18, (0, 0, 0))
                else:
                    card.set_text(" ", 26)
        else:
            wait_timer -= 1

        # Actualizar UI
        timer_display.set_text(str(elapsed_time), 40, DARK_BLUE)
        score_display.set_text(str(score_value), 40, DARK_BLUE)

        # Verificar condiciones de fin
        if score_value >= WIN_SCORE and elapsed_time <= TIME_LIMIT:
            game_over = True
            victory = True
        elif elapsed_time > TIME_LIMIT:
            game_over = True
            victory = False

    # --- Dibujo ---
    WINDOW.fill(BACK)

    # Dibujar UI
    time_label.draw(20, 20)
    score_label.draw(20, 20)
    timer_display.draw(0, 0)
    score_display.draw(0, 0)

    # Dibujar tarjetas
    for card in cards:
        card.draw(10, 30)  # centrado aproximado
        card.draw_outline(BLUE, 3)

    # Mostrar pantalla final
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((255, 255, 255))
        WINDOW.blit(overlay, (0, 0))

        result_text = Label(50, 200, 500, 60, None)
        if victory:
            result_text.set_text("¡VICTORIA!", 50, DARK_BLUE)
        else:
            result_text.set_text("¡DERROTA! Tiempo agotado", 40, DARK_BLUE)
        result_text.draw(0, 0)

        final_score = Label(50, 300, 500, 50, None)
        final_score.set_text(f"Puntaje final: {score_value}", 40, DARK_BLUE)
        final_score.draw(0, 0)

        pygame.display.update()
        pygame.time.delay(3000)  # 3 segundos
        running = False

    pygame.display.update()

# Salir
pygame.quit()