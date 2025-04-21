import os
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm

# Configuration parameters
input_dir = "/Users/xmf/Desktop/picture2"
output_dir = "/Users/xmf/Desktop/picture22"
aug_multiplier = 5
target_size = (224, 224)
color_mode = "rgb"
valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')

# Data augmentation configuration
augmenter = ImageDataGenerator(
    rotation_range=35,
    width_shift_range=0.25,
    height_shift_range=0.25,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.5, 1.5],
    fill_mode='nearest'
)

def process_images():
    os.makedirs(output_dir, exist_ok=True)
    all_files = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(valid_exts):
                all_files.append(os.path.join(root, f))
    
    pbar = tqdm(all_files, desc="Processing Images")
    
    for img_path in pbar:
        try:
            with Image.open(img_path) as img:
                if color_mode == "grayscale":
                    img = img.convert("L")
                else:
                    img = img.convert("RGB")
                
                img = img.resize(target_size)
                x = np.expand_dims(np.array(img), axis=0)
                
                base_name = os.path.basename(img_path)
                filename, ext = os.path.splitext(base_name)
                save_prefix = f"{filename}_aug"
                
                count = 0
                for batch in augmenter.flow(x,
                                          batch_size=1,
                                          save_to_dir=output_dir,
                                          save_prefix=save_prefix,
                                          save_format="jpeg"):
                    count += 1
                    if count >= aug_multiplier:
                        break
                        
        except Exception as e:
            tqdm.write(f"Processing failed: {img_path} - {str(e)}")

if __name__ == "__main__":
    print("🖼️ Starting data augmentation...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Generating {aug_multiplier} augmented versions per image")
    
    process_images()
    
    print("\n✅ Data augmentation completed!")
    print(f"Augmented images have been saved to: {output_dir}")