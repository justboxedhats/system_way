import pygame
import pickle
import os
from tkinter import *
from tkinter import filedialog
pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("System Way")
run_loop = True
frame_rate=30
# varrables
square_count=0
square_id_dic={}
squ={}
image_list={}
flags = ["home"]
bg_color=(0,0,0)
selected_node=["","",""]
current_tool=""
scroll={"images":0,"code":0}
basic_font = pygame.font.SysFont("Arial", 20)
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
nodes_dic = {1: {"type":"node","text": "get bread","x":100,"y":100, "width":100,"hight":100, "color": (255, 200, 200),"text_color":(0,0,0),"dragable":"True","sellectable":"True"},
             2: {"type":"node","text": "get jam and then get the knife that will be used to evenly spread the jam ontop of the bread/toast(yay)","x":300,"y":200, "width":100,"hight":100, "color": (200, 255, 200),"text_color":(0,0,0),"dragable":"True","sellectable":"True"},
             3: {"type":"node","text": "toast","x":500,"y":400, "width":100,"hight":100,  "color": (200, 200, 255),"text_color":(0,0,0),"dragable":"True","sellectable":"True"},
             4: {"type":"node","text": "image","x":600,"y":200, "width":100,"hight":100,  "color": (140, 200, 255),"text_color":(0,0,0),"dragable":"True","sellectable":"True"},
            } 

connection_dic = {1: [2], 2: [3]}
# fuctions

def open_exp():
    filepath = filedialog.askopenfilename()
    try:
        file=open(filepath, "r")
    except:
        print("error acored when attempting to retrive file")
        file=""
    if file == "":
        print("empty string")
        return "error"
    else:
        return file

def save_board(file_path):
    board_save={}
    board_save["settings"]=settings
    board_save["connection_dic"]= connection_dic
    board_save["nodes_dic"]=nodes_dic
    return save_board

def export_board ( ):
    save_board
    with open(file_path,'wb') as file:
    	pickle.dump(board_save,file)
		



def per2pix(percent,whole=screen.get_width()):
    return int( (percent / 100) * whole)

def button(x, y, width, height, text, color=(0, 0, 0), text_color=(255, 255, 255)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = basic_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)
    return text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]

def draw_line(x1, y1, x2, y2, color=(0, 0, 0), width=1):
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)

def draw_text(text, x, y, color=(0, 0, 0)):
    text_surface = basic_font.render(text, True, color)
    screen.blit(text_surface, (x, y))
def load_squares(dic={}):
    square_id_dic=dic
    for I in range(len(square_id_dic)):
        #type, x, y,width,hight,color . text,text_color. dragable. code. image
        squ[list(square_id_dic.keys())[I]]=squares(list(square_id_dic.keys())[I],square_id_dic[list(square_id_dic.keys())[I]]["type"],square_id_dic[list(square_id_dic.keys())[I]]["x"]
        , square_id_dic[list(square_id_dic.keys())[I]]["y"],square_id_dic[list(square_id_dic.keys())[I]]["width"],square_id_dic[list(square_id_dic.keys())[I]]["hight"],square_id_dic[list(square_id_dic.keys())[I]]["color"])

        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="visual":
            pass

        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="text":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]
        
        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="node":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]
            if "dragable" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].dragable=square_id_dic[list(square_id_dic.keys())[I]]["dragable"]
            if "sellectable" in square_id_dic[list(square_id_dic.keys())[I]] :
                squ[list(square_id_dic.keys())[I]].sellectable=square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]

            if "defualt" in square_id_dic[list(square_id_dic.keys())[I]] : # dragable,sellectable
                square_id_dic[list(square_id_dic.keys())[I]]["dragable"]="True"
                square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]="True"
                squ[list(square_id_dic.keys())[I]].dragable=square_id_dic[list(square_id_dic.keys())[I]]["dragable"]
                squ[list(square_id_dic.keys())[I]].sellectable=square_id_dic[list(square_id_dic.keys())[I]]["sellectable"]

        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="code_node":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]
        

            # dragable
            # Code

        if square_id_dic[list(square_id_dic.keys())[I]]["type"] =="img_node":
            squ[list(square_id_dic.keys())[I]].text=square_id_dic[list(square_id_dic.keys())[I]]["text"]
            squ[list(square_id_dic.keys())[I]].text_color=square_id_dic[list(square_id_dic.keys())[I]]["text_color"]

        
            # dragable
            # image
    #print(squ)

