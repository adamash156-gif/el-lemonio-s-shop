import tkinter as tk
from tkinter import messagebox
import random

# ----------------------------------------------------------------------
# el lemonio - a tiny shop app
#
# Screen 1 (Shop): pick products by pressing colored buttons.
# Screen 2 (Cart) : every product you bought shows up as a small card
#                   that you can pick up and drag around with the mouse.
# ----------------------------------------------------------------------

screen = tk.Tk()
screen.geometry('560x600')
screen.title('el lemonio')
screen['bg'] = '#fff4e0'   # soft cream background for the main window

# Products: name -> (price, color)
PRODUCTS = {
    "Lemon Soda": (2.50, "#f9d923"),
    "Iced Tea":   (3.00, "#a1de93"),
    "Cookie":     (1.50, "#d98324"),
    "Cupcake":    (2.00, "#f2a2b0"),
    "Water":      (1.00, "#8ecae6"),
    "Chips":      (2.20, "#eae2b7"),
    "Donut":      (2.30, "#ffb4a2"),
    "Muffin":     (2.10, "#cdb4db"),
    "Pretzel":    (1.80, "#e5989b"),
    "Ice Cream":  (3.50, "#bde0fe"),
    "Sandwich":   (4.00, "#ffd6a5"),
    "Popcorn":    (1.70, "#fefae0"),
}

cart_items = []   # holds names of things the user bought
cart_total = 0.0  # running total of everything bought so far

# ------------------------------------------------------------------
# Two frames stacked on top of each other. We just raise the one we
# want to show ("shop_frame" or "cart_frame").
# ------------------------------------------------------------------
shop_frame = tk.Frame(screen, bg='#fff4e0')
cart_frame = tk.Frame(screen, bg='#2b2d42')

for frame in (shop_frame, cart_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)


# ------------------------------- SHOP -------------------------------
tk.Label(
    shop_frame, text="el lemonio", font=("Helvetica", 22, "bold"),
    bg='#fff4e0', fg='#4a3728'
).pack(pady=15)

cart_count_label = tk.Label(
    shop_frame, text="Cart: 0 item(s)", font=("Helvetica", 11),
    bg='#fff4e0', fg='#4a3728'
)
cart_count_label.pack()

# total price shown as a small badge in the top-right corner, styled like
# the product cards (rounded-ish look via a colored frame + icon)
total_badge = tk.Frame(shop_frame, bg='#f9d923', bd=0)
total_badge.place(relx=1.0, y=12, x=-12, anchor='ne')

tk.Label(
    total_badge, text="🛒", font=("Helvetica", 10),
    bg='#f9d923', fg='#2b2d42'
).pack(side='left', padx=(8, 2), pady=4)

total_label = tk.Label(
    total_badge, text="$0.00",
    font=("Helvetica", 10, "bold"),
    bg='#f9d923', fg='#2b2d42'
)
total_label.pack(side='left', padx=(0, 8), pady=4)

buttons_area = tk.Frame(shop_frame, bg='#fff4e0')
buttons_area.pack(pady=15)


def buy(product_name):
    """Add a product to the cart and update the counter + total labels."""
    global cart_total
    cart_items.append(product_name)
    cart_total += PRODUCTS[product_name][0]
    cart_count_label.config(text=f"Cart: {len(cart_items)} item(s)")
    total_label.config(text=f"${cart_total:.2f}")


# Lay the products out in a 3-column grid of colored buttons
row = col = 0
for name, (price, color) in PRODUCTS.items():
    b = tk.Button(
        buttons_area,
        text=f"{name}\n${price:.2f}",
        width=12, height=3,
        bg=color, fg='#2b2d42',
        activebackground='#ffffff',
        font=("Helvetica", 10, "bold"),
        relief='raised', bd=2,
        command=lambda n=name: buy(n)
    )
    b.grid(row=row, column=col, padx=8, pady=8)
    col += 1
    if col == 3:
        col = 0
        row += 1


def go_to_cart():
    build_cart_cards()
    cart_frame.tkraise()


tk.Button(
    shop_frame, text="Go to Cart ->", font=("Helvetica", 12, "bold"),
    bg='#4a3728', fg='white', activebackground='#6b4f3a',
    command=go_to_cart
).pack(pady=10)


# ------------------------------- CART -------------------------------
tk.Label(
    cart_frame, text="Your Cart", font=("Helvetica", 20, "bold"),
    bg='#2b2d42', fg='white'
).place(x=15, y=10)

tk.Label(
    cart_frame, text="(drag the cards around)", font=("Helvetica", 9),
    bg='#2b2d42', fg='#c8c8d0'
).place(x=15, y=45)

back_button = tk.Button(
    cart_frame, text="<- Back to Shop", font=("Helvetica", 11, "bold"),
    bg='#8ecae6', fg='#2b2d42',
    command=lambda: shop_frame.tkraise()
)
back_button.place(x=15, y=555)


def pay():
    """Show a payment confirmation, then empty the cart."""
    global cart_total
    if not cart_items:
        messagebox.showinfo("Cart is empty", "Add some products before paying!")
        return

    messagebox.showinfo(
        "Payment successful",
        f"You paid ${cart_total:.2f} for {len(cart_items)} item(s). Enjoy!"
    )

    cart_items.clear()
    cart_total = 0.0
    cart_count_label.config(text="Cart: 0 item(s)")
    total_label.config(text="$0.00")
    build_cart_cards()


pay_button = tk.Button(
    cart_frame, text="Pay Now 💳", font=("Helvetica", 11, "bold"),
    bg='#f9d923', fg='#2b2d42', activebackground='#ffe57f',
    command=pay
)
pay_button.place(relx=1.0, x=-15, y=555, anchor='ne')

# keep track of card widgets so we can clear them each time we rebuild
cart_card_widgets = []


def make_draggable(widget):
    """Bind mouse events so the widget can be dragged with the mouse."""
    def on_press(event):
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        widget.lift()  # bring the card on top of the others

    def on_drag(event):
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        widget.place(x=x, y=y)

    widget.bind("<ButtonPress-1>", on_press)
    widget.bind("<B1-Motion>", on_drag)


def build_cart_cards():
    """Clear old cards and create a fresh draggable card for each bought item."""
    for w in cart_card_widgets:
        w.destroy()
    cart_card_widgets.clear()

    for name in cart_items:
        price, color = PRODUCTS[name]
        card = tk.Frame(cart_frame, bg=color, width=110, height=70,
                         relief='raised', bd=2)
        card.pack_propagate(False)

        tk.Label(card, text=name, bg=color, font=("Helvetica", 9, "bold")).pack(pady=(8, 0))
        tk.Label(card, text=f"${price:.2f}", bg=color, font=("Helvetica", 9)).pack()

        x = random.randint(20, 400)
        y = random.randint(90, 490)
        card.place(x=x, y=y)

        make_draggable(card)
        cart_card_widgets.append(card)


shop_frame.tkraise()

screen.mainloop()
