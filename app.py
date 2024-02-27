from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from imgaug import augmenters as iaa
import numpy as np
from PIL import Image
import io
import zipfile


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

seq = iaa.Sequential([
    iaa.Fliplr(0.5),  
    iaa.Affine(
        scale={"x": (0.5, 1), "y": (0.5, 1)},  
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},  
        rotate=(-30, 30),  
        shear=(-10, 10)  
    ),
    iaa.GaussianBlur(sigma=(0, 3.0))  
])

@app.get("/")
def form(request: Request):
    """Render the homepage with the form for uploading images."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_image(request: Request, file: UploadFile = File(...), augment_count: int = Form(...)):
    """Handle image upload and augmentation, then save augmented images to a ZIP file."""
    img = Image.open(file.file)
    img_array = np.array(img)
    
    
    augmented_images = seq(images=[img_array for _ in range(augment_count)])
    
    
    zip_filename = "augmented_images.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for idx, aug_img in enumerate(augmented_images, start=1):
            img_pil = Image.fromarray(aug_img)
            img_byte_arr = io.BytesIO()
            img_pil.save(img_byte_arr, format='PNG')
            img_data = img_byte_arr.getvalue()
            zipf.writestr(f"augmented_image_{idx}.png", img_data)
    
    return FileResponse(path=zip_filename, media_type='application/zip', filename=zip_filename)