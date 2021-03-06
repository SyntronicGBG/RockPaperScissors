from tkinter import Tk, ttk, StringVar
from data_collector import DataCollector
from os import startfile

class DataCollectionGUI:
    def __init__(self, root):
        self.dc = DataCollector()

        # configure the root Tk window
        root.title('Data Collection')
        root.minsize(640,150)
        root.resizeable=(False,False)
        root.configure(background='#e1d8b9')

        # set all styles for the different ttk object types
        style = ttk.Style()
        style.configure('TFrame', background='#e1d8b9', font=('Arial',11))
        style.configure('TLabel', background='#e1d8b9', font=('Arial',11))
        style.configure('Header.TLabel', font=('Arial',18,'bold'))
        style.configure('TButton', background='#e1d8b9', font=('Arial',11))
        style.configure('TCombobox', background='#e1d8b9', font=('Arial',11))
        style.configure('TRadiobutton', background='#e1d8b9', font=('Arial',11))
        style.configure('Message.TLabel', background='#e1d8b9', font=('Arial',10))

        # set up a frame for the title and short description of how to play
        self.frame_header = ttk.Frame(root)
        self.frame_header.pack()
        ttk.Label(self.frame_header, text='Rock Paper Scissors Data Collection',style='Header.TLabel').pack()
        ttk.Label(self.frame_header, text='Set your meta data, press record, play and then either save or clear').pack()

        # set up a frame for all meta data
        self.frame_meta = ttk.Frame(root)
        self.frame_meta.pack()
        
        # add radiobuttons for each of the three end results
        self.result = StringVar(None, 'Rock')
        ttk.Radiobutton(self.frame_meta, text='Rock', variable=self.result, value='Rock').grid(row=0,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Paper', variable=self.result, value='Paper').grid(row=1,column=0, sticky='w')
        ttk.Radiobutton(self.frame_meta, text='Scissors', variable=self.result, value='Scissors').grid(row=2,column=0, sticky='w')
        
        # add labels for each meta data column
        ttk.Label(self.frame_meta,text='Name:').grid(row=0,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Angle:').grid(row=1,column=1,sticky='e',padx=5)
        ttk.Label(self.frame_meta,text='Hand:').grid(row=2,column=1,sticky='e',padx=5)

        # set the entry name
        self.name = StringVar()
        self.entry_name = ttk.Entry(self.frame_meta, textvariable=self.name)
        self.entry_name.grid(row=0,column=2,sticky='w')

        # set the combobox for the angle of the hand toward the camera
        self.angle_of_hand = StringVar(None,'Outside')
        self.angle = ttk.Combobox(self.frame_meta, textvariable=self.angle_of_hand,
                                  values=('Inside','Frontal','Outside'))
        self.angle.grid(row=1,column=2,sticky='w')

        # set the combobox for which hand is used
        self.l_r_hand = StringVar(None,'Right')
        self.hand = ttk.Combobox(self.frame_meta, textvariable=self.l_r_hand,
                                 values=('Left','Right'))
        self.hand.grid(row=2, column=2,sticky='w')
        
        # set up a frame for the recording actions
        self.frame_record = ttk.Frame(root)
        self.frame_record.pack()

        # set up the button for recording and saving
        self.button_record_save = ttk.Button(self.frame_record,text='Record',command=self.record)
        self.button_record_save.grid(row=0,column=2,sticky='e',padx=10)

        # show video button
        self.button_show = ttk.Button(self.frame_record,text='Show',command=self.show)
        
        # clear button
        self.button_clear = ttk.Button(self.frame_record,text='Clear',command=self.clear)

        # set up message of recording status
        self.status = StringVar()
        self.label_record = ttk.Label(self.frame_record,style='Message.TLabel', textvariable=self.status)
        self.label_record.grid(row=0,column=3,sticky='w')

        # init meta_data
        self.meta_data = {}

    def close(self):
        """Stop all background processes
        """
        self.dc.close()

    def record(self):
        """Record a video
        """
        self.button_record_save.state(['disabled'])
        if not self.name.get():
            self.status.set('Must enter a name of the player')
            self.label_record.configure(foreground='red')
        else:
            self.reset_meta_data()
            try:
                # record the video
                self.dc.record_video(self.meta_data)
                # change button to save
                self.button_record_save.configure(text='Save', command=self.save)
                self.button_show.grid(row=0,column=4,sticky='e',padx=10)
                self.button_clear.grid(row=0,column=5,sticky='e',padx=10)
                # let the user know recording was successful
                self.status.set('Recording successful!')
                self.label_record.configure(foreground='green')
            except Exception as e:
                print(e)
                # let the user know something went wrong
                self.status.set('Recording unsuccessful!')
                self.label_record.configure(foreground='red')
        self.button_record_save.state(['!disabled'])
    
    def save(self):
        """Save recorded video
        """
        self.button_record_save.state(['disabled'])
        try:
            # save the video
            self.dc.transfer_video(self.meta_data)
            # change button to save
            self.button_record_save.configure(text='Record', command=self.record)
            self.button_show.grid_forget()
            self.button_clear.grid_forget()
            # let the user know it was successful
            self.status.set('Saving successful!')
            self.label_record.configure(foreground='green')
        except Exception as e:
            print(e)
            # let the user know something went wrong
            self.status.set('Saving unsuccessful!')
            self.label_record.configure(foreground='red')
        self.button_record_save.state(['!disabled'])
    
    def show(self):
        """Show latest recording
        """
        startfile(self.meta_data['movie_file_path'])

    def clear(self):
        """Clear recording
        """
        self.dc.remove_video(self.meta_data)
        self.reset_meta_data()
        self.button_record_save.configure(text='Record', command=self.record)
        self.button_show.grid_forget()
        self.button_clear.grid_forget()
        self.status.set('Removed recording')
        self.label_record.configure(foreground='green')

    def reset_meta_data(self):
        """Reset meta data settings
        """
        self.meta_data = {
                'hand_sign': self.result.get(),
                'left_or_right_hand': self.hand.get(),
                'photo_model': self.entry_name.get(),
                'angle': self.angle.get(),
                'movie_file_path': 'basicvideo.mp4',
                'fps': 30,
                'number_frames': 30*2,
                }

def main():
    root = Tk()
    dcg = DataCollectionGUI(root)
    root.mainloop()
    dcg.close()

if __name__ == '__main__':
    main()