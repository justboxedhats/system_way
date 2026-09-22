import pygame
import asyncio

pygame.init()
pygame.font.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((593,593),pygame.RESIZABLE)
pygame.display.set_caption("System Way")
run_loop = True
frame_rate=30
# varrables

frames=0
mouse_pos=pygame.mouse.get_pos()

square_count=0
square_id_dic={} 
squ={}
node_offset=5
flags = ["home"]
bg_color=(0,0,0) 
basic_font = pygame.font.SysFont("Arial", 20)
selected_node=["","",""]
mouse_just_pressed=[False,False,False]
current_tool=""
user_type="" #user text imputs
mouse_scroll=0
scroll_speed=1
text_offset_x=0
text_offset_y=-20
camera_x=0
camera_y=0
zoom=1
# import pikl file and dictionary
settings={
    "pan_speed":-2,
    "tool_bg_x" : 250
}
pan_speed= settings["pan_speed"]
tool_bg_x= settings["tool_bg_x"]
nodes_dic = {1: {"type":"node","text": "node","x":100,"y":100, "width":100,"hight":100, "color": (255, 200, 200),"text_color":(0,0,0),"dragable":"True","sellectable":"True"},
            } 

connection_dic = {}
 
# -------------    Fuctions



def fonts_li (str="df"): #why wont it define the function!!!
        # basic_font = pygame.font.SysFont("Arial", 20)
    #print("loading font fuction")
    if str == "df":#20
        return pygame.font.SysFont("Arial", 20)
    elif str == "t1" : #65
        return pygame.font.SysFont("Arial", int(per2pix(7)), True ,False)
    elif str == "t2" :#50
        return pygame.font.SysFont("Arial", int(per2pix(6)), True ,False)
    elif str == "t3" :#30
        return pygame.font.SysFont("Arial", int(per2pix(4)), True ,False)
    elif str == "sp1" :#23
        return pygame.font.SysFont("Arial", int(per2pix(4)), True ,False)
    elif str == "sp2" :#50
        return pygame.font.SysFont("Arial", int(per2pix(6)), True ,False)
    else:
        print(f" {str} not in libary ")
 
def per2pix(percent,whole="s_w"):
    m_whole=whole
    if whole == "s_w":
        m_whole=screen.get_width()
    elif whole == "s_h":
        m_whole = screen.get_height()
    
    return int( (percent / 100) * m_whole)

def button(x, y, width, height, text, color=(0, 0, 0), text_color=(255, 255, 255),font="df"):
    n_font=fonts_li(font)
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = n_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    button_rect = pygame.Rect(x,y,width,height)
    screen.blit(text_surface, text_rect)
    if button_rect.collidepoint(pygame.mouse.get_pos()) and mouse_just_pressed[0]==True:
        if "clicked" not in flags: 
            flags.append("clicked")
        return True
    else: return False

def draw_line(x1, y1, x2, y2, color=(0, 0, 0), width=1):
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)

