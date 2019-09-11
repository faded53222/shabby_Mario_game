import pygame
import sys
import time
import numpy
import math
import types
object_alive=[]
white = (255,255,255)
black=(0,0,0)
display_width,display_height=0,0
def text_objects(text, font):
	textSurface = font.render(text, True, white)
	return textSurface, textSurface.get_rect()
def message_display(text):
	screen.fill(black)	
	largeText = pygame.font.Font('freesansbold.ttf',60)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width*25/2),(display_height*25/2))
	screen.blit(TextSurf, TextRect)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()
picture_dic={}
object_dic={}
collision_dic={}
def build_dic(picture_dic_name,object_dic_name,collision_dic_name):
	f=open(picture_dic_name,'r')
	for each in f.readlines():
		temp=each.strip().split(" ")
		picture_dic[int(temp[0])]=temp[1]
	g=open(object_dic_name,'r')
	for each in g.readlines():
		temp=each.strip().split(" ")
		object_dic[int(temp[0])]=temp[1]
	k=open(collision_dic_name,'r')
	for each in k.readlines():
		temp=each.strip().split(" ")
		collision_dic[int(temp[0])]=int(temp[1])
build_dic("picture_dic.txt","object_dic.txt","collision_dic.txt")
locations=[]
collision_map=[]
def load_map(map_name):
	global display_width,display_height
	global locations
	global collision_map
	f=open(map_name,'r')
	temp=f.readline().split(" ")
	display_width=int(temp[0])
	display_height=int(temp[1])
	locations=[]
	special_deal=[]
	i=0
	j=0	
	for each in f.readlines():
		i+=1
		temp=each.strip().split(" ")
		location=[]
		collision=[]
		j=0
		for a_num in temp:
			j+=1
			location.append(int(a_num))
			collision.append(collision_dic[int(a_num)])
			if(int(a_num)==5):
				special_deal.append((5,(i,j)))
		locations.append(location)
		collision_map.append(collision)
	for one in special_deal:
		if one[0]==5:
			for t1 in range(one[1][0]-1,one[1][0]+2):
				for t2 in range(one[1][1]-1,one[1][1]+2):
					if t1!=one[1][0]+1 or t2!=one[1][1]:
						collision_map[t1][t2]=1
clock = pygame.time.Clock()
load_map("Mario_map.txt")
pygame.init()
size = display_width*25, display_height*25
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Mario")
background = pygame.image.load("background.PNG")
background_rect=background.get_rect()
background_rect.center=(display_width*25/2,display_height*25/2)
def draw_map():
	screen.blit(background, background_rect)
	for i in range(display_height+1):
		for j in range(display_width+1):
			if locations[i-1][j-1] in picture_dic.keys():
				screen.blit(pygame.image.load(picture_dic[locations[i-1][j-1]]),((j-1)*25,(i-1)*25))
