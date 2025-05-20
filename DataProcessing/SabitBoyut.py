from PIL import Image, ImageOps
import os

folders = ["CizgiRoman", "Cocuk", "KisiselGelisim", "Polisiye", "Tarih"]

target_size = (325, 325)

for folder in folders:
    input_folder = folder
    output_folder = folder + "_325x325"
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        save_path = os.path.join(output_folder, relative_path)
        os.makedirs(save_path, exist_ok=True)

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    image_path = os.path.join(root, file)
                    image = Image.open(image_path).convert("RGB")

                    image.thumbnail(target_size, Image.LANCZOS)

                    delta_w = target_size[0] - image.size[0]
                    delta_h = target_size[1] - image.size[1]
                    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))

                    new_image = ImageOps.expand(image, padding, fill=(0, 0, 0))

                    save_file_path = os.path.join(save_path, os.path.splitext(file)[0] + ".jpg")
                    new_image.save(save_file_path, "JPEG", quality=95)

                    print(f"[{folder}] Kaydedildi: {save_file_path}")

                except Exception as e:
                    print(f"Hata oluştu: {file}, Hata: {e}")

print("Tüm klasörlerde görseller başarıyla 325x325 olarak kaydedildi!")
