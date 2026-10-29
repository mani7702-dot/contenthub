#!/usr/bin/env python3
import subprocess, os

# List of ScienceDaily top headlines to check
headlines = [
    "Smaller EV batteries, longer range",
    "secret glow in toxic fire salamanders",
    "hidden reason why muscles weaken",
    "hidden oxygen reservoir deep inside Earth",
    "Doomsday Glacier",
    "Artemis I mission radiation",
    "Low testosterone sugar liver",
    "slower aging hiding in your gut",
    "immune system hidden sense of touch",
    "hidden 100-million-year-old volcanic system",
    "ice ages hidden ocean chain reaction",
    "asteroid killed dinosaurs ants",
    "Common drugs viruses spread",
    "James Webb lava planet giant sunscreen",
    "Smithsonian recreated Universe",
    "spiders dream surprising clue",
    "Exercise rewires heart",
    "surprising clue brains resist Alzheimer",
    "2,700-year-old solar eclipse Earth",
    "30-year mystery inflammatory bowel",
    "3D thermal invisibility cloak",
    "Mayo Clinic zombie cells aging",
    "tiny laser computer memory",
    "simple exercise lower blood pressure",
    "magnetic vortices computers brain",
    "Chinese fungus D-rex roots",
    "invisible signs pancreatic cancer",
    "cannabis sleep gummies dark side",
    "pancreatic cancer DNA escape treatment",
    "detect dangerous mirror life",
    "magnetic web above Sun",
    "tiny snakes roll faster",
    "blood inflammatory bowel disease 10 years",
    "150-million-year bird dinosaur teeth",
    "Mediterranean diet tiny proteins",
    "hidden switch burns fat",
    "Switzerland glacier ice vanished",
    "Dental implants hijack immune system",
]

# Directories to search
dirs = ["content/news/", "content/blog/", "content/trending/"]

# Get all existing article titles and content snippets
existing_files = []
for d in dirs:
    if os.path.exists(d):
        for f in os.listdir(d):
            existing_files.append(os.path.join(d, f))

for h in headlines:
    found = False
    for f in existing_files:
        try:
            with open(f, 'r', errors='replace') as fh:
                content = fh.read().lower()
                if h.lower() in content:
                    found = True
                    break
        except:
            pass
    if not found:
        print(f"FRESH: {h}")