from curses import initscr,curs_set,newwin,endwin,delay_output,KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN,start_color,init_pair,color_pair,COLOR_BLACK,COLOR_GREEN,COLOR_YELLOW,COLOR_RED
from random import randrange
initscr()
start_color()
init_pair(1,COLOR_GREEN,COLOR_BLACK)
init_pair(2,COLOR_YELLOW,COLOR_BLACK)
init_pair(3,COLOR_RED,COLOR_BLACK)

curs_set(0)
class robot:
  pass
def myfunc(level):
  self=robot()
  self.count=0#counts the number of codes collected by the robot
  self.F=40 #size of square field
  self.sx=0#starting x coordinate of field
  self.sy=0#starting y coordinate of field
  self.win = newwin(self.F,self.F,self.sy,self.sx)
  self.win.keypad(1)
  self.win.nodelay(1)
  self.win.border('|','|','-','-','+','+','+','+')

  self.r=5 #size of square robot
  self.robot=[]
  x=[n for n in [randrange(1,self.F-1,1)]] #initial x coordinate of robot
  y=[n for n in [randrange(1,self.F-1,1)]] #initial y coordinate of robot
  self.robot.append([x[0],y[0]])#storing the coordinates of the robot



  self.d=2 #no of codes to be collected to diffuse the bomb
  self.e=2#number of enemy robots
  self.s=30 #no of points to be given on bomb diffusion
  self.level=level
  self.m=2#number of mines
  self.sm=3#length of each mine
  def bomb():
     self.bx=15#x coordinate of bomb
     self.by=4#y coordinate of bomb
     self.win.addch(self.bx,self.by,'B')
  def robo():
       for i in range(0,self.r):
          for j in range(0,self.r):
	      if self.robot==[]:
	         myfunc(self.level)
              else:
                 self.win.addch(self.robot[0][1]-i,self.robot[0][0]-j,'R',color_pair(1))
  def codes():
      l=[]
      for i in range(0,self.r):
         for j in range(0,self.r):
	     l.append([self.robot[0][0]-i,self.robot[0][1]-j])
      if self.level==1:
          w=self.d
      elif self.level==2:
          w=self.d+self.e
      elif self.level==3:
          w=self.d+self.e+self.m
      for i in range(0,w):
          c=[n for n in [[randrange(1,self.F-self.r,1),randrange(1,self.F-self.r,1)]] if n not in self.robot and n not in l] #randomly generating the coordinates of the codes to be collected by the robot
	  if c==[]:
	     myfunc(self.level)
	  else:
             l.append([c[0][0],c[0][1]]) #storing the previous positions of the codes ,so that it does not get repeated
             self.win.addch(c[0][1],c[0][0],'D')
  def enemy():
     l=[]
     for i in range(0,self.e):
         c=[n for n in [[randrange(1,self.F-self.r,1),randrange(1,self.F-self.r,1)]] if n not in self.robot and n not in l]
	 if c==[]:
	    myfunc(self.level)
	 else:
	    l.append([c[0][0],c[0][1]])
            self.win.addch(c[0][1],c[0][0],'E')
  def mines():
      l=[]
      for i in range(0,self.m):
          c=[n for n in [[randrange(1,self.F-self.r,1),randrange(1,self.F-self.r,1)]] if n not in self.robot and n not in l]

	  l.append([c[0][0],c[0][1]])
          for j in range(0,self.sm):
	      #l.append([c[0][0],c[0][1]-j])
	      if c==[]:
	         myfunc(self.level)
	      else:
	         self.win.addch(c[0][1]-j,c[0][0],'X')
  def run(key3,m):
     key=KEY_RIGHT
     pause=0
     while key!=27:
           ovr=0
           cnt=0
           flag=4
           self.win.addstr(0,18,' Codes collected : '+str(self.count)+' ')
           self.win.addstr(0,2,' Level : '+str(self.level)+' ')
           self.win.timeout(180-self.count*5-self.level*10)
           getkey = self.win.getch()
	   if getkey!=27:
	      if m==0:
                 if getkey==-1:
                    key=key
                 else:
                    key=getkey
              elif m==1:
	          key=key3
	          m=0
	   else:
	        key=getkey
           if key==KEY_RIGHT and pause==0:
              self.robot.insert(0,[self.robot[0][0]+1,self.robot[0][1]])
	      for j in range(0,self.r):
	             self.win.addch(self.robot[1][1]-j,self.robot[1][0]-(self.r-1),' ')
	             if self.win.inch(self.robot[0][1]-j,self.robot[0][0])==32:
		        cnt=cnt+1
              if cnt==self.r:
	         ovr=1
	      else:
	         ovr=0
	      cnt=0
           elif key==KEY_LEFT and pause==0:
              self.robot.insert(0,[self.robot[0][0]-1,self.robot[0][1]])
	      for j in range(0,self.r):
	              self.win.addch(self.robot[1][1]-j,self.robot[1][0],' ')
	              if self.win.inch(self.robot[0][1]-j,self.robot[0][0]-(self.r-1))==32:
		         cnt=cnt+1
              if cnt==self.r:
	         ovr=1
	      else:
	         ovr=0
              cnt=0
           elif key==KEY_UP and pause==0:
              self.robot.insert(0,[self.robot[0][0],self.robot[0][1]-1])
	      for j in range(0,self.r):
	           self.win.addch(self.robot[1][1],self.robot[1][0]-j,' ')
	           if self.win.inch(self.robot[0][1]-(self.r-1),self.robot[0][0]-j)==32:
	              cnt=cnt+1
              if cnt==self.r:
	         ovr=1
	      else:
	         ovr=0
	      cnt=0   
           elif key==KEY_DOWN and pause==0:
              self.robot.insert(0,[self.robot[0][0],self.robot[0][1]+1])
	      for j in range(0,self.r):
	          self.win.addch(self.robot[1][1]-(self.r-1),self.robot[1][0]-j,' ')
	          if self.win.inch(self.robot[0][1],self.robot[0][0]-j)==32:
	             cnt=cnt+1
	      if cnt==self.r:
	        ovr=1
	      else:
	        ovr=0
	      cnt=0  
           elif key==27:
              flag=2
              break
	   elif key==ord('p') or key==ord('P'):
	      if pause==0:
	         pause=1
		 key=KEY_RIGHT
		 continue
	      else:
	         key=KEY_RIGHT
		 pause=0
		 continue
	   else:
	     key=KEY_RIGHT
           if ovr==1 and pause==0:
	         level11()
           elif ovr==0 and pause==0:
	      if self.level==1:
	         flag=level10()
	      elif self.level==2:
	         flag=level20()
	      elif self.level==3:
	         flag=level30(key)
           if flag==0 or flag==1 or flag==2 or flag==3:
	      break
     endwin()

     F=40 #size of square field
     sx=0#starting x coordinate of field
     sy=0#starting y coordinate of field
     win = newwin(F,F,sy,sx)
     win.keypad(1)
     win.nodelay(1)
     win.border('|','|','-','-','+','+','+','+')
     if flag==0:
        win.addstr(15,15,'Bomb exploded.',color_pair(3))
	win.addstr(17,9,'Unsuccesful in diffusing Bomb.')
	win.addstr(19,12,'Score : ' +str(self.count*10),color_pair(1))
	
     if flag==1:
        win.addstr(15,15,'You Won.',color_pair(2))
	win.addstr(17,12,'Score : ' +str(self.s),color_pair(1))
     if flag==2:
        win.addstr(15,8,'You chose to quit the game.')
	win.addstr(17,12,'Score : '+str(self.count*10),color_pair(1))
     if flag==3:
        win.addstr(15,15,'Game Over.',color_pair(3))
	win.addstr(17,15,'Score : '+str(self.count*10),color_pair(1))
     win.refresh()
     delay_output(200)
     endwin()
     return flag
  def level11():
               self.robot.pop()
               for i in range(0,self.r):
	             for j in range(0,self.r):
                         self.win.addch(self.robot[0][1]-i,self.robot[0][0]-j,'R',color_pair(1))
  def level10():
             flag=4
             for i in range(0,self.r):
               for j in range(0,self.r):
                    if self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('D'):
                          self.count=self.count+1
                    elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('B'):                   
                       if self.count==self.d:
	                  flag=1
	                  break
	       
	               else:
	                flag=0
	                break
	            elif self.robot[0][1]-i>=self.F or self.robot[0][1]-i<=0:
	                 flag=3
		         break
	            elif self.robot[0][0]-j>=self.F or self.robot[0][0]-j<=0:
	                 flag=3
		         break
               if flag==1 or flag==0 or flag==3:
	         break
	     return flag
  def level20():
             flag=4
             for i in range(0,self.r):
               for j in range(0,self.r):
                    if self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('D'):
                          self.count=self.count+1
                    elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('B'):
                       if self.count>=self.d:
	                  flag=1
	                  break
	       
	               else:
	                flag=0
	                break
	            elif self.robot[0][1]-i>=self.F or self.robot[0][1]-i<=0:
	                 flag=3
		         break
	            elif self.robot[0][0]-j>=self.F or self.robot[0][0]-j<=0:
	                 flag=3
		         break
		    elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('E'):
		            self.count=self.count-1
	       if flag==0 or flag==1 or flag==3:
	            break
	     return flag
  def level30(key):
             flag=4
             for i in range(0,self.r):
               for j in range(0,self.r):
                    if self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('D'):
                          self.count=self.count+1
                    elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('B'):                   
                       if self.count>=self.d:
	                  flag=1
	                  break
	       
	               else:
	                flag=0
	                break
	            elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('X'):
		         if key==KEY_RIGHT:
			     key=KEY_LEFT
			 elif key==KEY_LEFT:
			     key=KEY_RIGHT
			 elif key==KEY_UP:
			     key=KEY_DOWN
			 elif key==KEY_DOWN:
			     key=KEY_UP
			 elif key==27:
			     flag=2
			     break

                         for k in range(0,self.sm):
			     if self.robot[0][1]-i+self.sm>=self.F or self.robot[0][1]-i-self.sm<=0:
			        flag=3
				break
			     if self.robot[0][0]-j-1>=self.F or self.robot[0][0]-j-1<=0:
			        flag=3
				break

	                     if self.win.inch(self.robot[0][1]-i-k,self.robot[0][0]-j)==ord('X'):
	                        self.win.addch(self.robot[0][1]-i-k,self.robot[0][0]-j,' ')

	                     if self.win.inch(self.robot[0][1]-i+k,self.robot[0][0]-j)==ord('X'):
	                        self.win.addch(self.robot[0][1]-i+k,self.robot[0][0]-j,' ')

                             if key==KEY_RIGHT:
	                            self.win.addch(self.robot[0][1]-i-k,self.robot[0][0]-j-1,'X')
                             if key==KEY_LEFT:
	                            self.win.addch(self.robot[0][1]-i-k,self.robot[0][0]-j+1,'X')
			     if key==KEY_UP:
			            self.win.addch(self.robot[0][1]-i-k+1+self.sm,self.robot[0][0]-j,'X')
			     if key==KEY_DOWN:
			            self.win.addch(self.robot[0][1]-i+k-1-self.sm,self.robot[0][0]-j,'X')

			 if flag==3:
			     break
			 flag=run(key,1)
			 if flag==0 or flag==1 or flag==2 or flag==3:
			    break

	            elif self.robot[0][1]-i>=self.F or self.robot[0][1]-i<=0:
	                 flag=3
		         break
	            
		    elif self.robot[0][0]-j>=self.F or self.robot[0][0]-j<=0:
	                 flag=3
		         break

		    elif self.win.inch(self.robot[0][1]-i,self.robot[0][0]-j)==ord('E'):
		            self.count=self.count-1
               if flag==1 or flag==0 or flag==3 or flag==2:
	         break
	     return flag
  b=robot()   
  bomb()
  robo()
  codes()
  if level==2 or level==3:
     b.posenemy=enemy()
  if level==3:
     mines()
  b.lvl=run(KEY_RIGHT,0)
  return b.lvl
if __name__ == "__main__":
     t=1
     a= myfunc(t)
     for t in range(2,4):
        if a==1:
	   a=myfunc(t)
