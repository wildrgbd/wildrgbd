import os 
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cat", type=str, required=True)
cat = parser.parse_args().cat

categories = {
'bottle': ['bottle.z01', 'bottle.z02', 'bottle.zip'],
'cup': ['cup.z01', 'cup.z02', 'cup.z03', 'cup.zip'],
'tooth_brush': ['tooth_brush.z01', 'tooth_brush.z02', 'tooth_brush.z03', 'tooth_brush.zip'],
'book': ['book.z01', 'book.zip'],
'box': ['box.z01', 'box.zip'],
'knife': ['knife.z01', 'knife.z02', 'knife.zip'],
'remote_control': ['remote_control.z01', 'remote_control.zip'],
'razor': ['razor.z01', 'razor.zip'],
'keyboard': ['keyboard.z01', 'keyboard.zip'],
'bowl': ['bowl.z01', 'bowl.z02', 'bowl.zip'],
'scissor': ['scissor.z01', 'scissor.z02', 'scissor.z03', 'scissor.zip'],
'kettle': ['kettle.z01', 'kettle.z02', 'kettle.zip'],
'bucket': ['bucket.zip'],
'pliers': ['pliers.z01', 'pliers.z02', 'pliers.zip'],
'ball': ['ball.z01', 'ball.zip'],
'mouse': ['mouse.z01', 'mouse.zip'],
'handbag': ['handbag.z01', 'handbag.z02', 'handbag.zip'],
'cellphone': ['cellphone.zip'],
'microwave': ['microwave.z01', 'microwave.zip'],
'hat': ['hat.z01', 'hat.z02', 'hat.zip'],
'clock': ['clock.z01', 'clock.zip'],
'shoe': ['shoe.z01', 'shoe.z02', 'shoe.z03', 'shoe.zip'],
'flower_pot': ['flower_pot.z01', 'flower_pot.z02', 'flower_pot.zip'],
'detergent': ['detergent.z01', 'detergent.z02', 'detergent.zip'],
'backpack': ['backpack.z01', 'backpack.z02', 'backpack.zip'],
'chair': ['chair.z01', 'chair.z02', 'chair.zip'],
'TV': ['TV.zip'],
'pineapple': ['pineapple.z01', 'pineapple.zip'],
'potato': ['potato.zip'],
'cucumber': ['cucumber.zip'],
'apple': ['apple.zip'],
'banana': ['banana.zip'],
'pear': ['pear.zip'],
'tomato': ['tomato.zip'],
'peach': ['peach.zip'],
'orange': ['orange.z01', 'orange.zip'],
'carrot': ['carrot.zip'],
'donut': ['donut.zip'],
'cake': ['cake.zip'],
'stuffed_toy': ['stuffed_toy.z01', 'stuffed_toy.z02', 'stuffed_toy.zip'],
'train': ['train.zip'],
'truck': ['truck.zip'],
'boat': ['boat.zip'],
'bus': ['bus.zip'],
'plane': ['plane.zip'],
'car': ['car.zip'],
}

if cat == 'all':
    for cat in sorted(list(categories.keys())):
        for file in categories[cat]:
            subprocess.run(f"wget https://huggingface.co/hongchi/wildrgbd/resolve/main/{file}?download=true -O {file}", shell=True)

        if len(categories[cat]) > 1:
            subprocess.run(f"zip -F {cat}.zip --out {cat}-single.zip", shell=True)
            subprocess.run(f"unzip {cat}-single.zip", shell=True)
            subprocess.run(f"rm {cat}-single.zip", shell=True)
            for file in categories[cat]:
                subprocess.run(f"rm {file}", shell=True)
        else:
            subprocess.run(f"unzip {cat}.zip", shell=True)
            subprocess.run(f"rm {cat}.zip", shell=True)
            
else:
    for file in categories[cat]:
        subprocess.run(f"wget https://huggingface.co/hongchi/wildrgbd/resolve/main/{file}?download=true -O {file}", shell=True)

    if len(categories[cat]) > 1:
        subprocess.run(f"zip -F {cat}.zip --out {cat}-single.zip", shell=True)
        subprocess.run(f"unzip {cat}-single.zip", shell=True)
        subprocess.run(f"rm {cat}-single.zip", shell=True)
        for file in categories[cat]:
            subprocess.run(f"rm {file}", shell=True)
    else:
        subprocess.run(f"unzip {cat}.zip", shell=True)
        subprocess.run(f"rm {cat}.zip", shell=True)
