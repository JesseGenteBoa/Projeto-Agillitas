from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, Label
from mariquinhaCorrente import robozinho
from mariquinhaUnitaria import lancamentoIsolado
from utils import clicarMicrosiga
from time import sleep
import mensagens
import threading
from acaoComum import rejeitarCaixa



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"Imagens")


def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


def abrirNovaJanela():
    nova_janela = Toplevel()
    nova_janela.title("Rejeitar Caixa")

    largura = 250
    altura = 125

    x = (nova_janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (nova_janela.winfo_screenheight() // 2) - (altura // 2)

    nova_janela.geometry(f"{largura}x{altura}+{x}+{y}")
    nova_janela.iconbitmap(relative_to_assets("robozinho.ico"))

    label = Label(nova_janela, text="Insira a mensagem de rejeição:")
    label.pack(padx=10, pady=(10, 5))

    entrada = Entry(nova_janela)
    entrada.pack(padx=10, pady=10)

    def aoClicar():
        mensagem = entrada.get()
        rejeitarCaixa(mensagem, tipo="Independente")
        nova_janela.destroy()

    botao = Button(nova_janela, text="Executar", command=aoClicar)
    botao.pack(padx=10, pady=10)


def abrirGui():

    def validarEntrada(P):
        P = P.strip()
        if len(P) > 8:
            return False
        return True
        

    def soltarAMariquinha():
        sleep(0.5)
        window.iconify()
        sleep(1)
        clicarMicrosiga()
        threading.Thread(target=robozinho).start()


    def lancarRTIndividual():
        rt = entry_1.get()
        rt = rt.upper()
        if len(rt) == 8:
            rt = rt[-5:]
        if len(rt) == 5:
            if rt.isdigit():
                rt = "RT-" + rt
                sleep(0.5)
                window.iconify()
                sleep(1)
                threading.Thread(target=lancamentoIsolado, args=(rt,)).start()


    window = Tk()

    bot = mensagens.Mensagens(window)

    bot.mostrarInfo(bot.info, bot.texto)
    bot.mostrarInfo(bot.info2, bot.texto2)
    bot.mostrarInfo(bot.info3, bot.texto3)
    bot.mostrarAviso(bot.info4, bot.texto4)

    window.deiconify()

    vcmd = (window.register(validarEntrada), '%P')

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = str((screen_width - 500) // 2)
    y = str((screen_height - 550) // 2)

    window.geometry(f"505x333+{x}+{y}")
    window.iconbitmap(relative_to_assets("robozinho.ico"))
    window.title("Automação IntAgillitas")
    window.configure(bg = "#FF8D8D")


    canvas = Canvas(
        window,
        bg = "#FF8D8D",
        height = 333,
        width = 505,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        505.0,
        333.0,
        fill="#FF8D8D",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        cursor="hand2",
        highlightthickness=0,
        command=lambda: soltarAMariquinha(),
        relief="flat",
        background="#FF8D8D",
        bd=0.5,
        highlightcolor="#FF8D8D",
        highlightbackground="#FF8D8D"
    )

    button_1.place(
        x=37.0,
        y=83.0,
        width=205.0,
        height=166.0
    )

    canvas.create_rectangle(
        207.0,
        266.0,
        298.0,
        300.0,
        fill="#FF8D8D",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        252.0,
        46.99998474121094,
        image=image_image_1
    )

    canvas.create_rectangle(
        263.0,
        86.0,
        465.0,
        249.0,
        fill="#FFFFFF",
        outline="")
    window.resizable(False, False)

    entry_image_1 = PhotoImage(
        file=relative_to_assets("RetanguloArredondado.png"))
    entry_bg_1 = canvas.create_image(
        362.0,
        166.0,
        image=entry_image_1
    )

    entry_1 = Entry(
        cursor="xterm",
        bg="#FED4D4",
        fg="#000000",
        insertwidth=2,
        relief="sunken",
        highlightthickness=1.3,
        highlightbackground="#000000",
        highlightcolor="#000000",
        font=("Cascadia Mono", 10),
        validate="key",
        validatecommand=vcmd
    )

    entry_1.place(
        x=325.0,
        y=140.0,
        width=107.0,
        height=28.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        cursor="hand2",
        highlightthickness=0,
        command=lambda: lancarRTIndividual(),
        relief="flat"
    )
    button_2.place(
        x=337.0,
        y=174.0,
        width=52.0,
        height=53.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("image_EQS.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        cursor="hand2",
        highlightthickness=0,
        command=lambda: abrirNovaJanela(),
        relief="flat"
    )
    button_3.place(
        x=202.0,
        y=267.0,
        width=99.0,
        height=42.0
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("bochecha.png"))
    entry_bg_4 = canvas.create_image(
        115.0,
        290.0,
        image=entry_image_4
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("bochecha.png"))
    entry_bg_5 = canvas.create_image(
        383.0,
        290.0,
        image=entry_image_5
    )

    canvas.create_text(
        290.0,
        143.0,
        anchor="nw",
        text="RT-",
        fill="#000000",
        font=("Latha", 11, "bold")
    )

    canvas.create_text(
        290.0,
        110.0,
        anchor="nw",
        text="Lançar RT individual",
        fill="#000000",
        font=("Latha", 11, "bold")
    )
    window.mainloop()