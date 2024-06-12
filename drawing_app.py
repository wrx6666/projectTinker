import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")


        self.canvas_width = 600
        self.canvas_height = 400

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1
        self.eraser_mode = False
        self.last_pen_color = 'black'

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<Button-1>', self.add_text)

        self.root.bind('<Control-s>', self.save_image_shortcut)
        self.root.bind('<Control-c>', self.choose_color_shortcut)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_var = tk.StringVar()
        self.brush_size_var.set("1")
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, "1", "2", "5", "10", "15", "20", "25", command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.toggle_eraser)
        eraser_button.pack(side=tk.LEFT)


        help_button = tk.Button(control_frame, text="Руководство", command=self.show_help)
        help_button.pack(side=tk.LEFT)


        resize_button = tk.Button(control_frame, text="Изменить размер", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)


        text_button = tk.Button(control_frame, text="Текст", command=self.add_text_dialog)
        text_button.pack(side=tk.LEFT)


        background_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background)
        background_button.pack(side=tk.LEFT)


        self.color_preview = tk.Canvas(control_frame, width=20, height=20, bg=self.pen_color)
        self.color_preview.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            if self.eraser_mode:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=int(self.brush_size_var.get()), fill='white',
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='white',
                               width=int(self.brush_size_var.get()))
            else:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=int(self.brush_size_var.get()), fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                               width=int(self.brush_size_var.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.eraser_mode = False
        self.color_preview.config(bg=self.pen_color)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, size):
        self.brush_size = int(size)

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.last_pen_color = self.pen_color
            self.pen_color = 'white'
            self.color_preview.config(bg=self.pen_color)
        else:
            self.pen_color = self.last_pen_color
            self.color_preview.config(bg=self.pen_color)

    def pick_color(self, event):
        x, y = event.x, event.y
        rgb = self.image.getpixel((x, y))
        self.pen_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        self.eraser_mode = False
        self.color_preview.config(bg=self.pen_color)

    def save_image_shortcut(self, event=None):
        self.save_image()

    def choose_color_shortcut(self, event=None):
        self.choose_color()

    def show_help(self):
        help_text = "Горячие клавиши:\n" \
                    "Ctrl+S - Сохранить\n" \
                    "Ctrl+C - Выбрать цвет"
        messagebox.showinfo("Руководство", help_text)

    def resize_canvas(self):

        new_width = simpledialog.askinteger("Изменить размер", "Введите новую ширину:")
        new_height = simpledialog.askinteger("Изменить размер", "Введите новую высоту:")


        if new_width is None or new_height is None or new_width <= 0 or new_height <= 0:
            return


        self.canvas_width = new_width
        self.canvas_height = new_height
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)


        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def add_text_dialog(self):
        text = simpledialog.askstring("Введите текст", "Введите текст:")
        if text:
            self.text_to_add = text

    def add_text(self, event):
        if hasattr(self, 'text_to_add'):
            x, y = event.x, event.y
            self.draw.text((x, y), self.text_to_add, fill=self.pen_color)
            self.canvas.create_text(x, y, text=self.text_to_add, fill=self.pen_color)
            delattr(self, 'text_to_add')

    def change_background(self):
        new_color = colorchooser.askcolor(color=self.canvas['background'])[1]
        if new_color:
            self.canvas.config(background=new_color)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()