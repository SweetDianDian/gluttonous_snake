# -*- coding: utf-8 -*-
import pygame
import time
import random
import os

# 初始化pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_blue = (0, 0, 139)
purple = (147, 112, 219)
pink = (255, 182, 193)
orange = (255, 165, 0)
cyan = (0, 255, 255)
wall_color = (139, 69, 19)  # 棕色墙壁

# 设置游戏窗口为全屏
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()  # 获取屏幕的宽度和高度
pygame.display.set_caption('贪吃蛇大作战')

# 设置贪吃蛇的初始位置和速度
snake_block = 20
snake_speed = 15

# 创建时钟
clock = pygame.time.Clock()

# 加载字体
def get_font(size):
    try:
        # 在 macOS 上尝试直接使用系统字体文件
        font_path = '/System/Library/Fonts/PingFang.ttc'  # macOS 的中文字体路径
        return pygame.font.Font(font_path, size)
    except:
        try:
            # 如果找不到 PingFang 字体，尝试使用其他系统字体
            font_path = '/System/Library/Fonts/STHeiti Light.ttc'  # 另一个 macOS 中文字体
            return pygame.font.Font(font_path, size)
        except:
            # 如果所有尝试都失败，返回基础字体
            return pygame.font.SysFont(None, size)

# 显示分数
def show_score(score):
    score_font = get_font(35)
    score_surface = score_font.render(f'得分: {score}', True, white)
    screen.blit(score_surface, [10, 10])

# 绘制按钮
def draw_button(text, x, y, width, height, normal_color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, normal_color, (x, y, width, height))
        
    button_text = get_font(35).render(text, True, white)
    text_rect = button_text.get_rect(center=(x + width/2, y + height/2))
    screen.blit(button_text, text_rect)
    return False

# 更新皮肤配置
snake_skins = {
    "经典绿": {
        "body": (34, 177, 76),  # 更自然的绿色
        "border": (25, 120, 50),
        "pattern": (30, 150, 60)
    },
    "炫彩紫": {
        "body": (147, 112, 219),
        "border": (128, 0, 128),
        "pattern": (138, 43, 226)
    },
    "金蛇": {
        "body": (255, 215, 0),
        "border": (218, 165, 32),
        "pattern": (255, 200, 0)
    },
    "火焰蛇": {
        "body": (255, 69, 0),
        "border": (139, 0, 0),
        "pattern": (255, 140, 0)
    },
    "冰霜蛇": {
        "body": (135, 206, 235),
        "border": (70, 130, 180),
        "pattern": (176, 224, 230)
    }
}

# 添加全局变量存储当前选择的皮肤
current_skin = "经典绿"

# 添加速度选项
snake_speeds = {
    "慢": 10,
    "正常": 15,
    "快": 20,
    "超快": 25
}

# 添加全局变量存储当前选择的速度
current_speed = "正常"

