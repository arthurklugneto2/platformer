from GameObjects.gate import Gate
from Objects.player import Player
from Objects.background import Background
from GameObjects.gameobject import GameObject
from GameObjects.coin import Coin
from GameObjects.waterSurface import WaterSurface
from Objects.water import Water
from Objects.ground import Ground
from Objects.enemy import Enemy

def player_check(player, obj,game):

    xoffset = 8 + obj.xoffset  # Helps with sprite size issues (b/c homemade collision system)
    yoffset = 10  # Helps with sprite size issues (b/c homemade collision system)

    topoffset = obj.topoffset  # Special for neccessary changes sprite

    # Player Horizontal Collision
    if player.x + xoffset < obj.x + obj.w and player.x + player.w - xoffset > obj.x \
            and player.last_y + player.h > obj.y + topoffset and player.last_y < obj.y + obj.h - yoffset and \
            (player.state == "RUN_LEFT" or (player.state == "JUMP" and player.pastState == "RUN_LEFT")):
        if obj.collectable:
            obj.collected = True
            obj.collisionEvent()
        else:
            player.x = obj.x + obj.w - xoffset
    elif player.x + player.w - xoffset > obj.x and player.x + xoffset < obj.x + obj.w \
            and player.last_y + player.h > obj.y + topoffset and player.last_y < obj.y + obj.h - yoffset and \
            (player.state == "RUN_RIGHT" or (player.state == "JUMP" and player.pastState == "RUN_RIGHT")):
                
        if obj.collectable:
            obj.collected = True
            obj.collisionEvent()
        else:
            player.x = obj.x - player.w + xoffset

    # Player Vertical Collision (Gravity stuff)
    if player.y + player.h >= obj.y + topoffset and player.y < obj.y + obj.h - yoffset \
            and player.x + xoffset < obj.x + obj.w \
            and player.x + player.w - xoffset > obj.x and player.state == "JUMP":
        if obj.collectable:
            obj.collected = True
            obj.collisionEvent()
        else:
            player.y = obj.y + obj.h - yoffset
            player.isOnGround = False
            player.jumpVel = 0
            player.currG = 0
    elif player.y + player.h >= obj.y + topoffset and player.y < obj.y + obj.h - yoffset \
            and player.x + xoffset < obj.x + obj.w \
            and player.x + player.w - xoffset > obj.x:
        if obj.collectable:
            obj.collected = True
            obj.collisionEvent()
        else:
            player.y = obj.y - player.h + topoffset
            player.gs += 1
            player.isOnGround = True

    # Gate Collision
    if isinstance(obj, Gate):
        w = h = 32
        if obj.x < player.x + w and obj.x + w > player.x and obj.y < player.y + h and obj.y + h > player.y:
            if player.keys > 0:
                player.keys -= 1
                obj.collisionEvent()
                game.objects.remove(obj)
                #game.quadTree.remove(obj)
                #game.quadTree.remove(obj,(obj.left,obj.top,obj.right,obj.bottom))
                game.removeQuadTreeItem(obj)

    # Water
    if isinstance(obj,Water) or isinstance(obj,WaterSurface):
        w = h = 32
        if obj.x < player.x + w and obj.x + w > player.x and obj.y < player.y + h and obj.y + h > player.y:
            player.isOnWater = True

def enemy_check(enemy, obj,game):
    if isinstance(obj, Player):
        # Check enemy collision
        if (obj.x+obj.eco[0]) < (enemy.x+enemy.co[0]) + (enemy.w+enemy.cs[0]) and \
           (obj.x+obj.eco[0]) + (obj.w+obj.ecs[0])> (enemy.x+enemy.co[0]) and \
           (obj.y+obj.eco[1]) < (enemy.y+enemy.co[1]) + (enemy.h+enemy.cs[1]) and \
           (obj.y+obj.eco[1]) + obj.h+obj.ecs[1] > (enemy.y+enemy.co[1]):
           obj.enemyContact(enemy,game)

def bullet_check(bullet,game):
    
    # If there is collision with ground remove the bullet
    collisions = [rect for rect in game.quadTree.querry(bullet.x,bullet.y,bullet.w,bullet.h)]
    if len(collisions) > 0:
        for collision in collisions:
            data = collision.data
            if isinstance(data,Ground):
                rect1 = {'x':bullet.x,'y':bullet.y,'width':bullet.w,'height':bullet.h}
                rect2 = {'x':data.x,'y':data.y,'width':data.w,'height':data.h}
                if rect1['x'] < rect2['x'] + rect2['width'] and \
                    rect1['x'] + rect1['width'] > rect2['x'] and \
                    rect1['y'] < rect2['y'] + rect2['height'] and \
                    rect1['y'] + rect1['height'] > rect2['y']:
                    
                    if bullet in game.objectsWeapon:
                        game.objectsWeapon.remove(bullet)

def bullet_enemy_check(bullet,game,enemies):

    # Check if there is collision with the enemy
    for enemy in enemies:
        rect1 = {'x':bullet.x,'y':bullet.y,'width':bullet.w,'height':bullet.h}
        rect2 = {'x':enemy.x,'y':enemy.y,'width':enemy.w,'height':enemy.h}
        if rect1['x'] < rect2['x'] + rect2['width'] and \
            rect1['x'] + rect1['width'] > rect2['x'] and \
            rect1['y'] < rect2['y'] + rect2['height'] and \
            rect1['y'] + rect1['height'] > rect2['y']:
                enemy.hurt()
                if bullet in game.objectsWeapon:
                        game.objectsWeapon.remove(bullet)
    
