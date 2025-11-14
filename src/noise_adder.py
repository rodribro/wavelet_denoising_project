from skimage.util import random_noise
import os
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte, img_as_float

class NoiseAdder:

    VALID_KWARGS = {
        'mean': float,
        'var': float,
        'amount': float,
        'salt_vs_pepper': float,
    }
    MODE_KWARGS = {
        'gaussian': ['mean', 'var'],
        'speckle': ['mean', 'var'],
        'poisson': [],
        's&p': ['amount', 'salt_vs_pepper'],
    }

    def __init__(self, mode:str, **kwargs):

        if mode not in self.MODE_KWARGS:
            raise ValueError(f"Invalid mode: {mode}")
    
        valid_keys = self.MODE_KWARGS[mode]
        for key in kwargs:
            if key not in valid_keys:
                raise ValueError(f"Parameter '{key}' not valid for mode '{mode}'")
            
        self.mode = mode
        self.kwargs = kwargs
    
    def add_noise(self, image):
        """
        Apply noise separately to each channel.
        """
        

        noisy = image.copy()
        for c in range(image.shape[2]):
            noisy[..., c] = random_noise(image[..., c], mode=self.mode, **self.kwargs)

        return noisy

    
    
    def get_noise_string(self):
        """Generate a string representation for file/folder naming"""
        if not self.kwargs:
            return self.mode
        
        param_parts = []
        for k, v in self.kwargs.items():
            if v is not None:
                if isinstance(v, float):
                    v_str = str(v).replace('.', 'p')
                else:
                    v_str = str(v)
                param_parts.append(f"{k}{v_str}")
        
        param_str = "_".join(param_parts)
        return f"{self.mode}_{param_str}" if param_str else self.mode

if __name__ == "__main__":
    

    os.makedirs("../images/noisy_images", exist_ok=True)
    image_folders = os.listdir("../images/original")

    noise_configs = [
        # Gaussian
        NoiseAdder(mode='gaussian', mean=0, var=0.001),
        NoiseAdder(mode='gaussian', mean=0, var=0.005),
        NoiseAdder(mode='gaussian', mean=0, var=0.01),
        NoiseAdder(mode='gaussian', mean=0, var=0.02),
        NoiseAdder(mode='gaussian', mean=0, var=0.04),
        # Speckle
        NoiseAdder(mode='speckle', mean=0, var=0.02),
        NoiseAdder(mode='speckle', mean=0, var=0.05),
        NoiseAdder(mode='speckle', mean=0, var=0.1),
        # Salt & Pepper
        NoiseAdder(mode='s&p', amount=0.02, salt_vs_pepper=0.5),
        NoiseAdder(mode='s&p', amount=0.05, salt_vs_pepper=0.5),
        NoiseAdder(mode='s&p', amount=0.1, salt_vs_pepper=0.5),
        # Poisson
        NoiseAdder(mode='poisson'),
    ]


    for folder in image_folders:
        images = os.listdir(f"../images/original/{folder}")
        print(f"Processing folder: {folder} with {len(images)} images")
        
        for noise_adder in noise_configs:
            
            noise_desc = noise_adder.get_noise_string().replace('.', 'p')
            output_dir = f"../images/noisy_images/{folder}/{noise_desc}"
            os.makedirs(output_dir, exist_ok=True)
            
            for img_name in images:
                image = img_as_float(imread(f"../images/original/{folder}/{img_name}"))
                print(f'Image {img_name}: {image.shape}')
                noisy_image = noise_adder.add_noise(image)
                noisy_image_uint8 = img_as_ubyte(noisy_image)
                
                imsave(f"{output_dir}/{img_name}", noisy_image_uint8)

                
                


