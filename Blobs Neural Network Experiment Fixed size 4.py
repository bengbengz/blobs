from tkinter import *
from random import *
from time import *
from math import *


class Game():
    def __init__(self):
        self.root = Tk()
        self.r = Canvas(self.root, width=1350, height=800, bg='#adefff')
        self.r.pack()
        self.stats = False
        self.time = 10
        self.name_list = {}
        self.i = 1
        self.legend = 0
        self.life_forms = {}
        self.food()

    def food(self):
        x = randint(50, 1300)
        y = randint(50, 750)
        if (x, y) not in self.life_forms:   
            self.life_forms[(x, y, 'brown')] = self.r.create_oval(x-2, y-2, x+2, y+2,
                            outline = "#099c0e", fill = "#099c0e", width = 5)
        self.r.after(3*len(self.name_list)*self.time, self.food)

class Character():
    def __init__(self, game, name, X, Y, genes, energy, speed, digest):
        self.game = game
        self.name = name
        self.X = X
        self.Y = Y
        self.age = 0
        self.ocolour = "#6969ff"
        self.colour = self.colour_gene(digest[0])
        self.incubation = 20
        self.genes = genes
        self.digest = digest
        self.srnd = []
        self.srnd_b = []
        self.srnd_blob = []
        self.mass = 1
        self.energy = energy
        self.direction = randint(0, 1000)/1000*pi*2
        self.repro_reco = 0.1
        self.time_to_fertile = 0
        self.prv_dist_to_tgt = 200
        self.xd = sin(self.direction)
        self.yd = cos(self.direction+pi)
        self.size = 0.5
        self.prv_tgt = ()
        self.fd_count = 0
        self.tt = 1
        self.max_size = 1
        self.speed = speed
        self.tgt = (500, 500)
        self.Fr, self.Ba, self.L, self.R = 0, 0, 0, 0
        self.sprite()
        self.egg = self.game.r.create_oval(self.X-5, self.Y-5,
                                self.X+5, self.Y+5,
                        outline = self.colour, fill = "#fff3d4", width = 0.5)
        self.alive = True        
        self.ai()
        
        
    def sprite(self):
        x = self.X
        y = self.Y
        eye_space = 0.7
        xd = self.xd
        yd = self.yd
        
        if self.srnd != []:
            self.x_dist = self.tgt[0] - self.X
            self.y_dist = self.Y - self.tgt[1]         
            self.tgt_dist = sqrt(self.x_dist**2 + self.y_dist**2)

        #body
        self.a = self.game.r.create_oval(x-(10*self.size), y-(10*self.size),
                                    x+(10*self.size), y+(10*self.size),
                            outline = self.colour, fill = self.colour, width = 5)
        #mouth
        self.x_mouth = x+(self.size*10*sin(self.direction))
        self.y_mouth = y+(self.size*10*-cos(self.direction))


        #eyes
        xd_left_eye = sin(self.direction + eye_space)
        xd_right_eye = sin(self.direction - eye_space)
        yd_left_eye = -cos(self.direction + eye_space)
        yd_right_eye = -cos(self.direction - eye_space)
        self.b = self.game.r.create_oval(x+((7*self.size)*xd_left_eye)-2, y+((7*self.size)*yd_left_eye)-2,
                                    x+((7*self.size)*xd_left_eye)+2, y+((7*self.size)*yd_left_eye)+2,
                                    outline = "black", fill = "black", width = 0 )
        self.c = self.game.r.create_oval(x+((7*self.size)*xd_right_eye)-2, y+((7*self.size)*yd_right_eye)-2,
                                    x+((7*self.size)*xd_right_eye)+2, y+((7*self.size)*yd_right_eye)+2,
                                    outline = "black", fill = "black", width = 0 )

        #stats
        #self.d = self.game.r.create_text(x, y+(10*self.size)+10, text=str(tuple(self.genes)))
        self.x_ass = x-(self.size*22*sin(self.direction))
        self.y_ass = y-(self.size*22*-cos(self.direction))
        #self.d = self.game.r.create_oval(self.x_ass-2, self.y_ass-2,
                                    #self.x_ass+2, self.y_ass+2,
                                    #outline = "black", fill = "black", width = 0 )
        #self.d = None
        
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.i = None
        self.j = None
        if game.stats:
            self.e = self.game.r.create_text(x, y+(10*self.size)+7, text=f"{round(self.Fr, 3), round(self.Ba, 3), round(self.L, 3), round(self.R, 3)}", font=('Arial', 10))
            self.f = self.game.r.create_text(x, y-(10*self.size)-10, text=str(self.name), font=('Arial', 10))
            self.h = self.game.r.create_line(x-10, y-(10*self.size)-5, x+self.energy//200 - 10, y-(10*self.size)-5, fill='green', width=3)
            self.g = self.game.r.create_line(self.x_mouth, self.y_mouth, self.x_mouth + 50*sin(self.direction), self.y_mouth - 50*cos(self.direction), width=2, fill='black')
            
            if self.srnd != []:
                self.d = self.game.r.create_line(self.x_mouth, self.y_mouth, self.tgt[0], self.tgt[1], width=2, fill='red')

            if self.srnd_blob != []:
                self.i = self.game.r.create_line(self.X, self.Y, self.tgt_blob_x, self.tgt_blob_y, width=2, fill='green')

            if self.srnd_b != []:
                self.j = self.game.r.create_line(self.x_mouth, self.y_mouth, self.tgt_b[0], self.tgt_b[1], width=2, fill='red')
                

    def delete_prev(self):
        for obj in [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.j]:
            self.game.r.delete(obj)

    def move_frame(self, amt, direction):
        self.collision_check()
        if self.X < 50 or self.X > 1300 or self.Y < 50 or self.Y > 750:
            pass
        self.delete_prev()
        xd = sin(self.direction)
        yd = cos(self.direction)
        if direction == 'forward':
            self.X += xd*amt
            self.Y -= yd*amt
            if self.X > 1310:
                self.X = 50
            if self.X < 40:
                self.X = 1300
            if self.Y > 760:
                self.Y = 50
            if self.Y < 40:
                self.Y = 750
        elif direction == 'backward':
            self.X -= xd*amt
            self.Y += yd*amt
            if self.X > 1310:
                self.X = 50
            if self.X < 40:
                self.X = 1300
            if self.Y > 760:
                self.Y = 50
            if self.Y < 40:
                self.Y = 750
        self.sprite()

    def free_move(self, amt, direction):
        self.delete_prev()
        xd = sin(direction)
        yd = cos(direction+pi)
        self.X += xd*amt
        self.Y -= yd*amt
        self.sprite()

    def rotate(self, speed, direction):
        if direction == 'left':
            self.delete_prev()
            self.direction -= speed
            self.sprite()
        elif direction == 'right':
            self.delete_prev()
            self.direction += speed
            self.sprite()
            
        if self.direction > 2*pi:
            self.direction = 0
        elif self.direction < 0:
            self.direction = 2*pi

    def eat(self):
        tgt_fud = (int(self.x_mouth), int(self.y_mouth))
        mouth_size = 9 + 4*int(self.size)
        for i in range(mouth_size):
            for j in range(mouth_size):
                temp_pix_g = (int(tgt_fud[0] + i - (mouth_size-1)/2), int(tgt_fud[1] + j - (mouth_size-1)/2), 'green')
                temp_pix_b = (int(tgt_fud[0] + i - (mouth_size-1)/2), int(tgt_fud[1] + j - (mouth_size-1)/2), 'brown')
                if temp_pix_g in self.game.life_forms:
                    self.game.r.delete(self.game.life_forms[temp_pix_g])
                    self.fd_count += 1
                    if self.size < self.max_size:
                        self.size += 0.1
                        self.mass = self.size**3
                    self.energy += 6*(self.digest[0]-20)
                    del self.game.life_forms[temp_pix_g]
                    return
                if temp_pix_b in self.game.life_forms:
                    self.game.r.delete(self.game.life_forms[temp_pix_b])
                    self.fd_count += 1
                    if self.size < self.max_size:
                        self.size += 0.1
                        self.mass = self.size**3
                    self.energy += 6*(self.digest[1]-20)
                    del self.game.life_forms[temp_pix_b]
                    return
                
    def eat2(self, tgt, t):
        if t == "green":
            self.game.r.delete(self.game.life_forms[tgt])
            self.fd_count += 1
            if self.size < self.max_size:
                self.size += 0.1
                self.mass = self.size**3
                self.energy += 10*(self.digest[0]-10)
            del self.game.life_forms[tgt]
        if t == "brown":
            self.game.r.delete(self.game.life_forms[tgt])
            self.fd_count += 1
            if self.size < self.max_size:
                self.size += 0.1
                self.mass = self.size**3
                self.energy += 10*(self.digest[1]-10)
            del self.game.life_forms[tgt]        
        
    def sense(self):
        self.vision = 100
        temp = []
        nearest = ()
        lowest_dist = self.vision
        for i in self.game.life_forms:
            tgt_x = i[0]
            tgt_y = i[1]
            if (tgt_x > self.X - self.vision and tgt_x < self.X + self.vision) and\
                (tgt_y > self.Y - self.vision and tgt_y < self.Y + self.vision) and i[2] == 'green':
                dtt = sqrt((self.X-tgt_x)**2 + (self.Y-tgt_y)**2)
                if dtt <= self.vision:
                    temp.append(i)
                    if dtt < lowest_dist:
                        lowest_dist = dtt
                        nearest = i
        return (temp, nearest)

    def sense_b(self):
        self.vision = 100
        temp = []
        nearest = ()
        lowest_dist = self.vision
        for i in self.game.life_forms:
            tgt_x = i[0]
            tgt_y = i[1]
            if (tgt_x > self.X - self.vision and tgt_x < self.X + self.vision) and\
                (tgt_y > self.Y - self.vision and tgt_y < self.Y + self.vision) and i[2] == 'brown':
                dtt = sqrt((self.X-tgt_x)**2 + (self.Y-tgt_y)**2)
                if dtt <= self.vision:
                    temp.append(i)
                    if dtt < lowest_dist:
                        lowest_dist = dtt
                        nearest = i
        return (temp, nearest)

    def sense_blob(self):
        self.vision = 100
        temp = []
        nearest = ()
        lowest_dist = self.vision
        for i in game.name_list:
            tgt_x = game.name_list[i].X
            tgt_y = game.name_list[i].Y
            if (tgt_x > self.X - self.vision and tgt_x < self.X + self.vision) and\
                (tgt_y > self.Y - self.vision and tgt_y < self.Y + self.vision) and (tgt_x, tgt_y) != (self.X, self.Y):
                dtt = sqrt((self.X-tgt_x)**2 + (self.Y-tgt_y)**2)
                if dtt <= self.vision:
                    temp.append(i)
                    if dtt < lowest_dist:
                        lowest_dist = dtt
                        nearest = i
                        #print(temp, nearest)
        return (temp, nearest)

    def collision_check(self):
        border = 50
        temp = []
        nearest = ()
        for i in game.name_list:
            #print(str(self.name) + ': ' + str(i))
            if game.name_list[i].name == self.name:
                continue
            else:
                tgt_x = game.name_list[i].X
                tgt_y = game.name_list[i].Y
                #print(tgt_x, tgt_y)
                if (tgt_x > self.X - border and tgt_x < self.X + border) and\
                    (tgt_y > self.Y - border and tgt_y < self.Y + border):
                    dtt = sqrt((self.X-tgt_x)**2 + (self.Y-tgt_y)**2)
                    min_dist = 11*self.size + 11*game.name_list[i].size
                    if dtt <= min_dist and dtt != 0:
                        opp_mass = game.name_list[i].mass
                        tot_mass = self.mass + opp_mass
                        angle = asin((self.X-tgt_x)/dtt)
                        self.free_move(6*(opp_mass/tot_mass), angle)
                        self.energy -= opp_mass
                        game.name_list[i].energy -= self.mass

    def decompose(self):
        for i in range(3*int(self.mass) + 1):
            bd = 10*self.size
            x = randint(int(self.X-bd), int(self.X+bd))
            y = randint(int(self.Y-bd), int(self.Y+bd))
            if (x, y, 'green') not in self.game.life_forms and (x, y, 'brown') not in self.game.life_forms:   
                self.game.life_forms[(x, y, 'brown')] = self.game.r.create_oval(x-2, y-2, x+2, y+2,
                                outline = "#805700", fill = "#805700", width = 5)

    def die(self):
        score = self.fd_count
        if score > game.legend:
            game.legend = score
            self.orbit()
            
        self.alive = False
        self.decompose()
        del game.name_list[int(self.name)]
        del self

    def colour_gene(self, colour):
        self.order = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8',
                      9:'9', 10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f'}
        for j in self.order:
            if self.order[j] == self.ocolour[1]:
                self.first = j
                self.offspring_first = self.first
            if self.order[j] == self.ocolour[2]:
                self.second = j
                self.offspring_second = self.second
        for i in range(abs(colour)):
            if self.offspring_second >= 15:
                self.offspring_second = 0
                self.offspring_first += 1
                if self.offspring_first > 15:
                    self.offspring_first = 15
            else:
                self.offspring_second += 1
        #print(f'{colour} and colour is "#{self.order[self.offspring_first]}{self.order[self.offspring_second]}{self.order[self.offspring_first]}{self.order[self.offspring_second]}ff"')
        return f"#{self.order[self.offspring_first]}{self.order[self.offspring_second]}{self.order[self.offspring_first]}{self.order[self.offspring_second]}ff"

    def reproduce(self):
        x = self.x_ass
        y = self.y_ass
        offspring_genes = {}
        offspring_digest = [self.digest[0] + randint(0, 10)-5, self.digest[1] + randint(0, 10)-5, 100]
        if offspring_digest[0] < 0:
            offspring_digest[0] = 0
        if offspring_digest[1] < 0:
            offspring_digest[1] = 0
        if offspring_digest[0] > 100:
            offspring_digest[0] = 100
        if offspring_digest[1] > 100:
            offspring_digest[1] = 100
        if offspring_digest[0] + offspring_digest[1] > 100:
            offspring_digest[1] = 100 - offspring_digest[0]
        offspring_digest[2] -= (offspring_digest[0] + offspring_digest[1])
        #print(offspring_digest)
        self.energy -= 1000
        for i in self.genes:
            offspring_genes[i] = round((self.genes[i] + (randint(0, 4)-2)/1000), 3)
        self.game.name_list[game.i] = Character(game, str(game.i),
                                    x, y, offspring_genes, 500, self.speed + (randint(0, 100)-50)/100, offspring_digest)
        game.i += 1

    def sigmoid(self, x):
        return 1/(1 + exp(-x))

    def orbit(self):
        if self.fd_count > 10:
            print(f"{self.name}:")
            print(f"Scored {self.fd_count}")
            print(f"Genes: {self.genes}")

    def ai(self):
        if self.age > self.incubation:
            self.game.r.delete(self.egg)

            (self.srnd, self.tgt) = self.sense()
            (self.srnd_b, self.tgt_b) = self.sense_b()
            (self.srnd_blob, self.tgt_blob) = self.sense_blob()

            genes = self.genes
            drt = self.direction
                
            self.x_dist = 0
            self.y_dist = 0
            self.tgt_dist = 0
            tgt_alpha = 0

            if self.srnd != []:
                self.x_dist = self.tgt[0] - self.x_mouth
                self.y_dist = self.y_mouth - self.tgt[1]
                self.tgt_dist = sqrt(self.x_dist**2 + self.y_dist**2)
                if self.tgt_dist < 5*self.size:
                    self.eat2(self.tgt, "green")
                tgt_alpha = asin(abs(self.x_dist/self.tgt_dist))
                if self.x_dist >= 0:
                    if self.y_dist < 0:
                        tgt_alpha = pi - tgt_alpha
                else:
                    if self.y_dist < 0:
                        tgt_alpha += pi
                    else:
                        tgt_alpha = 2*pi - tgt_alpha
                
            tgt_alpha_r = 0
            tgt_alpha_l = 0
            tgt_alpha -= drt

            if tgt_alpha > pi:
                tgt_alpha -= 2*pi
                
            if tgt_alpha < 0:
                tgt_alpha_l = abs(tgt_alpha)
            else:
                tgt_alpha_r = tgt_alpha

            if self.tgt != self.prv_tgt:
                self.tt += 1
                self.prv_tgt = self.tgt

            #print(int(tgt_alpha_l*360/(2*pi)), int(tgt_alpha_r*360/(2*pi)))
            #print(int(tgt_alpha*360/(2*pi)))

                
            self.x_b_dist = 0
            self.y_b_dist = 0
            self.tgt_b_dist = 0
            tgt_b_alpha = 0

            if self.srnd_b != []:
                self.x_b_dist = self.tgt_b[0] - self.x_mouth
                self.y_b_dist = self.y_mouth - self.tgt_b[1]         
                self.tgt_b_dist = sqrt(self.x_b_dist**2 + self.y_b_dist**2)
                if self.tgt_b_dist < 5*self.size:
                    self.eat2(self.tgt_b, "brown")
                tgt_b_alpha = asin(abs(self.x_b_dist)/self.tgt_b_dist)
                if self.x_b_dist >= 0:   
                    if self.y_b_dist < 0:
                        tgt_b_alpha = pi - tgt_b_alpha
                else:
                    if self.y_b_dist < 0:
                        tgt_b_alpha += pi
                    else:
                        tgt_b_alpha = 2*pi - tgt_alpha

            tgt_b_alpha -= drt
            tgt_b_alpha_r = 0
            tgt_b_alpha_l = 0
            
            if tgt_b_alpha > pi:
                tgt_b_alpha -= 2*pi
                
            if tgt_b_alpha < 0:
                tgt_b_alpha_l = abs(tgt_b_alpha)
            else:
                tgt_b_alpha_r = tgt_b_alpha
                
            #print(int(self.tgt_b_dist), int(abs(tgt_b_alpha*360/(2*pi))), int(tgt_b_alpha_r*360/(2*pi)),)

            self.tgt_blob_x = 0
            self.tgt_blob_y = 0
            self.tgt_blob_x_dist = 0
            self.tgt_blob_y_dist = 0
            self.tgt_blob_dist = 0
            tgt_blob_alpha = 0
            
            if self.srnd_blob != []:
                self.tgt_blob_x = game.name_list[self.tgt_blob].X
                self.tgt_blob_y = game.name_list[self.tgt_blob].Y
                self.tgt_blob_x_dist = self.tgt_blob_x - self.X
                self.tgt_blob_y_dist = self.Y - self.tgt_blob_y
                self.tgt_blob_dist = sqrt(self.tgt_blob_x_dist**2 + self.tgt_blob_y_dist**2)
                if self.tgt_blob_dist == 0:
                    self.tgt_blob_dist = 1
                if self.tgt_blob_x_dist >= 0:
                    tgt_blob_alpha = asin(abs(self.tgt_blob_x_dist)/self.tgt_blob_dist)
                    if self.tgt_blob_y_dist < 0:
                        tgt_blob_alpha = pi - tgt_blob_alpha
                else:
                    tgt_blob_alpha = asin(abs(self.tgt_blob_x_dist)/self.tgt_blob_dist)
                    if self.tgt_blob_y_dist < 0:
                        tgt_blob_alpha += pi
                    else:
                        tgt_blob_alpha = 2*pi - tgt_blob_alpha

            tgt_blob_alpha -= drt
            tgt_blob_alpha_r = 0
            tgt_blob_alpha_l = 0

            if tgt_blob_alpha > pi:
                tgt_blob_alpha -= 2*pi
                
            if tgt_blob_alpha < 0:
                tgt_blob_alpha_l = abs(tgt_blob_alpha)
            else:
                tgt_blob_alpha_r = tgt_blob_alpha

            
            if not self.alive:
                self.delete_prev()
                return
                
            if self.energy <= 0:
                self.die()
            
            if self.size > 0.8*self.max_size and self.time_to_fertile <= 0 and self.energy > 2000:
                self.time_to_fertile = self.repro_reco*1000
                self.reproduce()
            self.time_to_fertile -= 1
            
            size = self.size
            
            A = self.sigmoid(genes['A1']*self.tgt_dist + genes['A2']*tgt_alpha_r + genes['A3']*tgt_alpha_l + \
                             genes['A4']*self.tgt_b_dist + genes['A5']*tgt_b_alpha_r + genes['A6']*tgt_b_alpha_l + \
                             genes['A7']*self.tgt_blob_dist + genes['A8']*tgt_blob_alpha_r + genes['A9']*tgt_blob_alpha_l)
            B = self.sigmoid(genes['B1']*self.tgt_dist + genes['B2']*tgt_alpha_r + genes['B3']*tgt_alpha_l + \
                             genes['B4']*self.tgt_b_dist + genes['B5']*tgt_b_alpha_r + genes['B6']*tgt_b_alpha_l + \
                             genes['B7']*self.tgt_blob_dist + genes['B8']*tgt_blob_alpha_r + genes['B9']*tgt_blob_alpha_l)
            C = self.sigmoid(genes['C1']*self.tgt_dist + genes['C2']*tgt_alpha_r + genes['C3']*tgt_alpha_l + \
                             genes['C4']*self.tgt_b_dist + genes['C5']*tgt_b_alpha_r + genes['C6']*tgt_b_alpha_l + \
                             genes['C7']*self.tgt_blob_dist + genes['C8']*tgt_blob_alpha_r + genes['C9']*tgt_blob_alpha_l)


            D = self.sigmoid(genes['D1']*A + genes['D2']*B + genes['D3']*C + genes['D'])
            E = self.sigmoid(genes['E1']*A + genes['E2']*B + genes['E3']*C + genes['E'])
            F = self.sigmoid(genes['F1']*A + genes['F2']*B + genes['F3']*C + genes['F'])

            Fr = self.sigmoid(genes['Fr1']*D + genes['Fr2']*E + genes['Fr3']*F + genes['Fr'])
            Ba = self.sigmoid(genes['Ba1']*D + genes['Ba2']*E + genes['Ba3']*F + genes['Ba'])
            L = self.sigmoid(genes['L1']*D + genes['L2']*E + genes['L3']*F + genes['L'])
            R = self.sigmoid(genes['R1']*D + genes['R2']*E + genes['R3']*F + genes['R'])
            N = self.sigmoid(genes['N1']*D + genes['N2']*E + genes['N3']*F + genes['N'])

            #print(f"{Fr, Ba, L, R}")

            self.Fr, self.Ba, self.L, self.R, self.N = Fr, Ba, L, R, N

            if self.age > 10000:
                self.speed *= 0.999
            speed = self.speed
            if self.energy <= 100:
                speed *= self.energy/100

            if Fr > Ba and Fr > L and Fr > R and Fr > N:
                self.energy -= self.speed/10
                self.move_frame(speed, 'forward')    
            elif Ba > Fr and Ba > L and Ba > R and Ba > N:
                self.energy -= self.speed/8
                self.move_frame(speed, 'backward')
            elif L > Fr and L > Ba and L > R and L > N:
                self.energy -= self.speed/12
                self.rotate(speed/30, 'left')
                #self.move_frame(speed, 'forward')
            elif R > Fr and R > Ba and R > L and R > N:
                self.energy -= self.speed/12
                self.rotate(speed/30, 'right')
                #self.move_frame(speed, 'forward')
        self.energy -= 0.1            
        self.age += 1        
        self.game.r.after(2*self.game.time, self.ai)


game=Game()

def fd():
    for i in range(200):
        x = randint(50, 1300)
        y = randint(50, 750)
        if (x, y) not in game.life_forms:
            game.life_forms[(x, y, 'brown')] = game.r.create_oval(x-2, y-2, x+2, y+2,
                            outline = "#099c0e", fill = "#099c0e", width = 5)

def genes(i):
    return game.name_list[i].genes


def blobs(n):
    for j in range(n):
        game.name_list[game.i] = Character(game, str(game.i), randint(50, 1300), randint(50, 750),
                        {'A1': (randint(0, 100)-50)/100, 'A2': (randint(0, 100)-50)/100, 'A3': (randint(0, 100)-50)/100,
                         'A4': (randint(0, 100)-50)/100, 'A5': (randint(0, 100)-50)/100, 'A6': (randint(0, 100)-50)/100,
                         'A7': (randint(0, 100)-50)/100, 'A8': (randint(0, 100)-50)/100, 'A9': (randint(0, 100)-50)/100,
                         'B1': (randint(0, 100)-50)/100, 'B2': (randint(0, 100)-50)/100, 'B3': (randint(0, 100)-50)/100,
                         'B4': (randint(0, 100)-50)/100, 'B5': (randint(0, 100)-50)/100, 'B6': (randint(0, 100)-50)/100,
                         'B7': (randint(0, 100)-50)/100, 'B8': (randint(0, 100)-50)/100, 'B9': (randint(0, 100)-50)/100,
                         'C1': (randint(0, 100)-50)/100, 'C2': (randint(0, 100)-50)/100, 'C3': (randint(0, 100)-50)/100,
                         'C4': (randint(0, 100)-50)/100, 'C5': (randint(0, 100)-50)/100, 'C6': (randint(0, 100)-50)/100,
                         'C7': (randint(0, 100)-50)/100, 'C8': (randint(0, 100)-50)/100, 'C9': (randint(0, 100)-50)/100,
                         'D': (randint(0, 100)-50)/100, 'D1': (randint(0, 100)-50)/100, 'D2': (randint(0, 100)-50)/100, 'D3': (randint(0, 100)-50)/100,
                         'E': (randint(0, 100)-50)/100, 'E1': (randint(0, 100)-50)/100, 'E2': (randint(0, 100)-50)/100, 'E3': (randint(0, 100)-50)/100,
                         'F': (randint(0, 100)-50)/100, 'F1': (randint(0, 100)-50)/100, 'F2': (randint(0, 100)-50)/100, 'F3': (randint(0, 100)-50)/100,
                         'Fr': (randint(0, 100)-50)/100, 'Fr1': (randint(0, 100)-50)/100, 'Fr2': (randint(0, 100)-50)/100, 'Fr3': (randint(0, 100)-50)/100,
                         'Ba': (randint(0, 100)-50)/100, 'Ba1': (randint(0, 100)-50)/100, 'Ba2': (randint(0, 100)-50)/100, 'Ba3': (randint(0, 100)-50)/100,
                         'L': (randint(0, 100)-50)/100, 'L1': (randint(0, 100)-50)/100, 'L2': (randint(0, 100)-50)/100, 'L3': (randint(0, 100)-50)/100,
                         'R': (randint(0, 100)-50)/100, 'R1': (randint(0, 100)-50)/100, 'R2': (randint(0, 100)-50)/100, 'R3': (randint(0, 100)-50)/100,
                         'N': (randint(0, 100)-50)/100, 'N1': (randint(0, 100)-50)/100, 'N2': (randint(0, 100)-50)/100, 'N3': (randint(0, 100)-50)/100},
                                           500, 5, [50, 50, 0])
        game.i += 1

def evolved(n):
    genes = {'A1': 0.006, 'A2': 0.218, 'A3': -0.204, 'A4': 0.002, 'A5': 0.207, 'A6': -0.213, 'A7': 0.002, 'A8': -0.003, 'A9': -0.027, 'B1': 0.292, 'B2': -0.453, 'B3': 0.343, 'B4': 0.279, 'B5': -0.465, 'B6': 0.333, 'B7': 0.052, 'B8': -0.012, 'B9': -0.058, 'C1': -0.516, 'C2': 0.361, 'C3': 0.007, 'C4': -0.513, 'C5': 0.381, 'C6': -0.027, 'C7': -0.002, 'C8': 0.002, 'C9': -0.024, 'D': 0.201, 'D1': -0.383, 'D2': 0.02, 'D3': -0.469, 'E': 0.189, 'E1': -0.515, 'E2': 0.313, 'E3': -0.57, 'F': -0.401, 'F1': -0.567, 'F2': 0.2, 'F3': -0.535, 'Fr': 0.38, 'Fr1': -0.345, 'Fr2': -0.061, 'Fr3': -0.26, 'Ba': 0.184, 'Ba1': -0.122, 'Ba2': 0.256, 'Ba3': -0.57, 'L': -0.293, 'L1': -0.148, 'L2': 0.507, 'L3': 0.416, 'R': 0.408, 'R1': 0.163, 'R2': -0.414, 'R3': -0.508, 'N': 0.263, 'N1': 0.226, 'N2': -0.417, 'N3': -0.323}
    for j in range(n):
        temp = {}
        for k in genes:
            temp[k] = round(genes[k] + (randint(0, 4)-2)/1000, 3)
        game.name_list[game.i] = Character(game, str(game.i), randint(50, 1300), randint(50, 750), temp, 500, 5, [100, 0, 0])
        game.i += 1

def scavenger(n):
    genes = {'A1': -0.47, 'A2': -0.402, 'A3': 0.041, 'A4': 0.453, 'A5': -0.201, 'A6': 0.058, 'A7': -0.346, 'A8': -0.449, 'A9': -0.101, 'B1': 0.415, 'B2': -0.051, 'B3': 0.449, 'B4': -0.318, 'B5': -0.169, 'B6': 0.144, 'B7': -0.117, 'B8': -0.167, 'B9': -0.424, 'C1': -0.162, 'C2': -0.269, 'C3': 0.471, 'C4': 0.268, 'C5': 0.159, 'C6': -0.287, 'C7': -0.224, 'C8': -0.388, 'C9': 0.083, 'D': 0.462, 'D1': -0.52, 'D2': -0.274, 'D3': 0.378, 'E': -0.039, 'E1': 0.141, 'E2': 0.433, 'E3': 0.475, 'F': 0.44, 'F1': 0.426, 'F2': -0.503, 'F3': 0.184, 'Fr': 0.216, 'Fr1': 0.127, 'Fr2': -0.048, 'Fr3': 0.104, 'Ba': 0.076, 'Ba1': -0.347, 'Ba2': -0.397, 'Ba3': 0.454, 'L': 0.415, 'L1': -0.077, 'L2': -0.415, 'L3': -0.237, 'R': 0.01, 'R1': -0.272, 'R2': -0.179, 'R3': -0.11, 'N': 0.234, 'N1': 0.187, 'N2': -0.241, 'N3': 0.123}
    for j in range(n):
        temp = {}
        for k in genes:
            temp[k] = round(genes[k] + (randint(0, 20)-10)/1000, 3)
        game.name_list[game.i] = Character(game, str(game.i), randint(50, 1300), randint(50, 750), temp, 500, 5, [0, 100, 0])
        game.i += 1

def champ():
    m = 0
    champ = None
    for i in game.name_list:
        score = game.name_list[i].fd_count
        if score > m:
            m = score
            champ = i
    print(f"Champ is {champ} with a score of {m}")

fd()
#blobs(40)
#evolved(20)
scavenger(50)
game.time = 10
#game.stats = True

#hardcode {'A1': 0.004, 'A2': 0.217, 'A3': -0.204, 'A4': 0.002, 'A5': 0.206, 'A6': -0.214, 'A7': 0.003, 'A8': -0.005, 'A9': -0.025, 'B1': 0.293, 'B2': -0.452, 'B3': 0.345, 'B4': 0.281, 'B5': -0.465, 'B6': 0.333, 'B7': 0.054, 'B8': -0.011, 'B9': -0.058, 'C1': -0.514, 'C2': 0.363, 'C3': 0.005, 'C4': -0.511, 'C5': 0.382, 'C6': -0.025, 'C7': 0.0, 'C8': 0.0, 'C9': -0.022, 'D': 0.202, 'D1': -0.383, 'D2': 0.019, 'D3': -0.47, 'E': 0.187, 'E1': -0.514, 'E2': 0.312, 'E3': -0.568, 'F': -0.4, 'F1': -0.567, 'F2': 0.202, 'F3': -0.535, 'Fr': 0.379, 'Fr1': -0.346, 'Fr2': -0.061, 'Fr3': -0.261, 'Ba': 0.185, 'Ba1': -0.124, 'Ba2': 0.258, 'Ba3': -0.572, 'L': -0.291, 'L1': -0.15, 'L2': 0.507, 'L3': 0.414, 'R': 0.408, 'R1': 0.161, 'R2': -0.413, 'R3': -0.506, 'N': 0.261, 'N1': 0.224, 'N2': -0.417, 'N3': -0.321}


'''
game.name_list[1] = Character(game, '1', ("#e3eb98","#fffef7","#ffe788"), 500, 500)
game.name_list[2] = Character(game, '2', ("#e3eb98","#fffef7","#ffe788"), 500, 500)
game.name_list[3] = Character(game, '3', ("#e3eb98","#fffef7","#ffe788"), 500, 500)
'''
