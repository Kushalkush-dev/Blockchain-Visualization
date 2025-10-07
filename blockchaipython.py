import tkinter as tk
import hashlib
import time
import random

# ------------------------------
# Blockchain Logic
# ------------------------------

def generate_hash(index, data, nonce, prev_hash):
    content = f"{index}{data}{nonce}{prev_hash}"
    return hashlib.sha256(content.encode()).hexdigest()

def mine_block(index, data, prev_hash):
    nonce = 0
    while True:
        hash_val = generate_hash(index, data, nonce, prev_hash)
        if hash_val.startswith("000"):
            return nonce, hash_val
        nonce += 1

def create_chain(num_blocks=5):
    chain = []
    start = time.time()
    # Genesis block
    index = 0
    data = "Genesis Block"
    prev_hash = "0"
    nonce, hash_val = mine_block(index, data, prev_hash)
    chain.append({"index": index, "data": data, "nonce": nonce, "hash": hash_val, "prev_hash": prev_hash})

    # Other blocks
    for i in range(1, num_blocks):
        data = f"Block {i} Data"
        prev_hash = chain[i-1]["hash"]
        nonce, hash_val = mine_block(i, data, prev_hash)
        chain.append({"index": i, "data": data, "nonce": nonce, "hash": hash_val, "prev_hash": prev_hash})

    print(f"Blockchain created in {round(time.time() - start, 2)}s")
    return chain

# ------------------------------
# Futuristic Animated GUI
# ------------------------------

class AnimatedBlockchain:
    def __init__(self, chain):
        self.chain = chain
        self.window = tk.Tk()
        self.window.title("🌌 Block Chain Visualization(Hash Start With - '000') 🌌")
        self.window.configure(bg="#0a0a0a")

        self.canvas_width = max(1200, len(chain)*280)
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="#0a0a0a", highlightthickness=0)
        self.canvas.pack()

        self.block_w, self.block_h = 220, 160
        self.gap = 50
        self.start_x = 20
        self.y = 120
        self.colors = ["#0ff6ff", "#ff6ec7", "#a0ff6e", "#fffa6e", "#6eafff", "#ff6e6e"]

        self.pulse = 0
        self.draw_blocks()
        self.animate_arrows()
        self.window.mainloop()

    def draw_blocks(self):
        self.blocks_coords = []
        for block in self.chain:
            idx, info, nonce, h, prev_h = block.values()
            x = self.start_x + idx * (self.block_w + self.gap)

            # Gradient simulation using multiple rectangles
            for i in range(10):
                color = self._shift_color(self.colors[idx % len(self.colors)], i*15)
                self.canvas.create_rectangle(
                    x, self.y + i*6, x + self.block_w, self.y + (i+1)*6,
                    fill=color, outline=""
                )

            # Neon border
            self.canvas.create_rectangle(x, self.y, x+self.block_w, self.y+self.block_h, outline="#ffffff", width=2)

            # Block text
            self.canvas.create_text(x + self.block_w/2, self.y + 20, text=f"Block {idx}", font=("Orbitron", 12, "bold"), fill="#ffffff")
            self.canvas.create_text(x + self.block_w/2, self.y + 50, text=f"Data: {info}", font=("Arial", 10), fill="#ffffff")
            self.canvas.create_text(x + self.block_w/2, self.y + 75, text=f"Nonce: {nonce}", font=("Arial", 10), fill="#ffffff")
            self.canvas.create_text(x + self.block_w/2, self.y + 105, text=f"Hash:\n{h[:20]}...", font=("Courier", 8), fill="#ffffff")
            self.canvas.create_text(x + self.block_w/2, self.y + 135, text=f"Prev Hash:\n{prev_h[:20]}...", font=("Courier", 8), fill="#ffffff")

            self.blocks_coords.append((x, self.y, x+self.block_w, self.y+self.block_h))

        # Title
        self.canvas.create_text(self.canvas_width/2, 40, text="🌌 Animated Sci-Fi Blockchain 🌌", font=("Orbitron", 18, "bold"), fill="#0ff6ff")

    def animate_arrows(self):
        self.canvas.delete("arrow")
        for i in range(len(self.blocks_coords)-1):
            x1 = self.blocks_coords[i][2]
            y1 = (self.blocks_coords[i][1] + self.blocks_coords[i][3]) / 2
            x2 = self.blocks_coords[i+1][0]
            y2 = (self.blocks_coords[i+1][1] + self.blocks_coords[i+1][3]) / 2
            # Pulsating effect
            width = 2 + abs((self.pulse % 10) - 5) / 2
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=width, fill="#0ff6ff", tags="arrow")
        self.pulse += 1
        self.window.after(100, self.animate_arrows)

    def _shift_color(self, hex_color, amount):
        hex_color = hex_color.lstrip("#")
        r = min(255, int(hex_color[0:2],16)+amount)
        g = min(255, int(hex_color[2:4],16)+amount)
        b = min(255, int(hex_color[4:6],16)+amount)
        return f"#{r:02x}{g:02x}{b:02x}"

# ------------------------------
# Run Program
# ------------------------------
if __name__ == "__main__":
    chain = create_chain(num_blocks=5)
    AnimatedBlockchain(chain)
