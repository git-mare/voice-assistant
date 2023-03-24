# https://github.com/git-mare/voice-assistant
# O programa consiste em realizar ações simples por voz, experimente falar "criar um evento" e siga os passos
# Após isso fale "lista" para abrir o cronograma de eventos criados.
# Você pode checar os outros comandos em Lista de aliases.
# OBS: Existe um intervalo na hora de receber o nome do evento e a hora do evento.
# O console irá avisar quando estiver ouvindo o nome do evento e a hora do evento.

import speech_recognition as sr
import pyttsx3
import webbrowser
import tkinter as tk
import threading
import sys
from tkinter import *
from tkinter.ttk import *

# Configuração do reconhecedor de voz
r = sr.Recognizer() # Variável da speech recognition
r.energy_threshold = 3000 # O valor inserido considera ou não como fala os valores recebidos por voz

# Configuração da engine de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'pt-br-f')  # Voz
engine.setProperty('rate', 190)  # Velocidade da fala

# Configuração da interface gráfica
root = tk.Tk()
root.geometry("600x600")
root.resizable(False, False)
root.title("Assistente")
root.configure(bg='#212121')

# Configuração da label que exibirá as mensagens
msg_label = tk.Label(root, font=('Arial', 16), bg='#212121', fg='white')
msg_label.place(relx=0.5, rely=0.3, anchor='center')

# Configuração do círculo lilás que indicará quando o programa estiver falando
microwave = tk.Canvas(root, width=50, height=50, bg='#212121', highlightthickness=0)
microwave.create_oval(5, 5, 45, 45, fill='#212121', outline='#c0c0c0')
microwave.place(relx=0.5, rely=0.6, anchor='center')

# Lista de aliases
internship_aliases = ['atividades', 'abre a lista', 'o que tem para fazer', 'lista', 'cronograma' 'abrir lista', 'abre a lista'] # Abre a janela com os eventos adicionados
close_aliases = ['fecha isso', 'fecha', 'fechar', 'fecha a última janela', 'fechar a última janela'] # Fecha a última janela (do programa) que estiver aberta
browser_aliases = ['abrir navegador',  'abre o navegador', 'navegador'] # Abre o navegador padrão da sua máquina
add_event_internship_aliases = ['adicionar evento', 'criar um novo evento', 'criar um evento', 'cria um evento', 'crie um evento', 'criar evento', 'cria um novo evento'] # Adiciona um evento a lista de eventos
close_program_aliases = ['fechar tudo', 'fecha tudo', 'desliga', 'tchau'] # Fecha o programa
clear_internship_events_aliases = ['limpar eventos', 'limpar lista', 'limpa os eventos', 'esvazia a lista', 'esvazia o cronograma'] # Limpa a lista de eventos adicionados

# Função que faz o programa falar
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Função que processa o comando de voz e realiza a ação correspondente
def process_voice_command():
    global microwave
    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source)
        print("Ouvindo...")
        microwave.create_oval(5, 5, 45, 45, fill='#212121', outline='white')
        root.update()
        audio = r.listen(source)
        microwave.create_oval(5, 5, 45, 45, fill='#c45fc9', outline='white')
        root.update()
        
        try:
            print("Processando...")
            command = r.recognize_google(audio, language='pt-BR').lower()
            print(f"Comando: {command}")

            if command in browser_aliases:
                speak("Abrindo")
                webbrowser.open_new("https://www.google.com")
           
            if command in close_aliases:
                speak("Fechando janela.")
                root.winfo_children()[-1].destroy()
                return
                
            if command in internship_aliases:
                speak("Abrindo lista")
                college_internship()
                
            if command in add_event_internship_aliases:
                add_college_internship_event()
                
            if command in close_program_aliases:
                close_program()
                
            if command in clear_internship_events_aliases:
                clear_internship_events()

            else:
                return
            
        except Exception as e:
            print(f"Erro: {e}")
            return

# Função para janela de Cronograma
def college_internship():
    global college_is
    college_is = Toplevel(root)
    college_is.title("Cronograma")
    college_is.geometry("600x600") 
    college_is.configure(bg='#212121')
    
     # Abre o arquivo e lê o conteúdo
    with open("cronograma.txt", "r") as f:
        text = f.read()

    # Configura a label que exibe o texto
    text_label = tk.Label(college_is, text=text, font=('Arial', 12), bg='#212121', fg='white', justify=LEFT)
    text_label.place(relx=0.0, rely=0.0)
    
# Função para adicionar eventos ao cronograma
def add_college_internship_event():
    speak("Qual evento deve ser adicionado?")
    while True:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            print("Ouvindo...")
            microwave.create_oval(5, 5, 45, 45, fill='#212121', outline='white')
            root.update()
            audio = r.listen(source)

        microwave.create_oval(5, 5, 45, 45, fill='#c45fc9', outline='white')
        root.update()

        try:
            print("Processando...")
            event = r.recognize_google(audio, language='pt-BR').lower()
            print(f"Evento: {event}")
            break

        except Exception as e:
            print(f"Erro: {e}")
            speak("Repita o nome do evento, por favor.")
            continue
    
    speak("Qual horário este evento ocorrerá?")
    while True:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            print("Ouvindo...")
            microwave.create_oval(5, 5, 45, 45, fill='#212121', outline='white')
            root.update()
            audio = r.listen(source)

            microwave.create_oval(5, 5, 45, 45, fill='#c45fc9', outline='white')
            root.update()

            try:
                print("Processando...")
                time_spoken = r.recognize_google(audio, language='pt-BR')
                print(f"Horário: {time_spoken}")

                # convertendo a hora falada para o formato hh:mm
                time_spoken = time_spoken.replace("horas", "").replace("h", "").strip()
                time_spoken_parts = time_spoken.split(":")
                if len(time_spoken_parts) == 1:
                    hours = int(time_spoken_parts[0])
                    minutes = 0
                elif len(time_spoken_parts) == 2:
                    hours = int(time_spoken_parts[0])
                    minutes = int(time_spoken_parts[1])
                else:
                    speak("Repita a hora do evento por favor.")
                    continue

                # adicionando o evento ao arquivo txt
                with open("cronograma.txt", "a") as f:
                    f.write(f"{hours:02d}:{minutes:02d} - {event}\n")

                speak(f"O evento '{event}' foi adicionado para as {hours:02d}:{minutes:02d}.")
                return

            except Exception as e:
                print(f"Erro: {e}")
                speak("Repita a hora do evento por favor.")
                continue

# Função para limpar os eventos do cronograma
def clear_internship_events():
    speak('O cronograma foi esvaziado')
    with open("cronograma.txt", "w") as f:
        f.write("")

# Função que fecha a última janela aberta
def close_last_window():
    all_windows = root.winfo_children()
    last_window = all_windows[-1]
    last_window.destroy()

# Função para fechar o programa
def close_program():
    speak("Até mais!")
    root.destroy()  # fechar a janela do tkinter
    sys.exit()  # encerrar o programa

# Loop "while True" que executará a função "process_voice_command()" em um thread separado
def voice_loop():
    while True:
        process_voice_command()

# Função que inicia o loop de voz em um thread separado
def start_voice_thread():
    voice_thread = threading.Thread(target=voice_loop)
    voice_thread.start()

# Inicia o processamento contínuo de voz em um thread separado
start_voice_thread()
root.mainloop()
