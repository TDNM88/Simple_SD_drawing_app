import tkinter as tk
from PIL import Image, ImageTk
import torch
from transformers import pipeline

class DrawingApp:
    def __init__(self, root):
        root.geometry("800x600")
        root.title("Image Generator")

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.previous_x = None
        self.previous_y = None
        self.brush_size = 10

        self.color_picker = tk.ColorChooser(root)
        self.color_picker.pack()

        self.text_input = tk.Entry(root)
        self.text_input.pack()

        self.display_label = tk.Label(root, text="Prompt: ")
        self.display_label.pack()

        self.img_display = tk.Label(root)
        self.img_display.pack()

        self.generate_button = tk.Button(root, text="Generate Image", command=self.generate_image)
        self.generate_button.pack()

        self.unclick_button = tk.Button(root, text="Unclick", command=self.unclick)
        self.unclick_button.pack()

        self.line_width_label = tk.Label(root, text="Brush Size:")
        self.line_width_label.pack()

        self.line_width_slider = tk.Scale(root, from_=1, to=50, command=self.update_line_width)
        self.line_width_slider.pack()

    def process_text(self, event):
        text = self.text_input.get()
        # Process the entered text
        self.text_prompt = text
        self.display_label.configure(text=f"Prompt: {text}")
        self.text_input.delete(0, tk.END)

    def update_line_width(self, value):
        self.brush_size = int(value)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.previous_x = None
        self.previous_y = None

    def unclick(self, event):
        self.previous_x = None
        self.previous_y = None

    def generate_image(self):
        ps_data = self.canvas.postscript(colormode="color")
        init_image = Image.open(io.BytesIO(ps_data.encode("utf-8"))).convert("RGB")

        generator = torch.Generator(device="cpu").manual_seed(1024)
        image = pipeline(prompt=self.text_prompt, image=init_image,
                        strength=0.85, guidance_scale=7, generator=generator).images[0]

        tk_image = ImageTk.PhotoImage(image)
        self.img_display.delete("all")

        self.img_display.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.img_display.image = tk_image


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    app.run()