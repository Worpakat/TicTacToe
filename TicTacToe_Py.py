from ctypes import *
import itertools 

 
STD_OUTPUT_HANDLE = -11
 
class COORD(Structure):
    pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]
 
def SetCursorPosNPrint(row, column, string):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(column, row))
    print(string)
    

def SetCursorPosition(row, column):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(column, row))

#SetCursorPosNPrint(6, 3, "Hello")  ##SetCursorPosition and Print Ornek
        
###  TicTacToe
#   ---|---|---
#    O | X | O       Eğer canvas 0. columndan başlarsa çizmeye   O ve X ler 1, 5, 9. columnlara denk geliyor
#   ---|---|---      Rowlar ise 1,3,5 "(coordinat*2)-1"
#    X | X | O                CANVAS
#   ---|---|---
#    X | O | X        
#   ---|---|---              #

def DrawGameCanvas(_start_row = 0, _start_col= 0 ):
    #Belirli bir orjinden ele alarak oyun tahtasini çizen method
    for i in range(7):
        SetCursorPosition(i + _start_row, _start_col)
        if i % 2 == 0:
            print("---|---|---")
        else:
            print("   |   |   ")

def DrawMenu():
    SetCursorPosNPrint(1,51,"TicTacToe") #scoreu (7,43) e yaz
    SetCursorPosNPrint(6,30,"Scores")
    SetCursorPosNPrint(7,30,"Player-1(O):0") #score u (7,43) e yaz
    SetCursorPosNPrint(8,30,"Player-2(X):0") #score u (8,43) e yaz
    SetCursorPosNPrint(6,67,"Tutorial") 
    SetCursorPosNPrint(7,67,'Write your move and press enter.' ) 
    SetCursorPosNPrint(8,67,'Like "12" which means 1st row  2nd column' ) 

def SetInputToCanvas(row, col, XorO, canvas_pan_row, canvas_pan_col):
    #Girilen oyun table kordinatlarına istenilen inputu girmemize yarayan method.
    SetCursorPosition(((row-1)*2+1)+canvas_pan_row, ((col-1)*4+1)+canvas_pan_col)
    print(XorO)

def SetInputToCtrlTable(_row, _col, _XorO, _control_table):
    _control_table[_row-1][_col-1] = _XorO

def CheckIsEmpty(_row, _col, _control_table):
    return _control_table[_row-1][_col-1] == "E"

def GetInput(canvas_pan_row, canvas_pan_col, _control_table, _player):
    
    def DeleteLatestInput(_will_be_deld_char_count): ##input yerini temizleyen method
        space = ""
        SetCursorPosition(11,72)
        
        for i in range(_will_be_deld_char_count):
            space+=" "
        
        print(space)    

    ##Input alıp kontrol edip uygunsas canvasa ve control table a atayan method
    SetCursorPosNPrint(11,39,"Player-1's turn, enter your move: ")
    if _player == True:
        SetCursorPosNPrint(11,46,"1")
    else:
        SetCursorPosNPrint(11,46,"2")
        
    will_be_deld_char_count = 0

    while True:
        DeleteLatestInput(will_be_deld_char_count)
        SetCursorPosition(11,72)
        _input = input()
        will_be_deld_char_count = len(_input) 
        DeleteLatestInput(will_be_deld_char_count)
        
        try:
            row = int(_input[0])
            col = int(_input[1])
        except (ValueError, IndexError)  : ##parantezle yazarak multiple exception yazabiliyoruz
            continue
        if not(row>=0 and row<=3 and col>=0 and col<=3):
            continue
        if CheckIsEmpty(row,col,_control_table):
            if _player:
                XorO = "O"
            else:
                XorO = "X"
            SetInputToCanvas(row,col,XorO,canvas_pan_row,canvas_pan_col)
            SetInputToCtrlTable(row,col,XorO,_control_table)
            break
        else:
            continue
    return row, col, XorO