def draw_text(text, x, y, color=(0, 0, 0),font="df"):
    #print(f"font: {font}") 
    n_font=fonts_li(font)
    text_surface = n_font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def load_squares(dic={}):
    square_id_dic=dic 
    for I in range(len(square_id_dic)):
        #type, x, y,width,hight,color . text,text_color. dragable. code. image
        squ[list(square_id_dic.keys())[I]]=squares(list(square_id_dic.keys())[I],square_id_dic[list(square_id_dic.keys())[I]]["type"],square_id_dic[list(square_id_dic.keys())[I]]["x"]
        , square_id_dic[list(square_id_dic.keys())[I]]["y"],square_id_dic[list(square_id_dic.keys())[I]]["width"],square_id_dic[list(square_id_dic.keys())[I]]["hight"],square_id_dic[list(square_id_dic.keys())[I]]["color"])

        #["type"] =="visual" -> pass 

        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="text":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]
            if "font" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].font=square_id_dic[list(square_id_dic.keys())[I]]["font"]
            else: 
                square_id_dic[list(square_id_dic.keys())[I]]["font"]="df"
                squ[list(square_id_dic.keys())[I]].font=square_id_dic[list(square_id_dic.keys())[I]]["font"]
        
        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="node":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]
            
            if "font" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].font=square_id_dic[list(square_id_dic.keys())[I]]["font"]
            else: 
                square_id_dic[list(square_id_dic.keys())[I]]["font"]="df"
                squ[list(square_id_dic.keys())[I]].font=square_id_dic[list(square_id_dic.keys())[I]]["font"]

            if "dragable" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].dragable=square_id_dic[list(square_id_dic.keys())[I]]["dragable"]
            
            if "sellectable" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].sellectable=square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]

            if "defualt" in square_id_dic[list(square_id_dic.keys())[I]] : # dragable,sellectable,click_b,
                square_id_dic[list(square_id_dic.keys())[I]]["dragable"]="True"
                square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]="True"
                square_id_dic[list(square_id_dic.keys())[I]]["re_resize"]="True"

                squ[list(square_id_dic.keys())[I]].dragable=square_id_dic[list(square_id_dic.keys())[I]]["dragable"]
                squ[list(square_id_dic.keys())[I]].sellectable=square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]
                squ[list(square_id_dic.keys())[I]].re_resize=square_id_dic[list(square_id_dic.keys())[I]]["re_resize"]
                


        #squ[list(square_id_dic.keys())[I]].click_b=square_id_dic[list(square_id_dic.keys())[I]]["click_b"]
        
    #print(squ)

def render_squares ():
    for I in range(len(list(squ))):
        #print(squ[list(squ.keys())[I]].type)
        if squ[list(squ.keys())[I]].type == "visual":
            squ[list(squ.keys())[I]].draw()

        if squ[list(squ.keys())[I]].type == "s_visual":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].set_sellectable()      

        if squ[list(squ.keys())[I]].type == "text":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text, squ[list(squ.keys())[I]].x, squ[list(squ.keys())[I]].y, squ[list(squ.keys())[I]].text_color,squ[list(squ.keys())[I]].font)

        if squ[list(squ.keys())[I]].type == "node":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text, squ[list(squ.keys())[I]].x+camera_x, squ[list(squ.keys())[I]].y+camera_y, squ[list(squ.keys())[I]].text_color,squ[list(squ.keys())[I]].font)
            try:
                if squ[list(squ.keys())[I]].sellectable== "True":
                    squ[list(squ.keys())[I]].set_sellectable()      
            except:pass
            try : 
                if squ[list(squ.keys())[I]].dragable == "True":
                    squ[list(squ.keys())[I]].set_dragable(list(squ.keys())[I])
            except:pass
            try :  
                if squ[list(squ.keys())[I]].re_resize == "True":
                    squ[list(squ.keys())[I]].set_re_resize ()
            except:pass


        squ[list(squ.keys())[I]].click_b()        

def square_clear():
        global squ
        global selected_node 
        del squ
        selected_node=["","",""]
        squ={}

def load_connections(): 
    for node_id, connected_nodes in connection_dic.items():
        x = nodes_dic[node_id]["x"]
        y = nodes_dic[node_id]["y"]
        width = nodes_dic[node_id]["width"]
        hight = nodes_dic[node_id]["hight"]
        start_x = x
        start_y = y
        start_x+=camera_x
        start_y+=camera_y
        start_width = width
        start_height = hight
        start_center_x = start_x + start_width / 2
        start_center_y = start_y + start_height / 2

        for connected_node_id in connected_nodes:
            end_x= nodes_dic[connected_node_id]["x"]
            end_y = nodes_dic[connected_node_id]["y"]
            end_x+=camera_x
            end_y+=camera_y
            end_width = nodes_dic[connected_node_id]["width"]
            end_height = nodes_dic[connected_node_id]["hight"]
            end_center_x = end_x + end_width / 2
            end_center_y = end_y + end_height / 2

            draw_line(start_center_x, start_center_y, end_center_x, end_center_y, color=(180, 220, 210), width=5)

