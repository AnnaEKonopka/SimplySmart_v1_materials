1# SimplySmart_v1, this is actual application 
2# Figure_2_raw_data, these are input images and output from SimplySmart_v1
3# Figure_3_raw_data, these are input images and output from SimplySmart_v1
4# Figure_4_raw_data, these are input images and output from SimplySmart_v1
5# Figure_5_and_6_raw_data, these are input images and output from SimplySmart_v1
6# Figure_7_raw_data, these are input images and output data from tools comparison 
7# Figure_8_raw_data, these are input images and output from SimplySmart_v1
8# SimplySmart_v1.py, this is source code
9# external_images_test, SimplySmart_v1 test on images avilable on CellProfiler web-side (the used images and output included) 

Implementation: 

Step 1. Prepare folders with images to be analysed. Images for each channel should be placed in separate folders. SimplySmart_v1 accepts following image formats: JPEG,  PNG, TIFF. 
Step 2.  Run application and press button on interface to provide path to folder with MARKER images. These are images, which will be used for the recognition of neurons to be analysed (for example, DAPI or NeuN stained neurons). Copy and paste absolute path to the folder. Klick OK, next button will appear on interface. 
 If new button will not appear check if provided path is correct. The new button will appear only if data and path to data are provided correctly. 
Step 3. Klick on ‘Select foci’ button and provide path to folder with DNA damage images. Klick OK and next button will appear. 
Similarly, if new button will not appear check if provided path is correct. New button will appear only if path and data are provided correctly. 
With this action two graph appear, 1) representing distribution of pixel intensity, calculated as a sum of specific pixels intensity of all input images, 2) histogram representing the size of detected objects (MARKER). 
Step 4. Klick on new button ‘Recognize neurons’. You will be asked to provide i) value for thresholding in range from 0 to 255 (this can be determined based on the displayed graph ‘pixel_intensity’, the graph flattening allows to determine cut-off point for background, in addition the graph displays suggested value for the minimal cut-off point as a difference between mean pixel intensity and mean intensity calculated after subtraction of dominance), ii) minimum and maximum area of MARKER to be considered in the analysis in pixels (this can be determined based on the displayed histogram of ‘MARKER_size’), iii) minimal area of foci to be analysed in pixels (user choice, type 1 if do not have specific requirements for foci size). Klick OK. The application will go through all images to detect neurons/nuclei about specified parameters. Once completed new button will appear.
If you do not see ‘Done!’ and new button does not appear, check if your folders with images are correct, for example contain equal number of images for each channel and in correct format. 
Step 5. Klick on new button ‘Measure foci’. Now application recognizes DNA damage foci within filtered in Step 4 nuclei. Last button will appear. 
If you do not see ‘Done! Save results!’ and new button does not appear, check if your folders with images are correct, for example contain equal number of images for each channel and in correct format.
Step 6. Klick on button ‘Save results’, you will be asked to provide name for your output folder. Use name, which will describe your set of data specifically, do not use name ‘Results’ as this name is used by application. Now, the analysis is completed and you will find your output folder within application folder. Your output folder will contain three folders with output images, i) ‘Output_images_nucleus’ (with detected nuclei/neurons), ii) ‘Output_images_DNAdamage’ (with detected DNA damage), and iii) Output_images_overlaid (with merged raw images and detected DNA damage foci) You will also get CSV file ‘Given_parameters’ with parameters provided by you and CSV file ‘Quantification’ with the results. 
You can do visual inspection of output images to exclude potential clump nuclei, or nuclei located at the edge of image. However, well defined range of MARKER size to be analysed allows to avoid or reduce such occurrence. 
Step 7. Close and run application again to analyse another batch of images. Your output folder will stay intact in its original location. 