def render_squares ():
    for I in range(len(list(squ))):
        #print(squ[list(squ.keys())[I]].type)
        if squ[list(squ.keys())[I]].type == "visual":
            squ[list(squ.keys())[I]].draw()

        if squ[list(squ.keys())[I]].type == "text":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text, squ[list(squ.keys())[I]].x, squ[list(squ.keys())[I]].y, squ[list(squ.keys())[I]].text_color)

        if squ[list(squ.keys())[I]].type == "node":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text, squ[list(squ.keys())[I]].x+camera_x, squ[list(squ.keys())[I]].y+camera_y, squ[list(squ.keys())[I]].text_color)
            try:
                if squ[list(squ.keys())[I]].sellectable== "True":
                    squ[list(squ.keys())[I]].set_sellectable()      
            except:pass
            try :
                if squ[list(squ.keys())[I]].dragable == "True":
                    squ[list(squ.keys())[I]].set_dragable(list(squ.keys())[I])
            except:pass

        if squ[list(squ.keys())[I]].type == "code_node":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text,squ[list(squ.keys())[I]].x+camera_x,squ[list(squ.keys())[I]].y+camera_y, squ[list(squ.keys())[I]].text_color)
            squ[list(squ.keys())[I]].add_code()

        if squ[list(squ.keys())[I]].type == "im_node":
            squ[list(squ.keys())[I]].draw()
            squ[list(squ.keys())[I]].draw_text(squ[list(squ.keys())[I]].text,squ[list(squ.keys())[I]].x+camera_x,squ[list(squ.keys())[I]].y+camera_y-per2pix(.7,squ[list(squ.keys())[I]].height),squ[list(squ.keys())[I]].text_color)
            #self.add_image()
            #self.dragrable()

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

            draw_line(start_center_x, start_center_y, end_center_x, end_center_y, color=(0, 0, 0), width=2)
#type, x, y,width,hight,color . text,text_color. dragable. code. image
class squares:
    def __init__(self,name,type="visual", x=100, y=100, width=20, height=20, color=(0, 0, 0),text="", text_color=(0, 0, 0), font_size=20, image="", code=""):
        global square_count
        square_count+=1
        self.name=name
        self.x = x
        self.y = y
        self.image= image
        self.code=code
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.type = type
        
    def __delete__(self, instance):
        square_count -=1
        print("deleted square")
    def draw(self):
        global selected_node

        if  "node" in self.type : 
            self.m_rect=(self.x+camera_x, self.y+camera_y, self.width*zoom, self.height*zoom)
            pygame.draw.rect(screen,self.color, self.m_rect,border_radius=int(self.width/30))
            self.rect=pygame.Rect((self.x, self.y, self.width, self.height)) 
            if self in selected_node :
                pygame.draw.rect(screen, (200, 200, 200), self.m_rect, width=4)
                #draws the pale outline
            else:
                pygame.draw.rect(screen, (50, 80, 90), self.m_rect, width=4)
                #draws the basic outline
        else:
            #print(f" color: {self.color} , x: {self.x} , y: {self.y} , width: {self.width} , x: {self.height}")
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=int(self.width/30))
            self.rect=pygame.Rect((self.x, self.y, self.width, self.height))

    def set_dragable(self,name):
        global selected_node
        #print("started draging")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x,mouse_y) and pygame.mouse.get_just_pressed()[0] and selected_node[0]=="":
            selected_node[0]=self
        if self == selected_node[0] and pygame.mouse.get_pressed()[0]:
            self.x = mouse_x - self.width / 2
            self.y = mouse_y - self.height / 2
            nodes_dic[name]["x"]=self.x
            nodes_dic[name]["y"]=self.y
            
        elif self == selected_node[0] and pygame.mouse.get_pressed()[0] !=True: 
            #selected_node[1]=selected_node[0]
            selected_node[0]=""
        
    def set_sellectable(self) :
        global selected_node
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x,mouse_y) and pygame.mouse.get_just_pressed()[0] and self not in selected_node:        
            selected_node.insert(1,self)
            del selected_node[3]
        elif self.rect.collidepoint(mouse_x,mouse_y) and pygame.mouse.get_just_pressed()[0] and self in selected_node:
            print("attempted to remove select")
            #print()
            del selected_node[self]

    def re_resize (self): #needs work, no fundimential
        pygame.rect
        self.width=self.rect[0]
        self.hight=self.rect[1]

    def draw_text(self, text, x, y, color=(0, 0, 0)):
        if self.text != "":
            text_surface = basic_font.render(text, True, color,None,int(self.width))
            screen.blit(text_surface, (x, y))
            
    def add_code (self):
        if self.code == "":
            print("There was no code to use")
        else:
            #rect=
            #pygame.draw.rect()
            draw_text(self.code,self.x+text_offset_x, self.y+text_offset_y,self.text_color)

    def add_image(self):
        if self.image == "":
            print("There was no image to pull")
        else:
            print(self.image)
            screen.blit(self.image,(self.x,self.y))