jump_lab=0
mushroom_lab=0
class an_object:
	def __init__(self,px,py,pic,typu):
		self.picture=pygame.image.load(pic)
		self.picture2=pygame.transform.flip(self.picture,True,False)		
		self.rect=self.picture.get_rect()
		self.rect.left=px
		self.rect.top=py
		if typu==3:
			self.speedx=0
			self.speedy=0
			self.mov_left=0
		if typu==7:
			self.speedx=0
			self.speedy=-2
		if typu==9:
			self.speedx=-8
			self.speedy=0
		if typu==10:
			self.speedx=-4
			self.speedy=0
		self.typ=typu
	def draw(self):
		if self.typ==7:
			screen.blit(self.picture,self.rect)
			for i in range(display_height+1):
				for j in range(display_width+1):
					if locations[i-1][j-1] ==5:
						screen.blit(pygame.image.load(picture_dic[5]),((j-1)*25,(i-1)*25))
		else:	
			if self.mov_left==0:
				screen.blit(self.picture,self.rect)
			else:
				screen.blit(self.picture2,self.rect)
	def force(self,a):
		if a==1:
			self.speedx=self.speedx-3
			if self.speedx<-3:
				self.speedx=-3	
		if a==2:
			self.speedx+=3
			if self.speedx>3:
				self.speedx=3	
		if a==3:
			self.speedy-=4
			if self.speedy<-4:
				self.speedy=-4
	def deal_cases(self,what_to_deal,which_direction,which_location):
		global jump_lab
		global mushroom_lab
		if self.typ==3 or self.typ==9:
			if what_to_deal ==0 or what_to_deal ==4:
				if which_direction==0:
					self.speedx+=0.16
					if self.speedx>=-0.16:
						self.speedx=0
				if which_direction==1:
					self.speedx-=0.16
					if self.speedx<=0.16:
						self.speedx=0
				if which_direction==2 or which_direction==3 :
					self.speedy+=0.16
			if what_to_deal ==1 or what_to_deal==3:
				if which_direction==0 or which_direction==1:
					self.speedx=0
				if which_direction==2 or which_direction==3:
					self.speedy=0
					if(which_direction==3 and self.typ==3 ):
						jump_lab=0
			if what_to_deal==3:
				ly=which_location[0]
				lx=which_location[1]
				if locations[ly][lx]==4 and mushroom_lab==0:
					mushroom_lab=1
					to_append=an_object((lx)*25,(ly-1)*25,"9.PNG",9)
					object_alive.append(to_append)
				if locations[ly][lx]==8:
					time.sleep(2)
					message_display("YOU WIN")				
		if	self.typ==10 or self.typ==7 or self.typ==9: 
			if object_alive[0].rect.left+object_alive[0].rect.width>=self.rect.left\
			and object_alive[0].rect.left<=self.rect.left+self.rect.width\
			and object_alive[0].rect.top+object_alive[0].rect.height>=self.rect.top\
			and object_alive[0].rect.top<=self.rect.top+self.rect.height:
				if	self.typ==10 or self.typ==7:
					time.sleep(2)
					message_display("YOU DIED")
				if self.typ==9:
					for onoo in object_alive:
						if onoo.typ==9:
							object_alive.remove(onoo)
							object_alive[0].picture=pygame.image.load("3+.PNG")
							object_alive[0].picture2=pygame.transform.flip(object_alive[0].picture,True,False)	
		if self.typ==7:
			if what_to_deal ==4:
				if which_direction==2 or which_direction==3:
					self.speedy=-self.speedy
		if self.typ==10:
			if what_to_deal ==0  or what_to_deal ==4 :
				if which_direction==2 or which_direction==3 :
					self.speedy+=0.16
			elif what_to_deal ==1 or what_to_deal ==3:
				if which_direction==0 or which_direction==1:
					self.speedx=-self.speedx
				if which_direction==2 or which_direction==3:
					self.speedy=0
	def mov(self):
		if self.speedx<0:
			self.mov_left=1
		if self.speedx>0:
			self.mov_left=0
		x_mov=0
		what_to_deal_x=0
		x_happen_where=(0,0)
		if self.speedx!=0:
			y_range=range(math.floor(self.rect.top/25.0), \
			math.ceil((self.rect.top+self.rect.height)/25.0),1)
			duang_x=0
			max_x_mov1=250
			max_x_mov2=-250
			max_x_mov=0
			for a_y in y_range:
				dis1=math.floor((self.speedx+self.rect.left+self.rect.width)/25.0)
				dis2=math.floor((self.speedx+self.rect.left)/25.0)
				condi1=collision_map[a_y][dis1]
				condi2=collision_map[a_y][dis2]			
				if(self.speedx>0 and ((condi1!=0 and condi1!=4 and self.typ!=7) or (self.typ==7 and condi1==4) )):
					duang_x=1
					this_mov=dis1*25-(self.rect.left+self.rect.width)
					if this_mov<max_x_mov1:
						max_x_mov1=this_mov
						max_x_mov=max_x_mov1
						what_to_deal_x=condi1
						x_happen_where=(a_y,dis1)
				if(self.speedx<0 and ((condi2!=0 and condi2!=4 and self.typ!=7) or (self.typ==7 and condi2==4) )):
					duang_x=1
					this_mov=(dis2+1)*25-self.rect.left
					if this_mov>max_x_mov2:
						max_x_mov2=this_mov
						max_x_mov=max_x_mov2
						what_to_deal_x=condi2
						x_happen_where=(a_y,dis2)
			if duang_x==1:
				x_mov=max_x_mov
			else:
				x_mov=self.speedx
		y_mov=0
		what_to_deal_y=0
		y_happen_where=(0,0)
		if self.speedy!=0:
			x_range=range(math.floor(self.rect.left/25.0), \
			math.ceil((self.rect.left+self.rect.width)/25.0),1)
			duang_y=0
			max_y_mov1=250
			max_y_mov2=-250
			max_y_mov=0
			for a_x in x_range:
				dis1=math.floor((self.speedy+self.rect.top+self.rect.height)/25.0)
				dis2=math.floor((self.speedy+self.rect.top)/25.0)
				condi1=collision_map[dis1][a_x]
				condi2=collision_map[dis2][a_x]
				#print("self.speedy and self.rect.top",self.speedy,self.rect.top)
				#print("dis1,dis2,a_x and condi1,2: ",dis1,dis2,a_x,condi1,condi2)	
				if(self.speedy>0 and ((condi1!=0 and condi1!=4 and self.typ!=7) or (self.typ==7 and condi1==4) )):
					duang_y=1
					this_mov=dis1*25-(self.rect.top+self.rect.height)
					if this_mov<max_y_mov1:
						max_y_mov1=this_mov
						max_y_mov=max_y_mov1
						what_to_deal_y=condi1
						y_happen_where=(dis1,a_x)
				if(self.speedy<0 and ((condi2!=0 and condi2!=4 and self.typ!=7) or (self.typ==7 and condi2==4) )):
					duang_y=1
					this_mov=(dis2+1)*25-self.rect.top
					if this_mov>max_y_mov2:
						max_y_mov2=this_mov
						max_y_mov=max_y_mov2
						what_to_deal_y=condi2
						y_happen_where=(dis2,a_x)
			if duang_y==1:
				y_mov=max_y_mov
			else:
				y_mov=self.speedy
		self.deal_cases(what_to_deal_y,(self.speedy>0)+2,y_happen_where)
		self.deal_cases(what_to_deal_x,(self.speedx>0),x_happen_where)
		self.rect=self.rect.move((x_mov,y_mov))
def deal_objects():
	for i in range(display_height+1):
		for j in range(display_width+1):	
			if locations[i-1][j-1] in object_dic.keys():
				to_append=an_object((j-1)*25,(i-1)*25,object_dic[locations[i-1][j-1]],locations[i-1][j-1])
				if locations[i-1][j-1]==3:
					object_alive.insert(0,to_append)
				else:
					object_alive.append(to_append)					
deal_objects()
def mov_and_draw_objects():
	for one in object_alive:
		one.mov()
		one.draw()
jump_start_time=0
if __name__ == "__main__":
	key_keep=pygame.K_0
	while(1):
		clock.tick(600)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				key_keep=event.key
			if event.type == pygame.KEYUP:			
				key_keep=pygame.K_0
		if key_keep==pygame.K_a:
			object_alive[0].force(1)
		if key_keep==pygame.K_d:
			object_alive[0].force(2)
		if key_keep ==pygame.K_w:
			if jump_lab==0:
				jump_start_time=time.time()
				jump_lab=1
			if time.time()-jump_start_time < 0.6:
				object_alive[0].force(3)
		draw_map()		
		mov_and_draw_objects()
		pygame.display.flip()	
