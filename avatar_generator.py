from email.mime import image
import random as rand
from typing import List
from layer import Layer
from PIL import Image
import os

class AvatarGenerator:
    def __init__(self, images_path: str):
        self.layers: List[Layer] =self.load_image_layers(images_path)
        self.background_colour = (248, 202, 250)
        self.rare_background_colour = (255,215,0)
        self.rare_background_chance = 0.05
        self.output_path: str = "./output"
        os.makedirs(self.output_path, exist_ok=True)

    def load_image_layers(self, images_path: str):
        sub_paths = sorted(os.listdir(images_path))
        layers: List[Layer] = []
        for sub_path in sub_paths:
            layer_path = os.path.join(images_path, sub_path)
            layer = Layer(layer_path)
            layers.append(layer)
        
        layers[2].rarity = 0.80
        layers[3].rarity = 0.15
        return layers

    def generate_image_sequence(self):
        image_path_sequence = []
        for layer in self.layers:
            if layer.should_generate():
                image_path = layer.get_random_image_path()
                image_path_sequence.append(image_path)
        return image_path_sequence

    def render_avatar_image(self, image_path_sequence: List[str]):

        if rand.random() < self.rare_background_chance:
            bg_colour = self.rare_background_colour
        else:
            bg_colour = self.background_colour
        image = Image.new("RGBA", (24,24), bg_colour)
        for image_path in image_path_sequence:
            layer_image = Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image

    def save_image(self, image: Image.Image, i: int = 0):
        image_index = str(i).zfill(3)
        image_file_name = f"avatar_{image_index}.png"
        image_save_path = os.path.join(self.output_path, image_file_name)
        image.save(image_save_path)

    def generate_avatar(self, n: int = 1):
        print("AvatarGenerator: Generating Avatar")
        for i in range(n):
            image_path_sequence = self.generate_image_sequence()
            image = self.render_avatar_image(image_path_sequence)
            self.save_image(image, i)