#type, x, y,width,hight,color . text,text_color. dragable. code. image
class squares:
    def __init__(self,name,type="visual", x=100, y=100, width=20, height=20, color=(0, 0, 0),text="", text_color=(0, 0, 0), image="", code=""):
        global square_count
        square_count+=1
        self.name=name
        self.x = x
        self.y = y
        self.code=code
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.type = type
    
    def __del__(self):
        global square_count
        square_count -=1
        #print("deleted  square")

    def draw(self):
        global selected_node ,nodes_dic

        if  "node" in self.type or "s_visual" in self.type : 
            
            self.rect=pygame.Rect((self.x+camera_x, self.y+camera_y, self.width, self.height))
  
            if  self.rect.x != nodes_dic[self.name]["x"] and self.rect.y != nodes_dic[self.name]["y"] : 
                nodes_dic[self.name]["x"]=self.x  
                nodes_dic[self.name]["y"]=self.y 
            
            pygame.draw.rect(screen,self.color, self.rect,border_radius=int(self.width/30)) 
            if self in selected_node :  
                pygame.draw.rect(screen, (200, 200, 200), self.rect, width=4)
                #draws the pale outline

            else:
                pygame.draw.rect(screen, (50, 80, 90), self.rect, width=4)
                #draws the basic outline
 
        else: 
            #print(f" color: {sef.color} , x: {self.x} , y: {self.y} , width: {self.width} , x: {self.height}")
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=int(self.width/30))
            self.rect=pygame.Rect((self.x, self.y, self.width, self.height))

    def set_dragable(self,name):
        # the first in selected node is for draging node
        global selected_node  

        mouse_x, mouse_y = pygame.mouse.get_pos()  
        
        if self.rect.collidepoint(mouse_x,mouse_y) and mouse_just_pressed[0] and selected_node[0]=="":  
            selected_node[0]=self
        if self == selected_node[0] and pygame.mouse.get_pressed()[0]:
            self.x = (mouse_x - self.width / 2) - camera_x
            self.y = (mouse_y - self.height / 2) - camera_y
            nodes_dic[self.name]["x"]=self.x  
            nodes_dic[self.name]["y"]=self.y # [name] should be changed to self.name

        elif self == selected_node[0] and pygame.mouse.get_pressed()[0] !=True: 
            #selected_node[1]=selected_node[0]
            selected_node[0]=""  
        
    def set_sellectable(self) :
        global selected_node 
        global flags 
        if "no_select" not in flags :
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_x,mouse_y) and mouse_just_pressed[0]:

                if  self not in selected_node:        
                    selected_node.insert(1,self)
                    del selected_node[3]
                elif self in selected_node:
                    selected_node[selected_node.index(self)] =""

    def click_b (self) : 
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0],mouse_pos[1]) and mouse_just_pressed[0] and "clicked" not in flags :
            flags.append("clicked")
            print(f"flages: {flags}") 

    def draw_text(self, text, x, y, color=(0, 0, 0),font="df"):
        n_font=fonts_li(font)                                       #print(f"N_F: {n_font}  O_F: {font}")
        if self.text != "":
            text_surface = n_font.render(text, True, color,None,int(self.width))
            self.text_surf= text_surface # resize function
            screen.blit(text_surface, (x, y))
 


#"image_bg":{"type":"","x":,"y","width","hight","color","text","text_color"}
 #type, x, y,width,hight,color . text,text_color. dragable. code. image
home_rec_list={
    "tital":{"type":"text","x":per2pix(10),"y":8,"width":per2pix(80),"hight":70,"color":(170,190,160,100),"text":"System Way","text_color":(150, 90, 110), "font":"t1" },
    "ver_bg":{"type":"text","x":per2pix(55),"y":80,"width":per2pix(35),"hight":30,"color":(160, 180, 150),"text":"web ver 1.0 (beta)","text_color":(150, 90, 110), "font":"sp1"},
    "intro_bg":{"type":"text","x":per2pix(9),"y":per2pix(23,"s_h"),"width":per2pix(80),"hight":per2pix(30,"s_h") ,"color":(150, 170, 140),"text":"Hello, welcome to the web version of system way, a program designed to help you develop systems and diagrams. Please note that the web version of the program is a cutdown version, please use the executable version for more features","text_color":(200, 210,255),"font":"t3"},
    "option_bg":{"type":"visual","x":per2pix(25),"y":per2pix(55,"s_h"),"width":per2pix(50),"hight":per2pix(40,"s_h") ,"color":(150, 170, 140)},
    } 
