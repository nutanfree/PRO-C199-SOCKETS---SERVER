import socket
from threading import Thread
import random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8000
server.bind((ip_address,port))
server.listen()
list_of_clients = []
questions = ["In what year did the Great October Socialist Revolution take place? \na.1917\n b.1923\n c.1914\n d.1920",
             "What is the largest lake in the world? a.Caspian Sea\n b.Baikal\n c.Lake Superior\n d.Ontario",
             "Which planet in the solar system is known as the “Red Planet”? a.Venus\n b.Earth\n c.Mars\n d.Jupiter",
             "Who wrote the novel “War and Peace”? a.Anton Chekhov\n b.Fyodor Dostoevsky\n c.Leo Tolstoy\n d.Ivan Turgenev",
             "What is the capital of Japan? a.Beijing\n b.Tokyo\n c.Seoul\n d.Bangkok",
             "Which river is the longest in the world? a.Amazon\n b.Mississippi\n c.Nile\n d.Yangtze",
             "What gas is used to extinguish fires? a.Oxygen\n b.Nitrogen\n c.Carbon dioxide\n d.Hydrogen",
             "What animal is the national symbol of Australia? a.Kangaroo\n b.Koala\n c.Emu\n d.Crocodile",
             "Which of the following planets is not a gas giant? a.Mars\n b.Jupiter\n c.Saturn\n d.Uranus",
             "What is the name of the process by which plants convert sunlight into energy? a.Respiration\n b.Photosynthesis\n c.Oxidation\n d.Evolution"]
answers = ['a','b','c','c','b','c','b','a','a','b']
while True:
    conn,addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    new_thread = Thread(target=clientthread,args=(conn,nickname))
    new_thread.start()

    def clientthread(conn,nickname):
        score = 0
        conn.send("Welcome To This quiz game!".encode("utf-8"))
        conn.send("You will receive a question.The answer to that question shuld be one of a, b, c, d".encode("utf-8"))
        conn.send("Good Luck!!\n\n".encode("utf-8"))
        index, question, answer = get_random_question_answer(conn)
        while True:
                try:
                    message=conn.recv(2048).decode('utf-8')
                    if message:
                        if message.lower() == answer:
                            score += 1
                            conn.send(f"Bravo! Your Score is {score}\n\n".encode('utf-8'))
                        else:
                            conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                        remove_question(index)
                        index, question, answer = get_random_question_answer(conn)
                    else:
                        remove(conn)
                except:
                    continue

    def get_random_question_answer(conn):
        random_index = random.randint(0,len(questions) - 1)
        random_question = questions[random_index]
        random_answer = answers[random_index]
        conn.send(random_question.encode('utf-8'))
        return random_index, random_question, random_answer
    
    def remove_question(index):
        questions.pop(index)
        answers.pop(index)

