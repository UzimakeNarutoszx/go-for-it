import arcade as aa
import _locale
from pyglet.media import Player, load, StaticSource
import os
import sys
import time

# resource
base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(base_dir)

screen_width = 1280
screen_height = 720

class Start(aa.View):
    def __init__(self):
        self.bgm_player = Player()
        self.bgm_player.queue(load('other_files/sound.mp3'))
        self.bgm_player.loop = True
        self.bgm_player.play()
        
        super().__init__()
        self.sb = aa.Sprite('images/start.png')
        self.sb.position = 640, 200
        self.bg = aa.Sprite('images/bg1.jpg', scale=0.75)
        self.bg.position = 640, 360
        self.r = aa.Sprite('images/r.png', scale=1.2)
        self.r.position = 300, 320
        self.mb = aa.Sprite('images/mb2.jpg', scale=3)
        self.mb.position = 630, 360
        self.mb.alpha = 0
        self.a = False

    def on_draw(self):
        self.clear()
        self.bg.draw()
        aa.draw_rectangle_filled(640, 360, 1280, 720, (255, 255, 255, 50))
        self.r.draw()
        self.sb.draw()
        aa.draw_text("Go For It!", 640, 480, aa.color.ORANGE, 90, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("Experience of Participant_001", 640, 320, aa.color.ORANGE, 25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        self.mb.draw()

    def on_update(self, time):
        if self.a:
            self.mb.alpha += 3
            if self.mb.alpha == 255:
                self.window.show_view(content)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.sb.collides_with_point((x, y)):
            self.a = True

class Content(aa.View):
    def __init__(self):
        super().__init__()
        self.bg = aa.Sprite('images/bg2.jpg', scale=2)
        self.bg.position = 640, 360
        self.ball = aa.Sprite('images/ball.png', scale=0.15)
        self.ball.position = 640, -100
        self.ball.alpha = 0
        self.mover = False
        self.flyer = False
        self.kuang = aa.Sprite('images/kuang.png', scale=0.8)
        self.kuang.position = 640, 270
        self.mb = aa.Sprite('images/mb2.jpg', scale=3)
        self.mb.position = 630, 360
        self.mb.alpha = 255
        self.a = False
        self.b = True

    def on_draw(self):
        self.clear()
        self.bg.draw()
        aa.draw_rectangle_filled(640, 360, 1280, 720, (255, 255, 255, 50))
        self.kuang.draw()
        self.ball.draw()
        self.mb.draw()

    def on_update(self, time):
        self.move_ball()
        self.ball.update()
        if self.b:
            self.mb.alpha -= 3
            if self.mb.alpha == 0:
                self.mb.alpha = 0
                self.b = False
        if self.a:
            self.mb.alpha += 3
            if self.mb.alpha == 255:
                self.window.show_view(progress)

    def move_ball(self):
        if self.mover:
            self.ball.change_y -= 0.08
            self.ball.scale -= 0.0003
            if self.ball.center_y >= 500:
                self.flyer = True
            if self.ball.bottom <= 432 and self.flyer:
                self.a = True

    def on_mouse_release(self, x, y, button, modifiers):
        if self.kuang.collides_with_point((x, y)):
            self.mover = True
            self.ball.alpha = 255
            self.ball.change_angle = 30
            self.ball.change_y = 10

class Progress(aa.View):
    def __init__(self):
        super().__init__()
        self.map = 1
        self.rmap = 1

        self.bg = aa.Sprite('images/bg3.jpg')
        self.bg.position = 640, 360
        self.mb1 = aa.Sprite('images/mb1.jpg', scale=3)
        self.mb1.position = 640, 360
        self.mb1.alpha = 0
        self.mb2 = aa.Sprite('images/mb2.jpg', scale=3)
        self.mb2.position = 640, 360
        self.door = aa.Sprite('images/door.png', scale=0.2)
        self.ball = aa.Sprite('images/ball.png', scale=0.07)
        self.ball.alpha = 0
        self.ud = True
        # self.back = aa.Sprite('images/back.png')
        # self.back.position = 1188, 108
        # self.back.alpha = 0
            
        self.ppt = aa.SpriteList()
        for i in range(7):
            ppt = aa.Sprite(f'images/ppt{i+1}.jpg')
            ppt.alpha = 0
            ppt.position = 640, 360
            self.ppt.append(ppt)
        self.ppt[3].scale = 0.8
            
        self.a, self.b, self.c, self.d = False, False, False, True
        self.bf = 0
        self.bfing = False

        self.tx = aa.load_texture('texture/pic.png')
        self.txl = []
        self.index = 0
        for i in range(15):
            t = aa.load_texture(f'texture/z{i+1}.png')
            self.txl.append(t)
        self.lst = time.time()
        
        self.setup()

    def setup(self):
        self.tile_map = aa.load_tilemap(map_file=f'other_files/map{self.rmap}.tmx', scaling=2)
        self.scene = aa.Scene.from_tilemap(self.tile_map)
        self.player = self.scene.name_mapping["character"][0]
        self.player.move = 0
        self.ball.position = self.player.position
        self.player_camera = aa.Camera(screen_width, screen_height)
        self.physics_engine = aa.PhysicsEnginePlatformer(self.player, walls=self.scene.name_mapping['wall'], gravity_constant=4.0)

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.scene.draw()
        self.player_camera.use()
        self.door.draw()
        self.mb1.draw()
        self.ppt.draw()
        # self.back.draw()
        self.mb2.draw()
        self.ball.draw()

    def on_update(self, time):
        self.physics_engine.update()
        self.move_player_camera()
        self.abcd()
        self.position_change()
        self.collide()
        self.texture_change()
        self.ball.update()
                    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.bfing:
            if self.map == 6:
                self.c = True
            self.a = True
            # self.back.alpha = 0
            self.ppt[self.map - 1].alpha = 0
            self.map += 1
            self.bfing = False
            if self.map == 5:
                self.setup()

        else:
            self.player.change_x = 5

    def move_player_camera(self):
        camera_x = self.player.center_x - screen_width // 2
        camera_y = self.player.center_y - screen_height // 2
        if camera_x < 0:
            camera_x = 0
        if camera_y < 0:
            camera_y = 0
        if camera_x > 900:
            camera_x = 900
        camera_pos = camera_x, camera_y
        self.player_camera.move(camera_pos)

    def abcd(self):
        if self.a:
            self.mb1.alpha -= 3
            if self.mb1.alpha == 0:
                self.mb1.alpha = 0
                self.a = False
        elif self.b == True:
            self.mb1.alpha += 3
            if self.mb1.alpha == 255:
                self.b = False
                self.mb1.alpha = 255
                self.player.center_x - 18
                self.bfing = True
        elif self.d:
            self.mb2.alpha -= 3
            if self.mb2.alpha == 0:
                self.mb2.alpha = 0
                self.d = False
        elif self.c:
            self.mb2.alpha += 3
            if self.mb2.alpha == 255:
                self.window.show_view(result)

    def position_change(self):
        if self.map < 4:
            self.rmap = 1
        else:
            self.rmap = 2

        if map == 7:
            self.rmap = 0

        if self.player.center_x < 640:
            self.player.move = 640
        elif self.player.center_x > 1520:
            self.player.move = 1520
        else:
            self.player.move = int(self.player.center_x)
        if self.map == 1:
            self.door.position = 432, 216
            # self.back.position = 1188, 108
        if self.map == 2:
            self.door.position = 1008, 252
            # self.back.position = 1610, 108
        elif self.map == 3:
            self.door.position = 1548, 216
            # self.back.position = 1610, 108
        elif self.map == 4:
            self.door.position = 2088, 360
        elif self.map == 5:
            self.door.position = 504, 216
            # self.back.position = 1610, 108
        elif self.map == 6:
            self.door.position = 900, 144
        if self.map >= 2:
            self.mb1.position = self.player.move, 360 
            self.mb2.position = self.player.move, 360
            self.ppt[self.map - 1].position = self.player.move, 360

    def collide(self):
        if self.player.collides_with_sprite(self.door):
            self.player.change_x = 0
            self.player.center_x += 20
            self.b = True

        self.player.center_x += 1
        if self.player.collides_with_list(self.scene.name_mapping['wall']):
            self.player.change_y = 10
        else:
            self.player.change_y = 0
        self.player.center_x -= 1
        
        if self.bfing:
            self.ppt[self.map - 1].alpha = 255
            # self.back.alpha = 255

    def texture_change(self):
        self.ball.center_x = self.player.center_x + 20
        if self.ball.center_y >= self.player.center_y + 20 or self.ball.center_y <= self.player.center_y - 20:
            self.ball.center_y = self.player.center_y
            
        if self.ud:
            self.ball.center_y += 1
            if self.ball.center_y >= self.player.center_y + 10:
                self.ud = False
        else:
            self.ball.center_y -= 1
            if self.ball.center_y <= self.player.center_y - 10:
                self.ud = True
            
        if self.player.change_x == 0:
            self.player.texture = self.tx
            self.ball.alpha = 0
        else:
            self.ball.alpha = 255
            self.ball.change_angle = 10
            if time.time() - self.lst > 0.1:
                self.index = (self.index + 1) % len(self.txl)
                self.player.texture = self.txl[self.index]
                self.lst = time.time()

class Result(aa.View):
    def __init__(self):
        super().__init__()
        self.player_camera = aa.Camera(screen_width, screen_height)
        self.a = 0
        self.y = 0

    def on_update(self, time):
        self.player_camera.move((640, 360))
        
    def on_draw(self):
        self.clear()
        self.y += 1
        
        aa.draw_text('Thank You for Whatching', 960, self.y, color=aa.color.WHITE, font_size=50, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text("That's All", 960, self.y - 200, color=aa.color.WHITE, font_size=40, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Development Team 开发团队', 960, self.y - 400, color=aa.color.WHITE, font_size=40, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Director 总监 : Demo', 960, self.y - 500, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Programmer 程序员 : Demo', 960, self.y - 580, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Artist 美术设计 : Doubao AI    Deepseek', 960, self.y - 660, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Composer 作曲 : Udio', 960, self.y - 740, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Contents 内容与设计', 960, self.y - 820, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Participant_002    Participant_003    Participant_005', 960, self.y - 900, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        aa.draw_text('Participant_006    Participant_004(temporary)', 960, self.y - 980, color=aa.color.WHITE, font_size=25, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
        if self.y > 1600:
            if self.a < 255:
                self.a += 1
        aa.draw_text("Go For It!", 960, 400, (255, 120, 0, self.a), 90, font_name="Comic Sans MS", anchor_x='center', anchor_y='center')
    
w = aa.Window(screen_width, screen_height, 'Go For It')
start = Start()
content = Content()
progress = Progress()
result = Result()
w.show_view(start)
w.run()