load_squares(home_rec_list)
render_squares()

nodes_dic["tool_bar_bg"]={"type":"visual", "x":per2pix(35),"y":per2pix(94,"s_h"),"width":per2pix(50),"hight":per2pix(7,"s_h"),"color":(120,200,180)}

async def main():
    global zoom,run_loop, mouse_scroll,selected_node,current_tool,connection_dic,flags,user_type,camera_x,camera_y,bg_color,frames, mouse_pos,mouse_click, mouse_just_pressed
    
    while run_loop:
        mouse_just_pressed=[False,False,False]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False

            elif event.type == pygame.KEYDOWN and "type_t_f" in flags:
                if event.key == pygame.K_RETURN:
                    flags.remove("typing_t_f")
                    flags.append("press_true")
                elif event.key == pygame.K_ESCAPE:
                    flags.remove("typing_t_f")
                    flags.append("press_false")
            elif event.type == pygame.KEYDOWN and "typing" in flags:
                
                if event.key == pygame.K_RETURN:
                    flags.remove("typing")
                    flags.append("fin_typing")
                elif event.key == pygame.K_ESCAPE:
                    flags.remove("typing")
                    flags.append("end_typing")
                elif event.key == pygame.K_BACKSPACE:
                    user_type = user_type[:-1]
                else:
                    user_type += event.unicode

                print(user_type) 


            elif event.type == pygame.MOUSEBUTTONDOWN:
                # event.button maps: 1=Left, 2=Middle, 3=Right
                if 1 <= event.button <= 3:
                    mouse_just_pressed[event.button - 1] = True
                    print(mouse_just_pressed)
            """if event.type == pygame.MOUSEWHEEL:
                mouse_scroll=event.y
                print(event.y)
            else:
                mouse_scroll=0"""  

        #print(square_count)
        if "home" in flags: #--************
            screen.fill((215, 225, 200)) 
            render_squares()
                    # buttons for the home screen 

            if button(per2pix(27.5), per2pix(60,"s_h"), per2pix(44), per2pix(12,"s_h"), "Workspace", (140, 100, 100), (255, 255, 255)):
                print(square_count)
                flags.clear()
                bg_color=(190,190,180) 
                flags.append("workspace")
                square_clear()
                load_squares(nodes_dic)

            """if button(per2pix(27.5), per2pix(79, "s_h"), per2pix(44), per2pix(7,"s_h"), "Settings", (150, 100, 100), (255, 255, 255)):
                flags.clear()
                flags.append("settings")"""
                
            if button(per2pix(27.5), per2pix(75, "s_h"), per2pix(44), per2pix(12,"s_h"), "quit", (160, 100, 100), (255, 255, 255)):
                run_loop = False
            

        if "load" in flags: #--************
            screen.fill((200, 200, 200))
            draw_text("Load", 10, 10, (0, 0, 0))
            if button(10, 10, 100, 30, "Home", (100, 100, 100), (255, 255, 255)) or mouse_just_pressed[1]:
                flags.clear()
                flags.append("home")
        """if flags[-1] == "settings": #--************
            screen.fill((200, 200, 200))
            draw_text("Settings", 10, 10, (0, 0, 0))
            if button(10, 10, 100, 30, "Home", (100, 100, 100), (255, 255, 255)) or mouse_just_pressed[1]:
                flags.clear()
                flags.append("home")"""
        
        if  "workspace" in flags:      #--************
            screen.fill(bg_color) 
            if button(per2pix(0), per2pix(0,"s_h"),per2pix(5),per2pix(3,"s_h"), "back", (204,34,244),(244,145,243)):
                square_clear()
                load_squares(home_rec_list)
                
                flags.clear()
                flags.append("home")

            #draw_text("Workspace", 5, 0, (0, 0, 0))
            if mouse_just_pressed[1]:
                square_clear()
                load_squares(home_rec_list)

                flags.clear()
                flags.append("home")

            load_connections()
            render_squares()

            keys=pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                camera_y += pan_speed
                print("keypress detected")
            if keys[pygame.K_UP]:
                camera_y -= pan_speed
                print("keypress detected")
            if keys[pygame.K_LEFT]:
                camera_x -= pan_speed
                print("keypress detected")
            if keys[pygame.K_RIGHT]:
                camera_x += pan_speed 
                print("keypress detected") 
            if mouse_scroll ==1 :
                zoom+=1*scroll_speed
                mouse_scroll=0
            if mouse_scroll ==-1 :
                zoom-=1*scroll_speed
                mouse_scroll=0
            
            #----------user tools 

            #---add node
            if button(per2pix(40),per2pix(95,"s_h"),per2pix(3),per2pix(3),"new node",(20,130,100),(255,255,255)):
                print(max(x for x in list(nodes_dic.keys()) if isinstance(x,int)))

                nodes_dic[max(x for x in list(nodes_dic.keys()) if isinstance(x,int))+1]={"type":"node","x":240,"y":0,"width":100,"hight":100,"color":(94,130,211),"text":"","text_color":(0,0,0),"defualt":"True"}
                square_clear()
                load_squares(nodes_dic)

            #---add lines
            if button(per2pix(50),per2pix(95,"s_h"),per2pix(3),per2pix(3),"new line",(60,100,140),(255,255,255)):
                selected_node=["","",""]
                current_tool="add line"
            if selected_node[1]!="" and selected_node[2] !="" and current_tool == "add line":

                if selected_node[1].name not in connection_dic:
                        connection_dic[selected_node[1].name]=[]
                if selected_node[2].name in connection_dic[selected_node[1].name] :
                    connection_dic[selected_node[1].name].remove(selected_node[2].name)
                connection_dic[selected_node[1].name].append(selected_node[2].name)
                selected_node=["","",""]
                current_tool=""
                bg_color=(190,190,180) 
            elif current_tool=="add line":
                bg_color=(60,70,100)
                draw_text("please select 2 nodes to add link",per2pix(40),per2pix(1,"s_h"),(255,255,255))

                #-----------------Remove line
            if button(per2pix(60),per2pix(95,"s_h"),per2pix(3),per2pix(3),"remove line",(140,100,60),(255,255,255)):
                selected_node=["","",""]
                current_tool="remove line"

            if selected_node[1]!="" and selected_node[2] !="" and current_tool == "remove line":
                    print(connection_dic)
                    print(f"1: {selected_node[1].name}  2: {selected_node[2].name}")
                    try :
                        connection_dic[selected_node[1].name].remove(selected_node[2].name)
                        if connection_dic[selected_node[1].name]==[]:
                            del connection_dic[selected_node[1].name]
                    except: # there is most likly a better way to do this
                        pass
                    try:
                        connection_dic[selected_node[2].name].remove(selected_node[1].name)
                        if connection_dic[selected_node[2].name]==[]:
                            del connection_dic[selected_node[2].name]
                    except:
                        pass
                    selected_node=["","",""]
                    current_tool=""
                    bg_color=(190,190,180) 
            elif current_tool=="remove line":
                        bg_color=(100,70,60)
                        draw_text("please select 2 nodes to remove link",per2pix(40),per2pix(1,"s_h"),(255,255,255))

                #----------edit text 
            if button(per2pix(70),per2pix(95,"s_h"),per2pix(3),per2pix(3),"text",(130,104,50),(255,255,255)):
                selected_node=["","",""]
                current_tool="edit_text"
                flags.append("typing")
                past_text=0

            if "typing" in flags and current_tool == "edit_text" and selected_node[1] != "":
                print(f"node text vaule: {nodes_dic[selected_node[1].name]["text"]}")
                if "no_select" not in flags : # prevents the selection of multiple nodes
                    flags.append("no_select")   
                #elif
                if past_text == 0 :   
                    past_text=nodes_dic[selected_node[1].name]["text"] # past text 
                    user_type=nodes_dic[selected_node[1].name]["text"] # current text 

                #load a instructions for user 
                draw_text("start typing!",per2pix(35),per2pix(3,"s_h"),(50,130,60),"sp1")
                draw_text("esc:cancel enter:finish",per2pix(35),per2pix(7,"s_h"),(50,130,60),"t3")

                bg_color=(180,180,100)
                nodes_dic[selected_node[1].name]["text"]=user_type
                squ={} 
                load_squares(nodes_dic)


            elif current_tool=="edit_text" and selected_node[1] == "" : # before a node is selected 
                print(f"selected node :  {selected_node}") 
                bg_color=(190,190,180) 
                draw_text("please select a node.",per2pix(35),per2pix(5,"s_h"),(50,130,60),"t3")

            if "fin_typing" in flags :
                print("finish_typing")
                user_type=""
                past_text=0   
                flags.remove("fin_typing")
                flags.remove("no_select")
                current_tool=""
                bg_color=(190,190,180) 
                square_clear()
                load_squares(nodes_dic)

            if "end_typing" in flags :
                print("end_typing")
                nodes_dic[selected_node[1].name]["text"]=past_text
                past_text=0
                flags.remove("end_typing")
                flags.remove("no_select")
                current_tool=""
                bg_color=(190,190,180) 
                square_clear()
                load_squares(nodes_dic)

                # mouse pan system
            if mouse_just_pressed[0]  and "clicked" not in  flags and "mouse_pan" not in flags:
                p_mouse_pos=pygame.mouse.get_pos()
                flags.append("mouse_pan")
                print("now using mouse pos")

                o_camera_x=camera_x
                o_camera_y=camera_y

            elif pygame.mouse.get_pressed()[0]  and "mouse_pan" in flags:
                c_mouse_pos= pygame.mouse.get_pos()
                #print(f" current:  {c_mouse_pos}  past:  {p_mouse_pos}" )

                camera_x = o_camera_x+ -1*(p_mouse_pos[0]-c_mouse_pos[0])
                camera_y = o_camera_y + -1*(p_mouse_pos[1]-c_mouse_pos[1])

                #print(f"x :  {-1(p_mouse_pos[0]-c_mouse_pos[0])} y: {-1(p_mouse_pos[1]-c_mouse_pos[1])} ")


            elif pygame.mouse.get_pressed()[0] ==False and "mouse_pan" in flags:
                flags.remove("mouse_pan")
                #print("removed mouse_pan from flags")

            elif pygame.mouse.get_pressed()[0] ==False and "clicked" in flags:
                flags.remove("clicked")
                #print("removed clicked from flags")

        #---------print zone 
        #print(f"seleted nodes: {selected_node}")
        #print(f" screen_x: {screen.get_width()}  screen_y: {screen.get_height()}")
        #print (flags)
        #print(f" pressing: {pygame.mouse.get_pressed()}  j_press: {pygame.mouse.get_just_pressed()}")
        frames+=1
        mouse_pos=pygame.mouse.get_pos() 
        mouse_click=f" pressing: {pygame.mouse.get_pressed()}  j_press: {pygame.mouse.get_just_pressed()}"
        #if sys.platform == "emscripten":
        #    platform.console.log(f" pressing: {pygame.mouse.get_pressed()}  j_press: {pygame.mouse.get_just_pressed()}")
        #else:
        #    print(f" pressing: {pygame.mouse.get_pressed()}  j_press: {pygame.mouse.get_just_pressed()}")

        clock.tick(frame_rate) 
        pygame.display.flip()
        await asyncio.sleep(0)
        
asyncio.run(main())