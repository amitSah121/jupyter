import os
import shutil
import random
from PIL import Image

def create_dataset_structure(base_path):
    # Create the new directory structure
    new_base = os.path.join(base_path, 'animal_dataset')
    for split in ['train', 'validation', 'test']:
        os.makedirs(os.path.join(new_base, split), exist_ok=True)

def gather_images(base_path):
    images = []
    for animal in ['cats', 'dogs', 'snakes']:
        animal_path = os.path.join(base_path, 'archive', 'Animals', animal)
        for img in os.listdir(animal_path):
            if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append((os.path.join(animal_path, img), animal))
    return images

def create_annotation(img_path, animal, destination):
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            
        img_filename = os.path.basename(img_path)
        ann_filename = os.path.split(img_filename)[0] + '.txt'
        ann_path = os.path.join(".","animal_dataset","ann.txt")
        
        with open(ann_path, 'a+') as f:
            f.write(f"{img_filename},")
            f.write(f"{animal},")
            f.write(f"{width},")
            f.write(f"{height}\n")
        
        return ann_path, width
    except Exception as e:
        print(f"Error creating annotation for {img_path}: {str(e)}")
        return None

def split_and_copy_images(images, base_path):
    random.shuffle(images)
    total = len(images)
    train_split = int(0.7 * total)
    val_split = int(0.15 * total)

    for i, (img_path, animal) in enumerate(images):
        if i < train_split:
            destination = os.path.join(base_path, 'animal_dataset', 'train', animal)
        elif i < train_split + val_split:
            destination = os.path.join(base_path, 'animal_dataset', 'validation', animal)
        else:
            destination = os.path.join(base_path, 'animal_dataset', 'test', animal)
        
        os.makedirs(destination, exist_ok=True)
        # shutil.copy(img_path, destination)
        create_annotation(img_path, animal, destination)

def main():
    base_path = '.'  # Assuming script is run from the directory containing 'archieve'
    
    create_dataset_structure(base_path)
    images = gather_images(base_path)
    split_and_copy_images(images, base_path)
    
    print("Dataset reorganization complete!")

if __name__ == "__main__":
    main()