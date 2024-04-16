#final version

import wx

class MyPanel(wx.Panel):
    
    def __init__(self, parent):
        super().__init__(parent)
              
        button1 = wx.Button(self, label='Select marker', pos=(5, 10), size=(110, 25))
        button1.Bind(wx.EVT_BUTTON, self.on_button1)
                      
    def on_button1(self, event):  #channel selection MARKER/DAPI
        
        import os
        import shutil
        
        path_results = "Results"
        shutil.rmtree(path_results, ignore_errors=True) #removes exisitng folder with results 
        shutil.rmtree("DNAdamage_thresholded", ignore_errors=True) #removes exisitng folder with results and creates new one
        os.mkdir("Results")                             
        os.mkdir("Results/Output_images_DNAdamage")
        os.mkdir("DNAdamage_thresholded")
        os.mkdir("Results/Output_images_nucleus")
            
        try:
            absolute_MARKER_path = wx.TextEntryDialog(self, message="Provide path to MARKER")
            absolute_MARKER_path.ShowModal()
            my_MARKER_path = absolute_MARKER_path.GetValue()
            absolute_MARKER_path.Destroy()

            relative_path_MARKER = os.path.relpath(my_MARKER_path) 
            self.relative_corrected_MARKER = relative_path_MARKER.replace("\\", "/") + "/*"
        except ValueError:
            st = wx.StaticText(self, label = "No path specified", pos=(140, 15))
                
        st = wx.StaticText(self, label = self.relative_corrected_MARKER, pos=(140, 15))
        
        if st:   
            button2 = wx.Button(self, label='Select foci', pos=(5, 45), size=(110, 25))
            button2.Bind(wx.EVT_BUTTON, self.on_button2)
        else:
            print("Error") #internal check if there is no error 
        
    def on_button2(self, event): #channel selection for DNA damage foci
        
        import os
        
        try:
            absolute_FOCI_path = wx.TextEntryDialog(self, message="Provide path to FOCI") 
            absolute_FOCI_path.ShowModal()
            my_FOCI_path = absolute_FOCI_path.GetValue()
            absolute_FOCI_path.Destroy()

            relative_path_FOCI = os.path.relpath(my_FOCI_path) 
            self.relative_corrected_FOCI = relative_path_FOCI.replace("\\", "/") + "/*"
        except ValueError:
            st = wx.StaticText(self, label = "No path specified", pos=(140, 50))
                                            
        st = wx.StaticText(self, label = self.relative_corrected_FOCI, pos=(140, 50))
        
        if st:
            button3 = wx.Button(self, label='Recognize neurons', pos=(5, 80), size=(110, 25))
            button3.Bind(wx.EVT_BUTTON, self.on_button3)
        else:
            print("Error")
        
    def on_button3(self, event):
        
        import cv2
        import glob  
        import numpy as np
        import matplotlib.pyplot as plt
        import os
        import pandas as pd
                
        try:           
            input_pixel_size = wx.TextEntryDialog(self, message="Provide pixel size [um2]")
            input_pixel_size.ShowModal()
            self.my_pixel_size = input_pixel_size.GetValue()
            input_pixel_size.Destroy()
            
            print(self.my_pixel_size)
            
            input_threshold = wx.TextEntryDialog(self, message="Provide value for treshold [from 0 to 255]")
            input_threshold.ShowModal()
            self.input_threshold = input_threshold.GetValue()
            input_threshold.Destroy()
            
            print(self.input_threshold)
            
            input_min_marker = wx.TextEntryDialog(self, message="Provide MIN area for MARKER detection [in pixels]")
            input_min_marker.ShowModal()
            self.input_min_marker = input_min_marker.GetValue()
            input_min_marker.Destroy()
            
            print(self.input_min_marker)
            
            input_max_marker = wx.TextEntryDialog(self, message="Provide MAX area for MARKER detection [in pixels]")
            input_max_marker.ShowModal()
            self.input_max_marker = input_max_marker.GetValue()
            input_max_marker.Destroy()
            
            print(self.input_max_marker)
            
            input_foci_size = wx.TextEntryDialog(self, message="Provide min area for foci detection [in pixels]")
            input_foci_size.ShowModal()
            self.input_foci_size = input_foci_size.GetValue()
            input_foci_size.Destroy()
            
            print(self.input_foci_size)
            
        except ValueError:
            st = wx.StaticText(self, label = "Missing fields", pos=(140, 85))
        
        self.list_nucleus_all_images = []
        list_file = []
        sorted_list_file = []
        
        name1 = 0
                       
        for file in glob.glob(self.relative_corrected_MARKER): 
            
            list_file.append(file)
            sorted_list_file = sorted(list_file) #file sorting based on number in file name, all number should have equal length (001 for 1)
            
        for s_file in sorted_list_file:
            
            read_file_DAPI = cv2.imread(s_file, 0)
            ret2, th2 = cv2.threshold(read_file_DAPI, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            
            try:
                (totalLabels, label_ids, values, centroid) = cv2.connectedComponentsWithStats(th2)
            except AttributeError: 
                 st = wx.StaticText(self, label = "check the file format [jpeg required]", pos=(140, 85))
                    
            list_single_nucleus = [] 

            for i in range(1, totalLabels):

                area_pixel = values[i, cv2.CC_STAT_AREA]               
                
                if area_pixel > float(self.input_min_marker) and area_pixel < float(self.input_max_marker):  #user's variables
                    name1 += 1 
                    
                    componentMask = (label_ids == i).astype("uint8") * 255 #future option: alert if empty set
                    
                    #cv2.imshow("Nucleus", componentMask)
                    #cv2.waitKey(200)
                    
                    cv2.imwrite(f"Results/Output_images_nucleus/Nucleus_{name1}.jpg", componentMask) 
                    
                    list_single_nucleus.append(componentMask)
            
            self.list_nucleus_all_images.append(list_single_nucleus)
            
        st = wx.StaticText(self, label = "Done!", pos=(140, 85))
        
        if st:
            button4 = wx.Button(self, label='Measure foci', pos=(5, 115), size=(110, 25))
            button4.Bind(wx.EVT_BUTTON, self.on_button4)
        else:
            print("Error")
        
        dict_param = {"pixel size" : float(self.my_pixel_size), 
                      "threshold" : float(self.input_threshold),
                      "min area MARKER" : float(self.input_min_marker),
                      "max area MARKER" : float(self.input_max_marker), 
                      "minimal foci size" : float(self.input_foci_size),
                     }
        
        parameters = pd.DataFrame.from_dict(dict_param, orient='index')
        parameters.to_csv(f'Results/Given_parameters.csv')
                      
        
    def on_button4(self, event):
        
        import cv2
        import glob  
        import numpy as np
        import matplotlib.pyplot as plt
        import math 
        import os
        import shutil
        #from PIL import Image, ImageDraw
               
        if round(float(self.my_pixel_size)) > 1 and round(float(self.my_pixel_size)) % 2 == 0:
            block_size = round(float(self.my_pixel_size)) + 1
        elif round(float(self.my_pixel_size)) == 1:
            block_size = round(float(self.my_pixel_size)) + 2
        elif round(float(self.my_pixel_size)) == 0:
            block_size = round(float(self.my_pixel_size)) + 3
        else: 
            block_size = round(float(self.my_pixel_size))
            
        list_file = []
        sorted_list_file = []
        paths_DNAdamage_tresholded = []
            
        for file in glob.glob(self.relative_corrected_FOCI):
            
            list_file.append(file)
            sorted_list_file = sorted(list_file)
            basename = os.path.basename(file)
            paths_DNAdamage_tresholded.append(f"DNAdamage_thresholded/{basename}")
                
        threshold = float(self.input_threshold)
            
        for s_file in sorted_list_file: # reads images, do treshold and save in new folder 
            
            read_file_DNAdamage = cv2.imread(s_file, 0)  
                                  
            ret1, th1 = cv2.threshold(read_file_DNAdamage, threshold, 255, cv2.THRESH_TOZERO)
            
            eq_th1 = cv2.equalizeHist(th1)         
                                          
            th3 = cv2.adaptiveThreshold(th1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 0) 
            
            basename_tresh = os.path.basename(s_file)
            cv2.imwrite(f"DNAdamage_thresholded/{basename_tresh}", th3)
                                                      
        self.number_foci_list_of_nucleus = [] 
        self.area_foci_list_of_nucleus = [] 
        
        name = 0

        for image in range(len(self.list_nucleus_all_images)): 
                                           
            for index in self.list_nucleus_all_images[image]:  
                
                name += 1   
                  
                read_file_DNAdamage = cv2.imread(paths_DNAdamage_tresholded[image], 0) 
                
                masked_img = cv2.bitwise_and(read_file_DNAdamage, read_file_DNAdamage, mask = index) 
                                                                     
                (totalLabelsMasked, label_idsMasked, valuesMasked, centroidMasked) = cv2.connectedComponentsWithStats(masked_img, connectivity=8, ltype=2)  
                
                number_foci = totalLabelsMasked - 1 #background subtraction
                
                area_foci = []
                    
                for i in range(1, totalLabelsMasked): 
                    
                    area = valuesMasked[i, cv2.CC_STAT_AREA]  
                        
                    if area >= float(self.input_foci_size): #user's varable
                        
                        area_foci.append(area) #saves only foci above declared number of pixels 
                        
                    else:
                        area_foci.append(0)
                        number_foci -= 1  
                                  
                label_hue = np.uint8(179*label_idsMasked/np.max(label_idsMasked))
                blank_ch = 255*np.ones_like(label_hue)
                labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
                
                labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
                
                labeled_img[label_hue==0] = 0   
                        
                #cv2.imshow("DNA damage foci", labeled_img)
                #cv2.waitKey(200)
                #cv2.destroyAllWindows()
                
                cv2.imwrite(f"Results/Output_images_DNAdamage/DNA_damage_{name}.jpg", labeled_img) # creates folder and saves masked images              
                area_sum = sum(area_foci) 

                self.area_foci_list_of_nucleus.append(area_sum)
                self.number_foci_list_of_nucleus.append(number_foci) 
                                        
        st = wx.StaticText(self, label = "Done! Save results!", pos=(140, 120))
        
        if st:
            button5 = wx.Button(self, label='Save results', pos=(5, 150), size=(110, 25))
            button5.Bind(wx.EVT_BUTTON, self.on_button5)
        else:
            print("Error")
        
        path_DNAdamage_thresholded = "DNAdamage_thresholded" # removes folder with tresh. images if not needed anymore
        shutil.rmtree(path_DNAdamage_thresholded, ignore_errors=True)
        
    def on_button5(self, event):
        
        import pandas as pd
        import os
        
        input_name_folder = wx.TextEntryDialog(self, message="Provide unique name for output folder [other than \"Results\"]")
        input_name_folder.ShowModal()
        my_name_folder = input_name_folder.GetValue()
        
        results = zip(self.number_foci_list_of_nucleus, self.area_foci_list_of_nucleus)
        results_df = pd.DataFrame(results, columns=["Foci Number", "Foci Total Area"])
        results_df.to_csv(f'Results/Quantification.csv') #saves results in results folder
        os.rename("Results", f"{my_name_folder}")
        
        st1 = wx.StaticText(self, label = "Saved! Analysis completed!", pos=(140, 155))

class MyFrame(wx.Frame):
    
    def __init__(self):
        super().__init__(None, title='SimplySmart v.1', size=(450,225)) 
        panel = MyPanel(self)
        self.Show()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    frame.Show()
    frame.SetIcon(wx.Icon("icon.png")) 
    app.MainLoop()