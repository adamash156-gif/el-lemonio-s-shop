# el lemonio 🍋

A tiny desktop shop app built with Python's built-in `tkinter` library.

Pick products from a colorful shop screen, then head to your cart where
every item you bought shows up as a little card you can pick up and
drag around with your mouse.

## Features

- 🛒 Simple product shop with colored buttons and live prices
- 🧾 Cart counter that updates as you buy
- 🖱️ Draggable cart cards — click and hold to move them anywhere on screen
- 🎨 Clean, colorful UI with no external dependencies

## Requirements

- Python 3.x
- `tkinter` (comes pre-installed with most Python installations)

No `pip install` needed — everything runs off the standard library.

## Getting Started

Clone the repo and run the script:

```bash
git clone https://github.com/your-username/el-lemonio-s-shop.git
cd el-lemonio-s-shop
python shop.py
```

> On some Linux distributions, `tkinter` isn't bundled with Python and
> needs to be installed separately, e.g.:
> ```bash
> sudo apt-get install python3-tk
> ```

## How to Use

1. Launch the app — you'll land on the **Shop** screen.
2. Press a product button to add it to your cart (the counter updates
   at the top).
3. Click **"Go to Cart ->"** to see everything you bought.
4. On the **Cart** screen, click and drag any card to move it around.
5. Click **"<- Back to Shop"** to buy more.

## Project Structure

```
el-lemonio/
├── shop.py       # main application
└── README.md     # this file
```

## Possible Future Improvements

- [ ] Remove items from the cart (e.g. right-click to delete a card)
- [ ] A trash-can drop zone to remove cards by dragging them out
- [ ] Snap cards to a grid layout
- [ ] Save/load the cart between runs
- [ ] Total price display on the cart screen

## License

Feel free to use, modify, and share this project.
