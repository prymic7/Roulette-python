
from variables import *
from chip import *
from button import *

class App:
    def __init__(self):
        self.appRun = True
        self.game = Game()

    def main_loop(self):
        while self.appRun :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.game.check_click()
                    print(self.game.table.all_bets)
                    print(len(self.game.bets_values))
                    print(len(self.game.bets_keys))



            window.fill("black")
            self.check_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def update(self):
        self.check_events()
        self.game.update()
        self.game.table.update()

    def draw(self):
        self.game.table.draw()
        self.game.draw()

    def check_events(self):
        self.game.table.check_events()

class Game:
    def __init__(self):
        self.table = Table(5000)
        self.action_text = "Place your bets please." # Spinning, Waiting(for bets)
        self.game_font = pygame.font.Font(None, game_font_size)
        self.number_font = pygame.font.Font(None, number_font_size)
        self.create_text()
        self.spinning = False
        self.button_image = pygame.image.load("img/button1.png")
        self.start_button = Button((width - 60, height - 120), self.button_image, "Spin", self.game_font, "white", "yellow")
        self.bet_back_button = Button((width - 60, height - 70), self.button_image, "Back", self.game_font, "white", "yellow")
        self.elapsed_time = 0
        self.start_time = 0
        self.time_now = 0 
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.black_numbers = [2, 4, 6, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 28, 31, 33, 35]
        self.number = random.randint(0, 36)
        self.bets_keys = []
        self.bets_values = []
        self.create_number_text()
        self.audio_chip_sound1 = pygame.mixer.Sound("audio/chipSound1.mp3")    
        self.audio_roulette_song1 = pygame.mixer.Sound("audio/rouletteSound.mp3")



    def check_box_clicked(self):
        if self.table.last_chip:
            mouse_position = pygame.mouse.get_pos()
            # Check classic box
            for i, rect in enumerate(self.table.classic_boxes):
                if rect.collidepoint(mouse_position):
                    self.audio_chip_sound1.play()
                    self.bets_values.append(self.table.active_chip_value)
                    self.bets_keys.append(i + 1)
                    self.table.money_placed += self.table.active_chip_value
                    self.create_text()
                    x = rect.x + rect.w / 2
                    y = rect.y + rect.h / 2
                    chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                    self.table.placed_chips.append(chip)
                    if i + 1 in self.table.all_bets:
                        self.table.all_bets[i + 1] += self.table.active_chip_value
                    else:
                        self.table.all_bets[i + 1] = self.table.active_chip_value

            #  Check zero box
            if self.table.zero_box[0].collidepoint(mouse_position):
                self.bets_values.append(self.table.active_chip_value)
                self.bets_keys.append(0)
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.zero_box[0].x + self.table.zero_box[0].w / 2
                y = self.table.zero_box[0].y + self.table.zero_box[0].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if 0 in self.table.all_bets:
                    self.table.all_bets[0] += self.table.active_chip_value
                else:
                    self.table.all_bets[0] = self.table.active_chip_value

            # Check 2 to 1 box click
            for i, rect in enumerate(self.table.two_to_one_boxes):
                if self.table.two_to_one_boxes[i].collidepoint(mouse_position):
                    self.bets_values.append(self.table.active_chip_value)
                    self.table.money_placed += self.table.active_chip_value
                    self.create_text()
                    x = rect.x + rect.w / 2
                    y = rect.y + rect.h / 2
                    chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                    self.table.placed_chips.append(chip)
                    if i == 0:
                        self.bets_keys.append("2to1B")
                        if "2to1B" in self.table.all_bets:
                            self.table.all_bets["2to1B"] += self.table.active_chip_value # box 2 to 1, bottom box(B)
                        else: 
                            self.table.all_bets["2to1B"] = self.table.active_chip_value
                    elif i == 1:
                        self.bets_keys.append("2to1B")
                        if "2to1M" in self.table.all_bets:
                            self.table.all_bets["2to1M"] += self.table.active_chip_value # M - middle
                        else:
                            self.table.all_bets["2to1M"] = self.table.active_chip_value 
                    elif i == 2:
                        self.bets_keys.append("2to1T")
                        if "2to1T" in self.table.all_bets:
                            self.table.all_bets["2to1T"] += self.table.active_chip_value # T - top
                        else:
                            self.table.all_bets["2to1T"] = self.table.active_chip_value


            # Check high low click
            if self.table.high_low_boxes[0].collidepoint(mouse_position):
                self.bets_values.append(self.table.active_chip_value)
                self.bets_keys.append("low")
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.high_low_boxes[0].x + self.table.high_low_boxes[0].w / 2
                y = self.table.high_low_boxes[0].y + self.table.high_low_boxes[0].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "low" in self.table.all_bets:
                    self.table.all_bets["low"] += self.table.active_chip_value
                else:
                    self.table.all_bets["low"] = self.table.active_chip_value
            elif self.table.high_low_boxes[1].collidepoint(mouse_position):
                self.bets_values.append(self.table.active_chip_value)
                self.bets_keys.append("high")
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.high_low_boxes[1].x + self.table.high_low_boxes[1].w / 2
                y = self.table.high_low_boxes[1].y + self.table.high_low_boxes[1].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "high" in self.table.all_bets:
                    self.table.all_bets["high"] += self.table.active_chip_value
                else:
                    self.table.all_bets["high"] = self.table.active_chip_value

            # Check one third click
            for i, rect in enumerate(self.table.one_third_boxes):
                if self.table.one_third_boxes[i].collidepoint(mouse_position):
                    self.bets_values.append(self.table.active_chip_value)
                    self.table.money_placed += self.table.active_chip_value
                    self.create_text()
                    if i == 0:
                        self.bets_keys.append("otL")
                        x = self.table.one_third_boxes[0].x + self.table.one_third_boxes[0].w / 2
                        y = self.table.one_third_boxes[0].y + self.table.one_third_boxes[0].h / 2
                        chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                        self.table.placed_chips.append(chip)
                        if "otL" in self.table.all_bets:
                            self.table.all_bets["otL"] += self.table.active_chip_value # box one third, left box(L)
                        else: 
                            self.table.all_bets["otL"] = self.table.active_chip_value
                    elif i == 1:
                        self.bets_keys.append("otM")
                        x = self.table.one_third_boxes[1].x + self.table.one_third_boxes[1].w / 2
                        y = self.table.one_third_boxes[1].y + self.table.one_third_boxes[1].h / 2
                        chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                        self.table.placed_chips.append(chip)
                        if "otM" in self.table.all_bets:
                            self.table.all_bets["otM"] += self.table.active_chip_value # M - middle
                        else:
                            self.table.all_bets["otM"] = self.table.active_chip_value 
                    elif i == 2:
                        self.bets_keys.append("otR")
                        x = self.table.one_third_boxes[2].x + self.table.one_third_boxes[2].w / 2
                        y = self.table.one_third_boxes[2].y + self.table.one_third_boxes[2].h / 2
                        chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                        self.table.placed_chips.append(chip)
                        if "otR" in self.table.all_bets:
                            self.table.all_bets["otR"] += self.table.active_chip_value # R - right
                        else:
                            self.table.all_bets["otR"] = self.table.active_chip_value

            # Check even odd click
            if self.table.even_odd_boxes[0].collidepoint(mouse_position):
                self.bets_keys.append("even")
                self.bets_values.append(self.table.active_chip_value)
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.even_odd_boxes[0].x + self.table.even_odd_boxes[0].w / 2
                y = self.table.even_odd_boxes[0].y + self.table.even_odd_boxes[0].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "even" in self.table.all_bets:
                    self.table.all_bets["even"] += self.table.active_chip_value
                else:
                    self.table.all_bets["even"] = self.table.active_chip_value
            elif self.table.even_odd_boxes[1].collidepoint(mouse_position):
                self.bets_keys.append("odd")
                self.bets_values.append(self.table.active_chip_value)
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.even_odd_boxes[1].x + self.table.even_odd_boxes[1].w / 2
                y = self.table.even_odd_boxes[1].y + self.table.even_odd_boxes[1].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "odd" in self.table.all_bets:
                    self.table.all_bets["odd"] += self.table.active_chip_value
                else:
                    self.table.all_bets["odd"] = self.table.active_chip_value

            # Check red black click
            if self.table.red_black_boxes[0].collidepoint(mouse_position):
                self.bets_keys.append("red")
                self.bets_values.append(self.table.active_chip_value)
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.red_black_boxes[0].x + self.table.red_black_boxes[0].w / 2
                y = self.table.red_black_boxes[0].y + self.table.red_black_boxes[0].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "red" in self.table.all_bets:
                    self.table.all_bets["red"] += self.table.active_chip_value
                else:
                    self.table.all_bets["red"] = self.table.active_chip_value
            elif self.table.red_black_boxes[1].collidepoint(mouse_position):
                self.bets_keys.append("black")
                self.bets_values.append(self.table.active_chip_value)
                self.table.money_placed += self.table.active_chip_value
                self.create_text()
                x = self.table.red_black_boxes[1].x + self.table.red_black_boxes[1].w / 2
                y = self.table.red_black_boxes[1].y + self.table.red_black_boxes[1].h / 2
                chip = Chip(self.table.last_chip, "bet", (x, y), 0)
                self.table.placed_chips.append(chip)
                if "black" in self.table.all_bets:
                    self.table.all_bets["black"] += self.table.active_chip_value
                else:
                    self.table.all_bets["black"] = self.table.active_chip_value
    
    def check_example_chip_click(self):
        mouse_position = pygame.mouse.get_pos()
        if self.table.yellow_chip_ex.image_rect.collidepoint(mouse_position):
            self.table.active_chip_value = self.table.yellow_chip_ex.value
            self.table.last_chip = self.table.yellow_chip_ex.color
        elif self.table.red_chip_ex.image_rect.collidepoint(mouse_position):
            self.table.active_chip_value = self.table.red_chip_ex.value
            self.table.last_chip = self.table.red_chip_ex.color
        elif self.table.blue_chip_ex.image_rect.collidepoint(mouse_position):
            self.table.active_chip_value = self.table.blue_chip_ex.value
            self.table.last_chip = self.table.blue_chip_ex.color
        elif self.table.orange_chip_ex.image_rect.collidepoint(mouse_position):
            self.table.active_chip_value = self.table.orange_chip_ex.value
            self.table.last_chip = self.table.orange_chip_ex.color
        elif self.table.green_chip_ex.image_rect.collidepoint(mouse_position):
            self.table.active_chip_value = self.table.green_chip_ex.value
            self.table.last_chip = self.table.green_chip_ex.color
        print(self.table.active_chip_value)

    def check_click(self):
        if not self.spinning:
            self.check_box_clicked()
            self.check_example_chip_click()

    def create_text(self):
        # Money text
        self.money_text_surface = self.game_font.render("Money: " + str(self.table.money), True, game_font_color)
        self.money_text_rect = self.money_text_surface.get_rect()
        self.money_text_rect.topleft =  20, (height - bottom_label_height / 2) - (self.money_text_rect.height / 2)

        # Placed money text
        self.placed_money_text_surface = self.game_font.render("Bet: " + str(self.table.money_placed), True, game_font_color)
        self.placed_money_text_rect = self.placed_money_text_surface.get_rect()
        self.placed_money_text_rect.topleft =  width - 60 - self.placed_money_text_rect.w, (height - bottom_label_height / 2) - (self.money_text_rect.height / 2)

        # Action text (Spinning, waiting for bets...)
        self.action_text_surface = self.game_font.render(self.action_text, True, action_font_color)
        self.action_text_rect = self.action_text_surface.get_rect()
        self.action_text_rect.topleft =  (width / 2) - (self.action_text_rect.width / 2), (height - bottom_label_height / 2) - (self.action_text_rect.height / 2)

    def create_number_text(self):
        self.number_text_surface = self.number_font.render(str(self.number), True, black_color)

        if self.number == 0:
            self.number_text_surface = self.number_font.render(str(self.number), True, green_color)
        else:
            for num in self.red_numbers:
                if num == self.number:
                    self.number_text_surface = self.number_font.render(str(self.number), True, red_color)
            for num in self.black_numbers:
                if num == self.number:
                    self.number_text_surface = self.number_font.render(str(self.number), True, black_color)

            self.number_text_rect = self.number_text_surface.get_rect()
            self.number_text_rect.center = 50, 50


    def handle_winnings(self):
        self.number = random.randint(0, 36)
        print(self.table.all_bets)
        winning_attributes = self.attributes_for_number(self.number)
        zero = winning_attributes[0]

        for key in self.table.all_bets:
            if key == self.number:
                self.table.money += self.table.all_bets[key] * 36
                break

        for key in self.table.all_bets:
            for attrib in winning_attributes:
                if not zero:
                    if key == attrib:
                        if key == "odd" or key == "even" or key == "red" or key == "black" or key == "low" or key == "high":
                            self.table.money += self.table.all_bets[key] * 2
                            continue
                        elif key == "otL" or key == "otM" or key == "otR" or key == "2to1T" or key == "2to1M" or key == "2to1B":
                            self.table.money += self.table.all_bets[key] * 3
                            continue

        self.create_text()
        self.create_number_text()

    def attributes_for_number(self, number):
        zero = False
        low_high = None
        even_odd = None
        third = None # L, M, R
        two_to_one = None # B, M, T
        red_black = None

        if number == 0:
            zero = True

        if not zero:
            if number % 2 != 0:
                even_odd = "odd"
            else:
                even_odd = "even"
            
            if number <= 18:
                low_high = "low"
            else:
                low_high = "hight"

            if number <= 12:
                third = "otL"
            elif number >= 13 and number <= 24:
                third = "otM"
            else:
                third = "otR"

            if number in self.black_numbers:
                red_black = "black"
            elif number in self.red_numbers:      
                red_black = "red"          

            first_row = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
            second_row = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
            third_row = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

            for num in first_row:
                if num == number:
                    two_to_one = "2to1T"

            for num in second_row:
                if num == number:
                    two_to_one = "2to1M"

            for num in third_row:
                if num == number:
                    two_to_one = "2to1B"

        attributes = [zero, low_high, even_odd, third, two_to_one, red_black]
        return attributes

    def draw_text(self):
        window.blit(self.money_text_surface, self.money_text_rect)
        window.blit(self.action_text_surface, self.action_text_rect)
        window.blit(self.placed_money_text_surface, self.placed_money_text_rect)
        if not self.spinning:
            window.blit(self.number_text_surface, self.number_text_rect)


    def draw(self):
        self.draw_text()
        self.start_button.draw()
        self.bet_back_button.draw()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        self.check_box_clicked()
        self.check_example_chip_click()
        if self.start_button.check_for_input(mouse_pos):
            self.spinning = True
            self.table.money -= self.table.money_placed
            self.table.money_placed = 0
            self.action_text = "Spinning.."
            self.start_time = time.perf_counter()
            self.audio_roulette_song1.play()
            self.create_text()

        if self.bet_back_button.check_for_input(mouse_pos):
            print(self.table.all_bets)
            print(len(self.bets_values))
            print(len(self.bets_keys))
            if len(self.table.placed_chips) > 0:
                self.table.money_placed -= self.table.placed_chips[-1].value
                self.table.placed_chips.pop()
                self.create_text()
                if len(self.bets_keys) > 0:
                    last_key = self.bets_keys[-1]
                    for key in self.table.all_bets:
                        if last_key == key:
                            if self.table.all_bets[key] > 0:
                                self.table.all_bets[key] -= self.bets_values[-1]
                                self.bets_values.pop()
                                self.bets_keys.pop()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.change_color(mouse_pos)
        self.bet_back_button.change_color(mouse_pos)
        self.time_now = time.perf_counter()
        if self.spinning:
            if self.time_now - self.start_time > 3:
                self.spinning = False
                self.handle_winnings()
                self.table.all_bets.clear()
                self.table.placed_chips.clear()
                self.audio_roulette_song1.stop()
                self.action_text = "Place your bets please."
                self.action_text_surface = self.game_font.render(self.action_text, True, action_font_color)
                self.action_text_rect = self.action_text_surface.get_rect()
                self.action_text_rect.topleft =  (width / 2) - (self.action_text_rect.width / 2), (height - bottom_label_height / 2) - (self.action_text_rect.height / 2)

