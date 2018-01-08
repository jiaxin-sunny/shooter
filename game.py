#导入库
import math
import random
import pygame
from pygame.locals import *
 
#初始化pygame,设置展示窗口
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("打怪兽-zjx")
# key队列用来记录几个按键的情况：WASD；第一个对应W，第二个对应A等等
keys = [False, False, False, False]
#变量表示玩家初始的位置
playerpos = [100,100]
#跟踪玩家的精度，记录射出的箭头数和被击中坏蛋的数量，通过这些信息计算精确度
acc=[0,0]
#跟踪箭头
arrows=[]
#定义一个定时器，使得游戏里可以经过一段时间后就新建一只怪兽
badtimer = 100
badtimer1 = 0
badguys = [[640,100]]
healthvalue = 194
#声音模块
pygame.mixer.init()
 
#加载作为兔子的图片
player = pygame.image.load("resources/images/dude.png")
#草地
grass = pygame.image.load("resources/images/grass.png")
#城堡
castle = pygame.image.load("resources/images/castle.png")
#箭头
arrow = pygame.image.load("resources/images/bullet.png")
#坏蛋
badguyimg1 = pygame.image.load("resources/images/badguy.png")
#声明了一个图片的复制
badguyimg = badguyimg1
#
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
#加载声音文件
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
#配置音量
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
#加载游戏的背景音乐然后下一行让背景音乐一致不停的播放
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
 
#不停地循环执行接下来的部分。running跟踪游戏是否结束，exitcode跟踪玩家是否胜利
running = 1
exitcode = 0
while running:
	badtimer-=1

	#在给屏幕画任何东西之前用黑色进行填充
	screen.fill(0)
	for x in range(int(width/grass.get_width()+1)):
		for y in range(int(height/grass.get_height()+1)):
			screen.blit(grass,(x*100,y*100))
	screen.blit(castle,(0,30))
	screen.blit(castle,(0,135))
	screen.blit(castle,(0,240))
	screen.blit(castle,(0,345))
	
	#在屏幕的（100,100）坐标添加你加载的兔子图片
	#screen.blit(player, playerpos)
	
	#6.1 在屏幕加载兔子图片，并带有旋转功能
	#（首先获取鼠标和玩家的位置。然后将它们使用atan2函数。然后，获取通过atan2函数得出的角度和弧度）
	#(当兔子被旋转的时候，它的位置将会改变。所以你需要计算兔子新的位置，然后将其在屏幕上显示出来)
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
	playerrot = pygame.transform.rotate(player, 360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	
	#6.2 绘出箭头
	for bullet in arrows:
		index=0
		#箭头发射出来的速度‘8’
		velx=math.cos(bullet[0])*8
		vely=math.sin(bullet[0])*8
		bullet[1]+=velx
		bullet[2]+=vely
		#检查箭头是否超出了屏幕范围，如果超出，就删除这个箭头
		if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
			arrows.pop(index)
		index+=1
		#循环来把箭头根据相应的旋转画出来
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
			screen.blit(arrow1, (projectile[1], projectile[2]))
			
	#6.3 显示坏蛋
	#检查badtime是否为0，如果为0，创建一个獾然后重新设置badtime
	if badtimer==0:
		badguys.append([640, random.randint(50,430)])
		badtimer=100-(badtimer1*2)
		if badtimer1>=35:
			badtimer1=10
		else:
			badtimer1+=2
	
	index=0
	#循环更新獾的x坐标，检查獾是否超出屏幕范围，如果超出范围，将獾删掉
	for badguy in badguys:
		if badguy[0]<-64:
			badguys.pop(index)
		#坏蛋出现的速度
		badguy[0]-=2
		
		#6.3.1攻击城堡
		badrect=pygame.Rect(badguyimg.get_rect())
		badrect.top=badguy[1]
		badrect.left=badguy[0]
		if badrect.left<64:
			healthvalue -= random.randint(5,20)
			badguys.pop(index)
			hit.play()
		
		#6.3.2 检查碰撞
		index1=0
		for bullet in arrows:
			bullrect=pygame.Rect(arrow.get_rect())
			bullrect.left=bullet[1]
			bullrect.top=bullet[2]
			if badrect.colliderect(bullrect):
				acc[0]+=1
				badguys.pop(index)
				arrows.pop(index1)
			index1+=1
			enemy.play()
		
		#6.3.3 下一个坏家伙
		index+=1
	
	#画出所有的獾
	for badguy in badguys:
		screen.blit(badguyimg, badguy)

	#6.4 绘制时钟
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext, textRect)
	
	#6.5 绘制健康值
	screen.blit(healthbar, (5,5))
	for health1 in range(healthvalue):
		screen.blit(health, (health1+8,8))
	
	#更新屏幕
	pygame.display.flip()
	
	#检查一些新的事件，如果有退出命令，则终止程序的执行
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit() 
			exit(0)
		#检查是否有一个按键被放下或放开，然后，检查是哪一个键被按下或放开了，如果被按下或放开的键是你使用的，你就更新记录按键的变量
		#最终，需要更新playerpos变量作为按键后的反应
		if event.type == pygame.KEYDOWN:
			if event.key==K_w:
				keys[0]=True
			elif event.key==K_a:
				keys[1]=True
			elif event.key==K_s:
				keys[2]=True
			elif event.key==K_d:
				keys[3]=True
		if event.type == pygame.KEYUP:
			if event.key==K_w:
				keys[0]=False
			elif event.key==K_a:
				keys[1]=False
			elif event.key==K_s:
				keys[2]=False
			elif event.key==K_d:
				keys[3]=False
		#检查鼠标是否被点击了，如果点击了，就会得到鼠标的位置并且根据玩家和光标的位置计算出箭头的旋转角度
		#旋转角度的值就放在arrows这个数字里
		if event.type == pygame.MOUSEBUTTONDOWN:
			position = pygame.mouse.get_pos()
			acc[1]+=1
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
			shoot.play()
	
	#检查哪个键被按下，然后增加或减少玩家的x和y坐标
	if keys[0]:
		playerpos[1]-=5
	elif keys[2]:
		playerpos[1]+=5
	if keys[1]:
		playerpos[0]-=5
	elif keys[3]:
		playerpos[0]+=5
	
	#输赢检查
	#判断游戏时间是否到了(30s)
	if pygame.time.get_ticks()>=30000:
		running=0
		exitcode=1
	#判断城堡是否被摧毁了
	if healthvalue<=0:
		running=0
		exitcode=0
	#计算精确度
	if acc[1]!=0:
		accuracy=acc[0]*1.0/acc[1]*100
	else:
		accuracy=0

#输赢显示
if exitcode==0:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(gameover, (0,0))
	screen.blit(text, textRect)
else:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(youwin, (0,0))
	screen.blit(text, textRect)
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
	pygame.display.flip()