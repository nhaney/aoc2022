import os


with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
    text = f.read()

elf_loads = [
    sum(int(item) for item in inventory.split("\n")) for inventory in text.split("\n\n")
]

# part 1
print(max(elf_loads))

# part 2
print(sum(sorted(elf_loads, reverse=True)[:3]))
