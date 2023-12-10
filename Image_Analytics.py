import os
import base64
import requests

import warnings
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

script_path = os.path.dirname(os.path.realpath(__file__))

def get_image_file(file_entry):
    global image_file
    image_file = filedialog.askopenfilename(parent = master, initialdir = "/", title = "Select Image File", filetypes = (("Image File", "*.jpg"), ("Image File", "*.jpeg"), ("Image File", "*.png"),))
    file_entry.delete(0, 'end')
    file_entry.insert(0, image_file)

def run_and_close(event = None):
    close()

def close(event = None):
    master.withdraw()
    master.destroy()

image_file = None

master = tk.Tk()
master.config(bg = "#002855")
master.title("")

master.resizable(False, False)

window_height = 300
window_width = 800

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

lbl = tk.Label(master, text = "IMAGE ANALYTICS APPLICATION", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.place(x = 100, y = 90)

from PIL import Image, ImageTk
logo_image = ImageTk.PhotoImage(Image.open(script_path + "\\actNable_Logo.png"))

label = tk.Label(master, text = "", image = logo_image)
label.place(x = 250, y = 10)

entry_data1 = tk.Entry(master, text = "", width = 80)
entry_data1.place(x = 180, y = 150)

tk.Label(master, text = "Select Image File", font = ('Arial', 10, 'bold')).place(x = 50, y = 150)
tk.Button(master, text = "Browse...", font = ('Arial', 10, 'bold'), width = 10, command = lambda:get_image_file(entry_data1)).place(x = 675, y = 150)

api_key = tk.StringVar()

tk.Label(master, text = "Your OpenAI GPT API Key", font = ('Arial', 10, 'bold')).place(x = 50, y = 200)

e = tk.Entry(master, font = ('Arial', 10, 'bold'), textvariable = api_key, width = 58).place(x = 250, y = 200)

tk.Button(master, text = "Analyze Image", font = ('Arial', 10, 'bold'), command = run_and_close, width = 20).place(x = 320, y = 250)

master.bind('<Return>', run_and_close)
master.bind('<Escape>', close)

master.mainloop()

cwd = os.path.dirname(os.path.realpath(image_file))
os.chdir(cwd)

# OpenAI API Key
api_key = api_key.get()

# Function to encode the image
def encode_image(image_file):
  with open(image_file, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image(image_file)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json = payload)

img_description = response.json()['choices'][0]['message']['content']

master = tk.Tk()
master.config(bg = "#002855")
master.title("")

master.resizable(False, False)

window_height = 300
window_width = 550

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

lbl = tk.Label(master, text = "IMAGE ANALYSIS RESULTS ", bg = '#002855', font = ('Arial', 25, 'bold'), fg = '#ABFF4F')
lbl.grid(row = 0, column = 0, sticky = 'w')

image_section = ttk.LabelFrame(master, text = "Image Description: ")
image_section.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")

image_description = ttk.Label(image_section, text = img_description, wraplength = 500)
image_description.grid(row = 1, column = 0, padx = 10, pady = 10)

master.mainloop()
