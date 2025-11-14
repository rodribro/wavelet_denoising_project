### <b> Multiscale image denoising using wavelet decomposition </b>

This project explores multiscale image denoising using wavelet decomposition. 

Images from several datasets (radiology, histology, and dense-object scenes) are corrupted with various types of noise, including additive Gaussian, speckle, Poisson, and salt-and-pepper. 

Using PyWavelets, the noisy images are decomposed, thresholded (hard and soft), and reconstructed to evaluate the effectiveness of different wavelet families and filtering strategies. Performance is measured via MSE, PSNR, and SSIM, and results are compared against a baseline Gaussian smoothing method.