# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:27:36 2026

@author: ivang
"""

import requests
import random
import textwrap
from PIL import Image
from io import BytesIO

from colorama import Fore, Style, init
init(autoreset=True)

def print_section(title):
    print(Fore.CYAN + "\n" + "═"*60)
    print(Fore.YELLOW + f"{title.center(60)}")
    print(Fore.CYAN + "═"*60)
    
DINO_LIST = [
    "Tyrannosaurus", "Triceratops", "Stegosaurus", "Velociraptor",
    "Brachiosaurus", "Spinosaurus", "Allosaurus", "Ankylosaurus",
    "Diplodocus", "Parasaurolophus", "Pachycephalosaurus", "Carnotaurus"
]

# Core biological data (stable taxonomy)
DINO_CORE_DATA = {
    "Tyrannosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Triceratops": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Stegosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Velociraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Brachiosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Spinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Allosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Ankylosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Diplodocus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Parasaurolophus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Pachycephalosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Carnotaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"}
}

# Encyclopedia information
LOCAL_DINO_DATA = {

    "Tyrannosaurus": {
        "meaning": "Tyrant lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "8–9 tons",
        "fun_fact": "One of the terrestrial predators with the most powerful bite force ever recorded."
    },

    "Triceratops": {
        "meaning": "Three-horned face",
        "length": "8–9 m",
        "height": "3 m",
        "weight": "6–12 tons",
        "fun_fact": "The large neck frill likely served for defense and species recognition."
    },

    "Stegosaurus": {
        "meaning": "Roofed lizard",
        "length": "9 m",
        "height": "4 m",
        "weight": "5 tons",
        "fun_fact": "The dorsal plates may have been used for thermoregulation or display."
    },

    "Velociraptor": {
        "meaning": "Swift thief",
        "length": "2 m",
        "height": "0.5 m",
        "weight": "15 kg",
        "fun_fact": "Fossil evidence shows it had feathers and was much smaller than depicted in films."
    },

    "Brachiosaurus": {
        "meaning": "Arm lizard",
        "length": "22–26 m",
        "height": "12–13 m",
        "weight": "35–50 tons",
        "fun_fact": "Its front legs were longer than its hind legs, producing a giraffe-like posture."
    },

    "Spinosaurus": {
        "meaning": "Spine lizard",
        "length": "14–16 m",
        "height": "5–7 m",
        "weight": "7–10 tons",
        "fun_fact": "Likely semi-aquatic and possibly the largest known carnivorous dinosaur."
    },

    "Allosaurus": {
        "meaning": "Different lizard",
        "length": "8–10 m",
        "height": "3–4 m",
        "weight": "2–3 tons",
        "fun_fact": "One of the dominant predators of the Late Jurassic ecosystems in North America."
    },

    "Ankylosaurus": {
        "meaning": "Fused lizard",
        "length": "6–8 m",
        "height": "1.7 m",
        "weight": "6–8 tons",
        "fun_fact": "Possessed heavy armor and a massive tail club used for defense."
    },

    "Diplodocus": {
        "meaning": "Double beam",
        "length": "24–27 m",
        "height": "4–5 m",
        "weight": "12–16 tons",
        "fun_fact": "Its extremely long tail may have functioned like a whip."
    },

    "Parasaurolophus": {
        "meaning": "Near crested lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "2.5–3 tons",
        "fun_fact": "The hollow crest likely acted as a resonating chamber for sound."
    },

    "Pachycephalosaurus": {
        "meaning": "Thick-headed lizard",
        "length": "4–5 m",
        "height": "1.5–2 m",
        "weight": "400–500 kg",
        "fun_fact": "Its skull dome may have been used for head-butting behavior."
    },

    "Carnotaurus": {
        "meaning": "Meat-eating bull",
        "length": "7–9 m",
        "height": "3 m",
        "weight": "1.3–2 tons",
        "fun_fact": "Recognizable by the horns above its eyes and extremely reduced forelimbs."
    }
}

def dino_explorer():

    user_input = input("Enter a dinosaur name (or press ENTER for random): ").strip().capitalize()
    name = user_input if user_input else random.choice(DINO_LIST)

    print("\n" + "="*60)
    print(f"      PALEONTOLOGICAL DOSSIER: {name.upper()}")
    print("="*60)

    headers = {'User-Agent': 'DinoExplorerBot/1.0'}

    location = "Unknown location"
    era_range = "Unknown"

    try:
        url_p = f"https://paleobiodb.org/data1.2/occs/list.json?base_name={name}&show=full"
        r_p = requests.get(url_p, timeout=5).json()

        if r_p.get("records"):
            f = r_p["records"][0]

            location = f"{f.get('st','Unknown area')} ({f.get('cc','??')})"

            start_age = f.get("lag")
            end_age = f.get("eag")

            if start_age and end_age:
                era_range = f"{start_age} – {end_age} Ma"
            else:
                era_range = f"{end_age} Ma"

    except:
        pass


    desc = "No information found."
    img_url = None

    try:
        url_w = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}"
        r_w = requests.get(url_w, headers=headers, timeout=5).json()

        desc = r_w.get("extract", desc)

        img_url = (
            r_w.get("originalimage", {}).get("source")
            or r_w.get("thumbnail", {}).get("source")
        )

    except:
        pass


    core = DINO_CORE_DATA.get(name, {})
    info = LOCAL_DINO_DATA.get(name, {})

    print_section("TAXONOMY")
    print(Fore.GREEN + f"Class        : " + Style.RESET_ALL + f"{core.get('class','Unknown')}")
    print(Fore.GREEN + f"Order        : " + Style.RESET_ALL + f"{core.get('order','Unknown')}")
    print(Fore.GREEN + f"Diet         : " + Style.RESET_ALL + f"{core.get('diet','Unknown')}")
    print(Fore.GREEN + f"Name Meaning : " + Style.RESET_ALL + f"{info.get('meaning','Unknown')}")
    
    print_section("PHYSICAL CHARACTERISTICS")
    print(Fore.MAGENTA + f"Length       : " + Style.RESET_ALL + f"{info.get('length','Unknown')}")
    print(Fore.MAGENTA + f"Height       : " + Style.RESET_ALL + f"{info.get('height','Unknown')}")
    print(Fore.MAGENTA + f"Weight       : " + Style.RESET_ALL + f"{info.get('weight','Unknown')}")
     
    print_section("PALEONTOLOGY")
    print(Fore.BLUE + f"Fossil Sites : " + Style.RESET_ALL + f"{location}")
    print(Fore.BLUE + f"Time Range   : " + Style.RESET_ALL + f"{era_range}")
    
    print_section("DESCRIPTION")
    print(textwrap.fill(desc, width=60))
    
    print_section("SCIENTIFIC NOTE")
    print(textwrap.fill(info.get("fun_fact","No recorded trivia."), width=60))

    if img_url:
        try:
            r_i = requests.get(img_url, headers=headers, timeout=10)
            img = Image.open(BytesIO(r_i.content))
            print("Displaying specimen reconstruction...")
            img.show()
        except:
            print("Image rendering failed.")
    else:
        print("No visual record found.")

    print("="*60 + "\n")

if __name__ == "__main__":
    dino_explorer()