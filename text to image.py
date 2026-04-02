import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk
from authtoken import auth_token
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
from torch import autocast
from diffusers import StableDiffusionPipeline
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

app = tk.Tk()
app.geometry("800x600")
app.title("stable buddy")

ctk.set_appearance_mode("dark")
prompt = ctk.CTkEntry(master=app, height=40, width=512, font =("Arial", 20), text_color="green", fg_color="white")
prompt.place(x=10,y=10)

lab = ctk.CTkLabel(master=app, height=400, width=512)
lab.place(x=10,y=110)

def generate():
    with autocast("cuda"):
        image = pipe(prompt.get(), guidance_scale=8.5).images[0]
    image.save("output.png")
    img = ImageTk.PhotoImage(image)
    lab.configure(image=img)
    lab.image = img


hit = ctk.CTkButton(master=app, height=40, width=512, font =("Arial", 20), text_color="yellow", fg_color="red")
hit.configure(text="Generate")
hit.configure(command= generate)
hit.place(x=206,y=60)

modelid = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(modelid, revision='fp16', torch_dtype=torch.float16, use_auth_token=auth_token)
pipe.to(device)

app.mainloop()