# 修改贪吃蛇绘制函数
def our_snake(snake_block, snake_list):
    skin = snake_skins[current_skin]
    for x in snake_list:
        pygame.draw.rect(screen, skin["body"], [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(screen, skin["border"], [x[0], x[1], snake_block, snake_block], 1)

# 添加皮肤选择函数
def skin_menu():
    global current_skin
    selecting = True
    while selecting:
        screen.fill(dark_blue)
        
        # 绘制标题
        title_font = get_font(50)
        title = title_font.render("选择皮肤", True, yellow)
        title_rect = title.get_rect(center=(width/2, height/6))
        screen.blit(title, title_rect)
        
        # 绘制皮肤预览和选择按钮
        button_width = 200
        button_height = 50
        preview_size = 40
        start_y = height/4
        
        for i, (skin_name, skin_colors) in enumerate(snake_skins.items()):
            # 绘制皮肤名称
            name_text = get_font(25).render(skin_name, True, white)
            screen.blit(name_text, [width/4, start_y + i * 70])
            
            # 绘制皮肤预览
            preview_x = width/4 + 150
            preview_y = start_y + i * 70
            pygame.draw.rect(screen, skin_colors["body"], [preview_x, preview_y, preview_size, preview_size])
            pygame.draw.rect(screen, skin_colors["border"], [preview_x, preview_y, preview_size, preview_size], 1)
            
            # 绘制选择按钮
            if current_skin == skin_name:
                button_color = (0, 200, 255)
                button_text = "已选择"
            else:
                button_color = blue
                button_text = "选择"
                
            if draw_button(button_text, width/2 + 100, start_y + i * 70, 100, 40, button_color, (0, 200, 255)):
                current_skin = skin_name
        
        # 返回按钮
        if draw_button("返回", width/2 - 100, height - 100, 200, 50, red, (255, 0, 0)):
            selecting = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selecting = False

# 添加速度选择函数
def speed_menu():
    global current_speed
    selecting = True
    while selecting:
        screen.fill(dark_blue)
        
        # 绘制标题
        title_font = get_font(50)
        title = title_font.render("选择速度", True, yellow)
        title_rect = title.get_rect(center=(width/2, height/6))
        screen.blit(title, title_rect)
        
        # 绘制速度选项
        button_width = 200
        button_height = 50
        start_y = height/4
        
        for speed_name, speed_value in snake_speeds.items():
            button_color = blue if current_speed != speed_name else (0, 200, 255)
            if draw_button(f"{speed_name} ({speed_value})", width/2 - button_width/2, start_y, button_width, button_height, button_color, (0, 200, 255)):
                current_speed = speed_name  # 更新当前速度
                global snake_speed
                snake_speed = speed_value  # 更新游戏速度
            
            start_y += 60  # 每个按钮之间的间距
        
        # 返回按钮
        if draw_button("返回", width/2 - 100, height - 100, 200, 50, red, (255, 0, 0)):
            selecting = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    selecting = False

# 修改主菜单函数，添加速度选择按钮
def game_menu():
    menu = True
    while menu:
        screen.fill(dark_blue)
        
        # 绘制标题
        title_font = get_font(60)
        title = title_font.render("贪吃蛇大作战", True, yellow)
        title_rect = title.get_rect(center=(width/2, height/4))
        screen.blit(title, title_rect)
        
        # 绘制按钮
        button_width = 200
        button_height = 50
        button_x = width/2 - button_width/2
        
        # 添加操作说明
        instruction_font = get_font(20)
        instructions = [
            "游戏说明:",
            "使用方向键控制蛇的移动",
            "按 ESC 键暂停游戏",
            "按 Q 键退出游戏",
            f"当前皮肤: {current_skin}",
            f"当前速度: {current_speed}"
        ]
        
        for i, text in enumerate(instructions):
            instruction = instruction_font.render(text, True, white)
            screen.blit(instruction, [50, height - 150 + i * 30])
        
        # 开始游戏按钮
        if draw_button("开始游戏", button_x, height/2, button_width, button_height, blue, (0, 200, 255)):
            return "start"
            
        # 皮肤选择按钮
        if draw_button("更换皮肤", button_x, height/2 + 70, button_width, button_height, blue, (0, 200, 255)):
            return "skin"
        
        # 速度选择按钮
        if draw_button("调节速度", button_x, height/2 + 140, button_width, button_height, blue, (0, 200, 255)):
            return "speed"
            
        # 退出按钮
        if draw_button("退出", button_x, height/2 + 210, button_width, button_height, red, (255, 0, 0)):
            return "quit"

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"

# 添加墙壁配置
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self):
        pygame.draw.rect(screen, wall_color, self.rect)
        pygame.draw.rect(screen, black, self.rect, 2)  # 边框

# 创建墙壁列表
def create_walls():
    walls = []
    wall_thickness = 20
    
    # 随机生成四周的墙
    walls.append(Wall(0, 0, width, wall_thickness))  # 上墙
    walls.append(Wall(0, height - wall_thickness, width, wall_thickness))  # 下墙
    walls.append(Wall(0, 0, wall_thickness, height))  # 左墙
    walls.append(Wall(width - wall_thickness, 0, wall_thickness, height))  # 右墙
    
    # 随机生成内部墙壁
    for _ in range(random.randint(2, 5)):  # 随机生成2到5个内部墙壁
        wall_width = random.randint(20, 100)  # 随机墙宽
        wall_height = random.randint(20, 100)  # 随机墙高
        x = random.randint(wall_thickness, width - wall_thickness - wall_width)
        y = random.randint(wall_thickness, height - wall_thickness - wall_height)
        walls.append(Wall(x, y, wall_width, wall_height))
    
    return walls

# 添加新的游戏特性
class GameFeatures:
    def __init__(self):
        self.power_ups = {
            "speed_boost": {"duration": 5, "active": False, "start_time": 0},
            "shield": {"duration": 3, "active": False, "start_time": 0},
            "score_multiplier": {"duration": 10, "active": False, "start_time": 0},
        }
        self.effects = []

# 增强食物系统
class Food:
    def __init__(self, walls):
        self.food_types = {
            "normal": {"color": red, "points": 10, "chance": 70},
            "special": {"color": (255, 215, 0), "points": 30, "chance": 20},  # 金色
            "power": {"color": (138, 43, 226), "points": 50, "chance": 10}   # 紫色
        }
        self.current_type = "normal"
        self.walls = walls
        self.spawn()

    def spawn(self):
        wall_thickness = 20
        while True:
            self.x = random.randint(wall_thickness, width - wall_thickness - snake_block) // snake_block * snake_block
            self.y = random.randint(wall_thickness, height - wall_thickness - snake_block) // snake_block * snake_block
            
            # 随机选择食物类型
            rand = random.randint(1, 100)
            if rand <= self.food_types["normal"]["chance"]:
                self.current_type = "normal"
            elif rand <= self.food_types["normal"]["chance"] + self.food_types["special"]["chance"]:
                self.current_type = "special"
            else:
                self.current_type = "power"
            
            # 检查是否与墙壁重叠
            food_rect = pygame.Rect(self.x, self.y, snake_block, snake_block)
            if not any(wall.rect.colliderect(food_rect) for wall in self.walls):
                break

    def draw(self):
        food_color = self.food_types[self.current_type]["color"]
        
        # 绘制基础食物
        pygame.draw.rect(screen, food_color, [self.x, self.y, snake_block, snake_block])
        pygame.draw.rect(screen, yellow, [self.x, self.y, snake_block, snake_block], 1)
        
        # 添加食物光晕效果
        if self.current_type in ["special", "power"]:
            for i in range(3):  # 多层光晕
                glow_size = snake_block * (1.5 + i * 0.2)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                glow_alpha = int(128 / (i + 1))  # 渐变透明度
                glow_color = (*food_color, glow_alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                 (glow_size, glow_size), glow_size)
                screen.blit(glow_surface, 
                          (self.x - glow_size + snake_block/2, 
                           self.y - glow_size + snake_block/2))

# 增强蛇的类
class Snake:
    def __init__(self):
        self.body = []
        self.length = 1
        self.x = width / 2
        self.y = height / 2
        self.x_change = 0
        self.y_change = 0
        self.speed_multiplier = 1
        self.shield_active = False
        self.score_multiplier = 1
        self.direction = "right"  # 添加方向属性
        
    def move(self):
        if self.x_change != 0 or self.y_change != 0:
            # 更新方向
            if self.x_change > 0:
                self.direction = "right"
            elif self.x_change < 0:
                self.direction = "left"
            elif self.y_change > 0:
                self.direction = "down"
            elif self.y_change < 0:
                self.direction = "up"
                
            self.x += self.x_change * self.speed_multiplier
            self.y += self.y_change * self.speed_multiplier
            self.body.append((self.x, self.y))
            if len(self.body) > self.length:
                del self.body[0]

    def draw(self):
        skin = snake_skins[current_skin]
        
        # 绘制蛇身
        for i, segment in enumerate(self.body):
            # 渐变效果
            color = skin["body"]
            if isinstance(color, tuple):
                fade = max(0.5, 1 - i / len(self.body))
                color = tuple(int(c * fade) for c in color)
            
            # 绘制蛇身段落
            pygame.draw.rect(screen, color, [segment[0], segment[1], snake_block, snake_block])
            pygame.draw.rect(screen, skin["border"], [segment[0], segment[1], snake_block, snake_block], 1)
            
            # 为蛇身添加花纹
            if i % 2 == 0:
                pattern_color = tuple(max(0, c - 30) for c in color) if isinstance(color, tuple) else color
                pattern_rect = pygame.Rect(segment[0] + 4, segment[1] + 4, snake_block - 8, snake_block - 8)
                pygame.draw.rect(screen, pattern_color, pattern_rect)
        
        # 绘制蛇头
        head = self.body[-1] if self.body else (self.x, self.y)
        head_color = skin["body"]
        pygame.draw.rect(screen, head_color, [head[0], head[1], snake_block, snake_block])
        pygame.draw.rect(screen, skin["border"], [head[0], head[1], snake_block, snake_block], 1)
        
        # 绘制眼睛
        eye_color = (255, 255, 255)  # 白色眼睛
        pupil_color = (0, 0, 0)      # 黑色瞳孔
        eye_size = 6
        pupil_size = 3
        
        # 根据方向设置眼睛位置
        if self.direction == "right":
            eye_positions = [(head[0] + snake_block - 8, head[1] + 4),
                           (head[0] + snake_block - 8, head[1] + snake_block - 10)]
        elif self.direction == "left":
            eye_positions = [(head[0] + 4, head[1] + 4),
                           (head[0] + 4, head[1] + snake_block - 10)]
        elif self.direction == "up":
            eye_positions = [(head[0] + 4, head[1] + 4),
                           (head[0] + snake_block - 10, head[1] + 4)]
        else:  # down
            eye_positions = [(head[0] + 4, head[1] + snake_block - 8),
                           (head[0] + snake_block - 10, head[1] + snake_block - 8)]
        
        # 绘制眼睛和瞳孔
        for pos in eye_positions:
            pygame.draw.circle(screen, eye_color, (pos[0] + eye_size//2, pos[1] + eye_size//2), eye_size//2)
            pygame.draw.circle(screen, pupil_color, (pos[0] + eye_size//2, pos[1] + eye_size//2), pupil_size//2)
        
        # 绘制护盾效果
        if self.shield_active:
            shield_surface = pygame.Surface((snake_block * 1.5, snake_block * 1.5), pygame.SRCALPHA)
            shield_color = (0, 191, 255, 128)  # 半透明的蓝色
            pygame.draw.circle(shield_surface, shield_color, 
                             (snake_block * 0.75, snake_block * 0.75), snake_block)
            screen.blit(shield_surface, (head[0] - snake_block/4, head[1] - snake_block/4))

# 添加特效系统
class Effect:
    def __init__(self, x, y, color, size, duration):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.duration = duration
        self.start_time = time.time()
        
    def draw(self):
        current_time = time.time() - self.start_time
        if current_time < self.duration:
            alpha = int(255 * (1 - current_time / self.duration))
            effect_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(effect_surface, (*self.color, alpha), 
                             (self.size, self.size), self.size * (1 + current_time))
            screen.blit(effect_surface, (self.x - self.size, self.y - self.size))
            return True
        return False

# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False
    paused = False
    invincible = False  # 无敌状态

    walls = create_walls()
    snake = Snake()
    food = Food(walls)
    score = 0
    game_features = GameFeatures()
    effects = []

    while not game_over:
        while paused:
            screen.fill(dark_blue)
            pause_text = get_font(50).render("游戏暂停", True, white)
            screen.blit(pause_text, [width/3, height/3])
            
            if draw_button("继续游戏", width/2 - 100, height/2, 200, 50, blue, (0, 200, 255)):
                paused = False
            if draw_button("返回菜单", width/2 - 100, height/2 + 70, 200, 50, red, (255, 0, 0)):
                return  # 返回主菜单
                
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    if event.key == pygame.K_q:
                        game_over = True
                        paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                elif event.key == pygame.K_q:
                    game_over = True
                    paused = False
                elif event.key == pygame.K_LEFT and snake.x_change == 0:
                    snake.x_change = -snake_block
                    snake.y_change = 0
                elif event.key == pygame.K_RIGHT and snake.x_change == 0:
                    snake.x_change = snake_block
                    snake.y_change = 0
                elif event.key == pygame.K_UP and snake.y_change == 0:
                    snake.y_change = -snake_block
                    snake.x_change = 0
                elif event.key == pygame.K_DOWN and snake.y_change == 0:
                    snake.y_change = snake_block
                    snake.x_change = 0

        # 检查是否撞墙（无敌状态下不检查）
        if not invincible:
            next_pos = (snake.x + snake.x_change, snake.y + snake.y_change)
            for wall in walls:
                if wall.rect.collidepoint(next_pos):
                    game_close = True

        if not game_close:
            # 修改无敌状态下的移动控制
            if invincible:
                # 允许玩家手动控制，但保持自动寻找食物的功能
                if snake.x_change == 0 and snake.y_change == 0:  # 只在蛇没有移动时自动寻找食物
                    if snake.x < food.x:
                        snake.x_change = snake_block
                        snake.y_change = 0
                    elif snake.x > food.x:
                        snake.x_change = -snake_block
                        snake.y_change = 0
                    elif snake.y < food.y:
                        snake.y_change = snake_block
                        snake.x_change = 0
                    elif snake.y > food.y:
                        snake.y_change = -snake_block
                        snake.x_change = 0
            
            snake.move()
            
        screen.fill(dark_blue)
        
        # 绘制所有墙壁
        for wall in walls:
            wall.draw()
        
        # 绘制食物
        food.draw()
        
        # 绘制蛇
        snake.draw()

        # 修改食物碰撞检测
        # 检查是否吃到食物（使用碰撞矩形进行更精确的检测）
        snake_rect = pygame.Rect(snake.x, snake.y, snake_block, snake_block)
        food_rect = pygame.Rect(food.x, food.y, snake_block, snake_block)
        
        if snake_rect.colliderect(food_rect):
            # 添加吃到食物的特效
            effects.append(Effect(food.x, food.y, food.food_types[food.current_type]["color"], 
                                snake_block, 0.5))
            
            points = food.food_types[food.current_type]["points"] * snake.score_multiplier
            score += points
            
            if food.current_type == "power":
                # 随机激活一个能力提升
                power_up = random.choice(list(game_features.power_ups.keys()))
                game_features.power_ups[power_up]["active"] = True
                game_features.power_ups[power_up]["start_time"] = time.time()
                
                if power_up == "speed_boost":
                    snake.speed_multiplier = 1.5
                elif power_up == "shield":
                    snake.shield_active = True
                elif power_up == "score_multiplier":
                    snake.score_multiplier = 2
            
            food.spawn()
            snake.length += 1
        
        # 更新特效
        effects = [effect for effect in effects if effect.draw()]
        
        # 更新能力提升状态
        current_time = time.time()
        for power_up, status in game_features.power_ups.items():
            if status["active"]:
                if current_time - status["start_time"] > status["duration"]:
                    status["active"] = False
                    if power_up == "speed_boost":
                        snake.speed_multiplier = 1
                    elif power_up == "shield":
                        snake.shield_active = False
                    elif power_up == "score_multiplier":
                        snake.score_multiplier = 1

        show_score(score)
        pygame.display.update()
        clock.tick(snake_speed)

        # 游戏结束处理
        while game_close:
            screen.fill(dark_blue)
            game_over_text = get_font(50).render("游戏结束!", True, red)
            score_text = get_font(35).render(f"最终得分: {score}", True, white)
            screen.blit(game_over_text, [width/3, height/3])
            screen.blit(score_text, [width/3, height/2])
            
            if draw_button("复活无敌3秒", width/2 - 100, height/2 + 50, 200, 50, blue, (0, 200, 255)):
                # 重置游戏状态
                snake.x = width / 2
                snake.y = height / 2
                snake.x_change = 0
                snake.y_change = 0
                invincible = True
                game_close = False  # 继续游戏
                invincible_start_time = time.time()  # 记录复活时间
            
            if draw_button("返回菜单", width/2 - 100, height/2 + 120, 200, 50, red, (255, 0, 0)):
                return  # 返回主菜单
                
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        return gameLoop()

        # 检查无敌状态
        if invincible:
            if time.time() - invincible_start_time > 3:  # 3秒后取消无敌状态
                invincible = False

    pygame.quit()
    quit()

# 主循环
while True:
    try:
        choice = game_menu()
        if choice == "start":
            gameLoop()
        elif choice == "skin":
            skin_menu()
        elif choice == "speed":
            speed_menu()
        elif choice == "quit":
            break
    except KeyboardInterrupt:
        break

pygame.quit()
quit()