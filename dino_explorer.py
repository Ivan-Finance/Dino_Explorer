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
    "Diplodocus", "Parasaurolophus", "Pachycephalosaurus", "Carnotaurus",
    "Deinonychus", "Utahraptor", "Giganotosaurus", "Carcharodontosaurus",
    "Iguanodon", "Edmontosaurus", "Corythosaurus", "Lambeosaurus", 
    "Apatosaurus", "Argentinosaurus", "Camarasaurus", "Therizinosaurus",
    "Oviraptor", "Dilophosaurus", "Microraptor"
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
    "Carnotaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Deinonychus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Utahraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Giganotosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Carcharodontosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Iguanodon": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Edmontosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Corythosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Lambeosaurus": {"class": "Reptilia", "order": "Ornithischia", "diet": "Herbivore"},
    "Apatosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Argentinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Camarasaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Therizinosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Herbivore"},
    "Oviraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Omnivore"},
    "Dilophosaurus": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"},
    "Microraptor": {"class": "Reptilia", "order": "Saurischia", "diet": "Carnivore"}
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
    },
    
      "Deinonychus": {
        "meaning": "Terrible claw",
        "length": "3–3.5 m",
        "height": "1.5 m",
        "weight": "70–100 kg",
        "fun_fact": "Its large sickle-shaped claw inspired the modern image of agile raptor dinosaurs."
    },

    "Utahraptor": {
        "meaning": "Utah predator",
        "length": "6–7 m",
        "height": "2 m",
        "weight": "500–700 kg",
        "fun_fact": "The largest known dromaeosaurid, much bigger than Velociraptor."
    },

    "Giganotosaurus": {
        "meaning": "Giant southern lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "6–8 tons",
        "fun_fact": "One of the largest carnivorous dinosaurs ever discovered."
    },

    "Carcharodontosaurus": {
        "meaning": "Shark-toothed lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "6–7 tons",
        "fun_fact": "Named for its blade-like teeth resembling those of sharks."
    },

    "Iguanodon": {
        "meaning": "Iguana tooth",
        "length": "9–11 m",
        "height": "5 m",
        "weight": "3–5 tons",
        "fun_fact": "One of the first dinosaurs ever scientifically described in the 19th century."
    },

    "Edmontosaurus": {
        "meaning": "Edmonton lizard",
        "length": "12–13 m",
        "height": "4 m",
        "weight": "4 tons",
        "fun_fact": "Many fossils preserve impressions of skin, revealing a scaly texture."
    },

    "Corythosaurus": {
        "meaning": "Helmet lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "3 tons",
        "fun_fact": "Its tall crest may have been used for visual display and sound resonance."
    },

    "Lambeosaurus": {
        "meaning": "Lambe's lizard",
        "length": "9–10 m",
        "height": "4 m",
        "weight": "2.5–3 tons",
        "fun_fact": "Its hollow crest likely amplified vocal calls within the herd."
    },

    "Apatosaurus": {
        "meaning": "Deceptive lizard",
        "length": "21–23 m",
        "height": "4–5 m",
        "weight": "20–25 tons",
        "fun_fact": "Previously confused with the dinosaur Brontosaurus in early classifications."
    },

    "Argentinosaurus": {
        "meaning": "Argentina lizard",
        "length": "30–35 m",
        "height": "15 m",
        "weight": "60–80 tons",
        "fun_fact": "One of the largest land animals known to have ever existed."
    },

    "Camarasaurus": {
        "meaning": "Chambered lizard",
        "length": "18–20 m",
        "height": "7 m",
        "weight": "20 tons",
        "fun_fact": "Its vertebrae contained hollow chambers that reduced body weight."
    },

    "Therizinosaurus": {
        "meaning": "Scythe lizard",
        "length": "9–10 m",
        "height": "5 m",
        "weight": "5 tons",
        "fun_fact": "Famous for its enormous claws that could exceed one meter in length."
    },

    "Oviraptor": {
        "meaning": "Egg thief",
        "length": "1.5–2 m",
        "height": "1 m",
        "weight": "20–30 kg",
        "fun_fact": "Originally thought to steal eggs, later fossils showed it was actually protecting its own nest."
    },

    "Dilophosaurus": {
        "meaning": "Two-crested lizard",
        "length": "6–7 m",
        "height": "2 m",
        "weight": "400 kg",
        "fun_fact": "Recognizable by the pair of crests on its skull."
    },

    "Microraptor": {
        "meaning": "Small thief",
        "length": "0.8–1 m",
        "height": "0.4 m",
        "weight": "1 kg",
        "fun_fact": "Had feathers on both arms and legs, allowing it to glide between trees."
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

