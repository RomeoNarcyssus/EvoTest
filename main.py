import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime


class main():
    def __init__(self,root):
        self.font = ('Arial', 25)
        self.sfont=('Arial',19)
        self.root=root
        self.size=15
        self.step = 20
        self.fill_char='-'
        self.start()

    def start(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack()
        self.lbl = tk.Label(self.start_frame, text='Розмір поля:', font=self.font)
        self.lbl.pack()
        self.edit = tk.Entry(self.start_frame, font=self.font, justify=tk.CENTER)
        self.edit.insert(0, str(self.size))
        self.edit.pack()
        self.start_button = tk.Button(self.start_frame, text='Почати гру', font=self.font, command=self.start_button_press)
        self.start_button.pack(fill='both')
        self.load_button = tk.Button(self.start_frame, text='Завантажити файл реплею',command=self.load_button_press)
        self.load_button.pack(fill='both')
        self.edit.bind('<Return>',self.start_button_press)
        self.edit.focus_force()


    def load_button_press(self):
        filename=filedialog.askopenfilename()
        self.current_player = 'X'
        self.replay = True
        self.move_sequence=open(filename,'r').read().strip().split('\n')
        self.size=int(self.move_sequence.pop(0))
        if len(self.move_sequence)==0:
            self.canvas.unbind('<Button-1>')
        self.board = [[self.fill_char for x in range(self.size)] for x in range(self.size)]
        self.start_frame.destroy()
        self.prepare_game_field()

    def start_button_press(self,event=None):
        try:
            size=int(self.edit.get())
        except:
            messagebox.showwarning('Не корректний ввід','Не корректний ввід')
            return None
        if size<5:
            messagebox.showwarning('Занадто мале поле', 'Занадто мале поле')
            return None
        self.size=size
        self.current_player='X'
        self.replay=False
        self.board=[[self.fill_char for x in range(size)] for x in range(size)]
        self.start_frame.destroy()
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(self.timestamp + '.log', 'w') as f:
            f.write(str(self.size) + '\n')
            f.close()
        self.prepare_game_field()

    def prepare_game_field(self):
        self.game_frame=tk.Frame(self.root)
        self.game_frame.pack()
        self.player_label=tk.Label(self.game_frame,text='Хід '+self.current_player)
        self.player_label.pack(fill='both')
        self.canvas=tk.Canvas(self.game_frame,width=self.size*self.step,height=self.size*self.step)
        for i in range(0,self.size*self.step,self.step):
            self.canvas.create_line(i, 0, i, self.size*self.step)
            self.canvas.create_line(0, i, self.size * self.step, i)
        self.canvas.bind('<Button-1>',self.game_click)
        self.canvas.pack()
        self.new_game_button=tk.Button(self.game_frame, text='Почати нову гру', command=self.new_game)
        self.new_game_button.pack(fill="both")


    def game_click(self,event):
        if self.replay:
            pos_y,pos_x=[int(x) for x in self.move_sequence.pop(0).split()]
            if len(self.move_sequence)==0:
                self.canvas.unbind('<Button-1>')
        else:
            try:
                for i in range(0, self.size * self.step, self.step):
                    if 0<event.x-i<self.step:
                        pos_x=i//self.step
                    if 0<event.y-i<self.step:
                        pos_y=i//self.step
            except:
                return None
            #print(event.x, event.y, pos_x, pos_y)
            if self.board[pos_y][pos_x]!=self.fill_char:
                return None
            with open(self.timestamp + '.log', 'a') as f:
                f.write(str(pos_y) + ' ' + str(pos_x) + '\n')
                f.close()
        self.board[pos_y][pos_x]=self.current_player
        color='green' if self.current_player=='X' else 'red'
        self.canvas.create_text(((pos_x+0.5)*self.step,(pos_y+0.5)*self.step),text=self.current_player,fill=color,font=self.sfont)
        self.current_player='O' if self.current_player=='X' else 'X'
        self.player_label.config(text='Хід '+self.current_player)
        self.check_winner()


    def check_line(self,s):
        win_x=s.find('X'*5)
        if win_x!=-1:
            return 'X', win_x
        win_o=s.find('O'*5)
        if win_o != -1:
            return 'O', win_o
        return None, -1

    def end_game(self,winner):
        messagebox.showinfo('Переможець "' + winner + '"', 'Переможець "' + winner + '"')
        self.canvas.unbind('<Button-1>')


    def check_winner(self):
        for i in range(self.size):
            winner,pos=self.check_line(''.join(self.board[i]))
            if winner!=None:
                #horizontal
                color='green' if winner=='X' else 'red'
                self.canvas.create_line((pos-0.25)*self.step,(i+0.5)*self.step,(pos+5.25)*self.step,(i+0.5)*self.step,
                                        fill=color,width=2)
                self.end_game(winner)
                return None
        vert=[[x[i] for x in self.board] for i in range(self.size)]
        for i in range(self.size):
            winner,pos=self.check_line(''.join(vert[i]))
            if winner!=None:
                #vertical
                color = 'green' if winner == 'X' else 'red'
                self.canvas.create_line((i+0.5)*self.step,(pos-0.25)*self.step,(i+0.5)*self.step,(pos+5.25)*self.step,
                                        fill=color, width=2)
                self.end_game(winner)
                return None
        for i in range(0,(self.size-4)):
            # main diagonal up
            main_diag_up=[self.board[j][j+i] for j in range(self.size-i)]
            winner, pos = self.check_line(''.join(main_diag_up))
            if winner!=None:
                color = 'green' if winner == 'X' else 'red'
                self.canvas.create_line((pos+i-0.25)*self.step,(pos-0.25)*self.step,(pos+i+5.25)*self.step,(pos+5.25)*self.step,
                                        fill=color, width=2)
                self.end_game(winner)
                return None
            main_diag_down=[self.board[j+i][j] for j in range(self.size-i)]
            winner, pos = self.check_line(''.join(main_diag_down))
            if winner != None:
                color = 'green' if winner == 'X' else 'red'
                self.canvas.create_line((pos - 0.25) * self.step, (pos +i- 0.25) * self.step,
                                        (pos + 5.25) * self.step, (pos +i+ 5.25) * self.step,
                                        fill=color, width=2)
                self.end_game(winner)
                return None
            #------------
            #anti diagonal
            anti_diag_up=[self.board[self.size-j-1-i][j] for j in range(self.size-i)]
            winner, pos = self.check_line(''.join(anti_diag_up))
            if winner != None:
                color = 'green' if winner == 'X' else 'red'
                self.canvas.create_line((pos - 0.25) * self.step, (self.size-pos-i+ 0.25) * self.step,
                                        (pos +5.25) * self.step, (self.size-pos-i- 5.25) * self.step,
                                        fill=color, width=2)
                self.end_game(winner)
                return None
            anti_diag_down=[self.board[self.size-j-1][j+i] for j in range(self.size-i)]
            #print(anti_diag_down)
            winner, pos = self.check_line(''.join(anti_diag_down))
            if winner != None:
                color = 'green' if winner == 'X' else 'red'
                self.canvas.create_line((pos+i - 0.25) * self.step, (self.size - pos + 0.25) * self.step,
                                        (pos +i+ 5.25) * self.step, (self.size - pos - 5.25) * self.step,
                                        fill=color, width=2)
                self.end_game(winner)
                return None
        if ''.join([''.join(x) for x in self.board]).count(self.fill_char)==0:
            self.end_game('ДРУЖБА')



    def new_game(self):
        self.game_frame.destroy()
        self.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('')
    root.resizable(False, False)
    app = main(root)
    root.mainloop()