def CheckForScore(_input_row, _input_col, XorO, _control_table, _ctrl_dict):
    """parametredeki hamleden sonra sayı olup olmadigini kontrol eden method"""
    
    score = 0
    #Her türlü dik ve yanı kontrol ediyoruz
    
    if _ctrl_dict["c"+str(_input_col)] == False:
        for row in range(len(_control_table)): #column checkleniyor
            if _control_table[row][_input_col-1] != XorO:
                break  #bir tane bile inputdan farklıysa o columnda sayı yoktur zaten
            elif row == len(_control_table) - 1: #3. row/col da da geçtiyse sayı demektir
                score+=1
                _ctrl_dict["c"+str(_input_col)] = True
            else:
                continue
    if _ctrl_dict["r"+str(_input_row)] == False:
        for col in range(len(_control_table)): #row checkleniyor (rowların ve columnların sayısı eşit olduğu için iteration sayısı aynı kalabilir)
            if _control_table[_input_row-1][col] != XorO:
                break  #bir tane bile inputdan farklıysa o rowda sayı yoktur zaten
            elif col == len(_control_table)-1: #3. row/col da da geçtiyse sayı demektir
                score+=1
                _ctrl_dict["r"+str(_input_row)] = True
            else:
                continue


    if not((_input_row == 2 or _input_col == 2) and not(_input_row == 2 or _input_col == 2)): ##artı kısmının değili: çaprazlarıda kontrol etceğimiz kısım 
        #çaprazlarıda kontrol et
        if _ctrl_dict["rc-"] == False:
            if _input_row != _input_col or (_input_row == 2 and _input_col == 2) :
                for row_index, col_index in zip(range(3), range(2,-1,-1)):  ## https://stackoverflow.com/questions/18648626/for-loop-with-two-variables : çift iteration için  
                    ##sağ üstten sol aşağıya checkliyor                                                            #buraya bakabilirsin
                    if _control_table[row_index][col_index] != XorO:
                        break  #bir tane bile inputdan farklıysa o rowda sayı yoktur zaten
                    elif row_index == len(_control_table)-1: #3. row/col da da geçtiyse sayı demektir
                        score+=1
                        _ctrl_dict["rc-"] = True

                    else:
                        continue
        if _ctrl_dict["rc+"] == False:
            if _input_row == _input_col or (_input_row == 2 and _input_col == 2) :
                for row_index, col_index in zip(range(3), range(3)):  ## https://stackoverflow.com/questions/18648626/for-loop-with-two-variables : çift iteration için  
                    ##sol üstten sağ aşağıya checkliyor                                                            #buraya bakabilirsin
                    if _control_table[row_index][col_index] != XorO:
                        break  #bir tane bile inputdan farklıysa o rowda sayı yoktur zaten
                    elif row_index == len(_control_table)-1: #3. row/col da da geçtiyse sayı demektir
                        score+=1
                        _ctrl_dict["rc+"] = True
                    else:
                        continue

    
        
    return score    

def PrintScore(_player, _score):
    if _player == True:
        SetCursorPosNPrint(7,42,_score)
    else:
        SetCursorPosNPrint(8,42,_score)
     

control_table = [["E", "E", "E"],
                 ["E", "E", "E"],
                 ["E", "E", "E"]]

ctrl_dict = {"r1":False, "r2":False, "r3":False, "c1":False, "c2":False, "c3":False, "rc+":False, "rc-":False }



    
canvas_pan_row = 3
canvas_pan_col = 50

DrawGameCanvas(canvas_pan_row,canvas_pan_col)
DrawMenu() 


player1_score = 0
player2_score = 0
player = True

for i in range(9):
    if player:
        input_row, input_col, XorO = GetInput(canvas_pan_row,canvas_pan_col,control_table, player)
        score = CheckForScore(input_row, input_col, XorO, control_table, ctrl_dict) 
        if score > 0:
            player1_score += score
            print("test",player1_score)
            PrintScore(player, player1_score)
        player = not player    
    else:
        input_row, input_col, XorO = GetInput(canvas_pan_row,canvas_pan_col,control_table, player)
        score = CheckForScore(input_row, input_col, XorO, control_table, ctrl_dict) 
        if score > 0:
            player2_score += score
            print("test",player2_score)
            PrintScore(player, player2_score)
        player = not player
     
winner = ""
if player1_score > player2_score:
    winner= "Player-1"
elif player1_score < player2_score:
    winner= "Player-2"
else:
    winner = "Draw" 
SetCursorPosNPrint(13,39,("Game Over\nWinner:",winner))
    

