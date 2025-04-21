import os
from PIL import Image, ImageOps, ImageEnhance
import argparse

TARGET_RESOLUTION = (2592, 1944) 
JPEG_QUALITY = 85
ASPECT_RATIO = TARGET_RESOLUTION[0]/TARGET_RESOLUTION[1]  # 1.333 (4:3)
ENHANCE_FACTORS = {
    'contrast': 1.1,
    'sharpness': 1.2,
    'color': 1.05,
    'brightness': 1.03
}

def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
          
            img = ImageOps.exif_transpose(img).convert('RGB')
            
            original_width, original_height = img.size
            target_ratio = TARGET_RESOLUTION[0]/TARGET_RESOLUTION[1]
            
            if original_width/original_height > target_ratio:
                new_height = original_height
                new_width = int(new_height * target_ratio)
            else:
                new_width = original_width
                new_height = int(new_width / target_ratio)
            
            left = (original_width - new_width)/2
            top = (original_height - new_height)/2
            right = left + new_width
            bottom = top + new_height
            cropped = img.crop((left, top, right, bottom))
            
            resized = cropped.resize(TARGET_RESOLUTION, Image.LANCZOS)
            
            enhancer = ImageEnhance.Contrast(resized)
            enhanced = enhancer.enhance(ENHANCE_FACTORS['contrast'])
            
            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(ENHANCE_FACTORS['sharpness'])
            
            enhancer = ImageEnhance.Color(enhanced)
            enhanced = enhancer.enhance(ENHANCE_FACTORS['color'])
            
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(ENHANCE_FACTORS['brightness'])
            
            enhanced.save(output_path, "JPEG", 
                        quality=JPEG_QUALITY,
                        optimize=True,
                        progressive=True,
                        exif=b'')  

    except Exception as e:
        print(f"Failed to process {os.path.basename(input_path)}: {str(e)}")

def batch_process(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    success = 0
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            input_path = os.path.join(source_dir, filename)
            output_filename = f"picam3_{filename}"
            output_path = os.path.join(target_dir, output_filename)
            
            process_image(input_path, output_path)
            success += 1
            print(f"✓ Processed: {filename}")
    
    print(f"\nCompleted! Successfully processed {success} images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JPEG to Raspberry Pi Camera format (with auto-crop)')
    parser.add_argument('source_dir', help='Input directory path')
    parser.add_argument('target_dir', help='Output directory path')
    args = parser.parse_args()

    batch_process(args.source_dir, args.target_dir)