#"image_bg":{"type":"","x":,"y","width","hight","color","text","text_color"}
 #type, x, y,width,hight,color . text,text_color. dragable. code. image
home_rec_list={
    "tital":{"type":"text","x":per2pix(2),"y":10,"width":per2pix(50),"hight":70,"color":(170,190,160,100),"text":"System Way","text_color":(200, 140, 160,120) },
    "ver_bg":{"type":"text","x":10,"y":80,"width":100,"hight":30,"color":(160, 180, 150),"text":"ver 1.0 (beta)","text_color":(220, 160, 180)},
    "option_bg":{"type":"visual","x":0,"y":160,"width":140,"hight":400,"color":(150, 170, 140)},
    "image_bg":{"type":"visual","x":per2pix(55),"y":per2pix(2,screen.get_height()),"width":per2pix(40),"hight":per2pix(90,screen.get_height()),"color":(200, 220, 190)}
    }
load_squares(home_rec_list)
render_squares()

nodes_dic["tool_bar_bg"]={"type":"visual", "x":per2pix(35),"y":per2pix(94,screen.get_height()),"width":per2pix(50),"hight":per2pix(7,screen.get_height()),"color":(120,200,180)}

while run_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_loop = False
    #print(square_count)
    if flags[-1] == "home": #--************
        screen.fill((215, 225, 200))

        render_squares()

        if button(10, 170, 120, 90, "load", (103, 100, 100), (255, 255, 255)):

            file_path = open_exp() #'text_files/list_recall.pkl'
            if file_path == "error":  
                print("error detected")
            else:
                file_path = file_path.name
                print (file_path)
            #retreaving board data 
            if os.path.exists(file_path):
                print("detected save file")
                with open( file_path, "rb") as file:
                    board_save=pickle.load(file)
                    print(board_save)
                    #assining dictionaries 
                    nodes_dic=board_save["nodes_dic"]
                    connection_dic=board_save["connection_dic"]
                    settings=board_save["settings"]
                    pan_speed= settings["pan_speed"]
                    tool_bg_x= settings["tool_bg_x"]

                flags.clear()
                flags.append("workspace")
        if button(10, 300, 120, 90, "Workspace", (140, 100, 100), (255, 255, 255)):
            print(square_count)
            flags.clear()
            bg_color=(100,100,100)
            flags.append("workspace")
            square_clear()
            load_squares(nodes_dic)

        if button(10, 450, 120, 40, "Settings", (150, 100, 100), (255, 255, 255)):
            flags.clear()
            flags.append("settings")
            
        if button(10, 500, 120, 40, "quit", (160, 100, 100), (255, 255, 255)):
                    run_loop = False
        

    if flags[-1] == "load": #--************
        screen.fill((200, 200, 200))
        draw_text("Load", 10, 10, (0, 0, 0))
        if button(10, 10, 100, 30, "Home", (100, 100, 100), (255, 255, 255)) or pygame.mouse.get_just_pressed()[1]:
            flags.clear()
            flags.append("home")
    if flags[-1] == "settings": #--************
        screen.fill((200, 200, 200))
        draw_text("Settings", 10, 10, (0, 0, 0))
        if button(10, 10, 100, 30, "Home", (100, 100, 100), (255, 255, 255)) or pygame.mouse.get_just_pressed()[1]:
            flags.clear()
            flags.append("home")
    
    if flags[-1] == "workspace":      #--************
        screen.fill(bg_color)
        draw_text("Workspace", 5, 0, (0, 0, 0))
        if pygame.mouse.get_just_pressed()[1]:
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
        #if  mouse scroll up :
        # zoom+=1
        #if mouse scrool ip :
        # zoom-=1

        #----------user tools 

        #add node
        if button(per2pix(35),per2pix(95,screen.get_height()),per2pix(3),per2pix(3),"new node",(20,130,100),(255,255,255)):
            print(max(x for x in list(nodes_dic.keys()) if isinstance(x,int)))

            nodes_dic[max(x for x in list(nodes_dic.keys()) if isinstance(x,int))+1]={"type":"node","x":240,"y":0,"width":100,"hight":100,"color":(94,130,211),"text":"","text_color":(0,0,0),"defualt":"True"}
            square_clear()
            load_squares(nodes_dic)
        #add lines
        if button(per2pix(41),per2pix(95,screen.get_height()),per2pix(3),per2pix(3),"new line",(60,100,140),(255,255,255)):
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
            bg_color=(100,100,100)
        elif current_tool=="add line":
            bg_color=(60,70,100)
            draw_text("please select 2 nodes",per2pix(40),per2pix(1,screen.get_height()),(255,255,255))

        if button(per2pix(48),per2pix(95,screen.get_height()),per2pix(3),per2pix(3),"remove line",(140,100,60),(255,255,255)):
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
                bg_color=(100,100,100)
        elif current_tool=="remove line":
                    bg_color=(100,70,60)
                    draw_text("please select 2 nodes",per2pix(40),per2pix(1,screen.get_height()),(255,255,255))
            
            
                

        #add text
        if button(per2pix(54),per2pix(95,screen.get_height()),per2pix(3),per2pix(3),"text",(130,104,50),(255,255,255)):
            pass
        #add images 
        if button(per2pix(61),per2pix(95,screen.get_height()),per2pix(3),per2pix(3),"image",(190,210,40),(255,255,255)):
            pass

        if "code" in flags:
            if button(10, 20, 70, 20, "images", (0, 0, 0), (255, 255, 255)):
                flags.remove("code")
                flags.insert(0, "images")
                print("images button clicked, changed flags")
            if button(80, 20, 180, 20, "Code", (110, 180, 170), (255, 255, 255)):
                flags.remove("code")
                print("Code button clicked, changed flags")

            if "image_bg" in list(nodes_dic.keys()):
                nodes_dic.pop("image_bg")
                nodes_dic["code_bg"]={"type":"visual","x":10,"y":40,"width":tool_bg_x,"hight":600,"color": (10, 18, 12)}
                print("added code bg 1 ")
                square_clear()
                load_squares(nodes_dic)
            else:
                nodes_dic["code_bg"]={"type":"visual","x":10,"y":40,"width":tool_bg_x,"hight":600,"color": (180, 190, 210)}
                print("added code bg 2 ")
                square_clear()
                load_squares(nodes_dic)   
                


        elif "images" in flags:
            
                #load images

            if image_list != "":
                for I in range(len(image_list)):
                    #image_rect=pygame.rect(20,250*I, 100,200 )
                    screen.blits(image_list[I], (20,250*I+scroll["images"]))                   
            else:
                draw_text("no images in board",20,per2pix(95,screen.get_height()),(190,160,150))
                # loading ui buttions

            if button(10, 20, 180, 20, "images", (110, 180, 170), (255, 255, 255)):
                flags.remove("images")
                print("images button clicked, changed flags")
            if button(190, 20, 70, 20, "Code", (0, 0, 0), (255, 255, 255)):
                flags.remove("images")
                flags.insert(0, "code")
                print("Code button clicked, changed flags")      
            if button(10,per2pix(95,screen.get_height()), 200,per2pix(3), "import",(90,160,150),(0,0,0)):
                file=open_exp()
                image_file=pygame.image.load(file.name).convert_alpha
                print(f" file: {file}  and image : {image_file}")
                image_list[len(image_list)]= image_file
                print(f"image list: {image_list}")
                """if selected_node != "":
                    nodes_dic[selected_node][type]= "image"          
                    print(f"added image to node : {selected_node}")"""
            if "code_bg" in list(nodes_dic.keys()):
                nodes_dic.pop("code_bg")
                nodes_dic["image_bg"]={"type":"visual","x":10,"y":40,"width":tool_bg_x,"hight":600,"color": (180, 190, 210)}
                square_clear()
                load_squares(nodes_dic)
                print("added image bg 1 ")
            else:
                print("added image bg 2 ")
                nodes_dic["image_bg"]={"type":"visual","x":10,"y":40,"width":tool_bg_x,"hight":600,"color": (180, 190, 210)}
                square_clear()
                load_squares(nodes_dic)
        
        else:
            if button(10, 20, tool_bg_x/2, 20, "images", (0, 0, 0), (255, 255, 255)):
                flags.insert(0,"images")
                print("images button clicked, changed flags")
            if button(10+tool_bg_x/2, 20, tool_bg_x/2, 20, "Code", (0, 0, 0), (255, 255, 255)):
                flags.insert(0, "code")
                print("Code button clicked, changed flags")
            if "code_bg" in list(nodes_dic.keys()):
                nodes_dic.pop("code_bg")
                square_clear()
                load_squares(nodes_dic)
            elif "image_bg" in list(nodes_dic.keys()) :
                nodes_dic.pop("image_bg")
                square_clear()
                load_squares(nodes_dic)

        if button(per2pix(90),10,50,3,"export",(100,100,100),(225,225,225)):
            print("pressed the import buttion ")
            filepath = filedialog.askdirectory()
            print(filepath)     
            save_board(filepath)
        if button(per2pix(80),10,50,3,"save",(100,100,100),(225,225,225)):
            pass
            #if save_filepath
            #board_save()
        # Checks for mouse drag or click
    #print(f"seleted nodes: {selected_node}")

            
            


    clock.tick(frame_rate)
    pygame.display.flip()