class Table:
    def __init__(self, money):
        self.money = money
        self.placing_bet_money = 0
        self.yellow_chip_img_path = "img/yellowChip.png"
        self.table_img_path = "img/rouletteTable.jpg"
        self.table_img = pygame.image.load(self.table_img_path)
        self.table_img_rect = self.table_img.get_rect()
        self.example_chip_gap = 80
        self.active_chip_value = 0
        self.money_placed = 0
        self.bet_value = 0
        self.last_chip = None
        self.all_bets = {}

        #Set chip examples
        self.yellow_chip_ex = Chip("yellow", "example", (200, 330), 0)
        self.red_chip_ex = Chip("red", "example", (200 + self.example_chip_gap, 330), 0)
        self.blue_chip_ex = Chip("blue", "example", (200 + self.example_chip_gap * 2, 330), 0)
        self.orange_chip_ex = Chip("orange", "example", (200 + self.example_chip_gap * 3, 330), 0)
        self.green_chip_ex = Chip("green", "example", (200 + self.example_chip_gap * 4, 330), 0)

        #Classic box
        self.classic_box_x = 120 #First box x
        self.classic_box_y = 165 #First box y
        self.classic_box_width = 40
        self.classic_box_height = 55
        self.classic_boxes = []

        #Zero box
        self.zero_box_x = 80
        self.zero_box_y = 55
        self.zero_box_width = 40
        self.zero_box_height = 165
        self.zero_box = []

        #Two to one box
        self.two_to_one_box_x = self.classic_box_x * 11 #First box x
        self.two_to_one_box_y = 165 #First box y
        self.two_to_one_box_width = 40
        self.two_to_one_box_height = 55
        self.two_to_one_boxes = []

        #high low box
        self.high_low_box_x = self.classic_box_x #First box x
        self.high_low_box_y = self.classic_box_y + self.classic_box_height + self.classic_box_width + 3 # First box y
        self.high_low_box_width = 80
        self.high_low_box_height = 40
        self.high_low_boxes = []

        #one third box
        self.one_third_box_x = self.classic_box_x #First box x
        self.one_third_box_y = self.classic_box_y + self.classic_box_height + 2# First box y
        self.one_third_box_width = 160
        self.one_third_box_height = 40
        self.one_third_boxes = []

        #even odd box
        self.even_odd_box_x = self.classic_box_x + 80 #First box x
        self.even_odd_box_y = self.high_low_box_y # First box y
        self.even_odd_box_width = 80
        self.even_odd_box_height = 40
        self.even_odd_boxes = []

        #red black box
        self.red_black_box_x = self.classic_box_x + 80 * 2 #First box x
        self.red_black_box_y = self.high_low_box_y # First box y
        self.red_black_box_width = 80
        self.red_black_box_height = 40
        self.red_black_boxes = []

        self.colors = ["red", "yellow", "green", "blue", "purple", "pink"]
        self.create_boxes()
        self.placed_chips = []
        self.mini_green = Chip("green", "bet", (50, 50), 0)

    def create_chip_into_box():
        pass

    def create_boxes(self):
        x = self.classic_box_x
        y = self.classic_box_y

        # Create classic boxeses
        for i in range(1, 36, 3):
            self.rect = pygame.Rect(x, y, self.classic_box_width, self.classic_box_height)
            self.classic_boxes.append(self.rect)
            y -= self.classic_box_height

            self.rect = pygame.Rect(x, y, self.classic_box_width, self.classic_box_height)
            self.classic_boxes.append(self.rect)
            y -= self.classic_box_height

            self.rect = pygame.Rect(x, y, self.classic_box_width, self.classic_box_height)
            self.classic_boxes.append(self.rect)
            y -= self.classic_box_height

            x += self.classic_box_width
            y = self.classic_box_y

        #Create zero box
        self.rect = pygame.Rect(self.zero_box_x, self.zero_box_y, self.zero_box_width, self.zero_box_height)
        self.zero_box.append(self.rect)
        
        # Create two to one
        for i in range(1, 3, 3):
            self.rect = pygame.Rect(x, y, self.two_to_one_box_width, self.two_to_one_box_height)
            self.two_to_one_boxes.append(self.rect)
            y -= self.two_to_one_box_height

            self.rect = pygame.Rect(x, y, self.two_to_one_box_width, self.two_to_one_box_height)
            self.two_to_one_boxes.append(self.rect)
            y -= self.two_to_one_box_height

            self.rect = pygame.Rect(x, y, self.two_to_one_box_width, self.two_to_one_box_height)
            self.two_to_one_boxes.append(self.rect)
            y -= self.two_to_one_box_height


        #Create high low boxes
        self.rect = pygame.Rect(self.high_low_box_x, self.high_low_box_y, self.high_low_box_width, self.high_low_box_height)
        self.high_low_boxes.append(self.rect)
        self.rect = pygame.Rect(self.high_low_box_x + (self.one_third_box_width - 1) * 2.5, self.high_low_box_y, self.high_low_box_width, self.high_low_box_height)
        self.high_low_boxes.append(self.rect)

        #Create one third boxes
        x = self.classic_box_x
        y = self.one_third_box_y
        for i in range(1, 3, 3):
            self.rect = pygame.Rect(x, y, self.one_third_box_width, self.one_third_box_height)
            self.one_third_boxes.append(self.rect)
            x += self.one_third_box_width

            self.rect = pygame.Rect(x, y, self.one_third_box_width, self.one_third_box_height)
            self.one_third_boxes.append(self.rect)
            x += self.one_third_box_width

            self.rect = pygame.Rect(x, y, self.one_third_box_width, self.one_third_box_height)
            self.one_third_boxes.append(self.rect)
            x += self.one_third_box_width

        #Create even odd box
        self.rect = pygame.Rect(self.even_odd_box_x, self.even_odd_box_y, self.even_odd_box_width, self.even_odd_box_height)
        self.even_odd_boxes.append(self.rect)
        self.rect = pygame.Rect(self.even_odd_box_x -1 + 80 * 3, self.even_odd_box_y, self.even_odd_box_width, self.even_odd_box_height)
        self.even_odd_boxes.append(self.rect)

        #Create red black box
        self.rect = pygame.Rect(self.red_black_box_x, self.red_black_box_y, self.red_black_box_width, self.red_black_box_height)
        self.red_black_boxes.append(self.rect)
        self.rect = pygame.Rect(self.red_black_box_x + 80, self.red_black_box_y, self.red_black_box_width, self.red_black_box_height)
        self.red_black_boxes.append(self.rect)

    def choose_chip(self):
        if self.last_chip == "yellow":
            pass

    def draw_chips(self):
        self.yellow_chip_ex.draw()
        self.red_chip_ex.draw()
        self.blue_chip_ex.draw()
        self.orange_chip_ex.draw()
        self.green_chip_ex.draw()


    def draw(self):
        window.blit(self.table_img, self.table_img_rect)
        self.draw_chips()
        for chip in self.placed_chips:
            chip.draw() 
    
    def update(self):
        pass


    def check_events(self):
        pass
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('Roulette')

    app = App()
    app.main_loop()

    pygame.quit()
    sys.exit()