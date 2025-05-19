import os

from PIL import Image, ImageDraw, ImageFont

# Criar uma imagem simples para o avatar
img = Image.new("RGB", (100, 100), color="#3D4058")
d = ImageDraw.Draw(img)

# Adicionar um texto no centro
# Nota: você pode precisar ajustar o caminho da fonte
try:
    font = ImageFont.truetype("arial.ttf", 40)
except:
    font = ImageFont.load_default()

d.text((50, 50), "U", fill="#BD93F9", font=font, anchor="mm")

# Salvar a imagem
png_path = os.path.join("resources", "images", "default_avatar.png")
img.save(png_path)
print(f"Avatar criado: {png_path}")
