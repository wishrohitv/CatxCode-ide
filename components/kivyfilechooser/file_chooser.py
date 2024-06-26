from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from app_storage_implement.app_storage import storage_path

Builder.load_string("""                                   
<ModalFileChooser>:
    id: file_chooser_popup
    BoxLayout:
        canvas.before:
            Color:
                rgba: 60/255, 48/255, 72/255, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [6,]
        canvas.after:
            Color:
                rgba: 99/255, 166/255, 242/255, 0.327
            Line:
                width: 2
                rounded_rectangle: (self.x, self.y, self.width, self.height, 6)
                    
        orientation: "vertical"
        # header
        BoxLayout:
            size_hint: (1, None)
            height: "40dp"
            padding: "8dp","4dp","4dp",0
            Label:
                text: "Explorer"
                halign: "left"
                valign: "middle"
                text_size: self.size
                # on_touch_down: print(file_chooser_popup.pos)
                # on_touch_move:print(file_chooser_popup.pos) #file_chooser_popup.pos = self.pos
            Button:
                #:set full False
                text: '◻' if not full else '▫'
                font_name: "./assets/fonts/seguiemj.ttf"
                size_hint: (None, 1)
                width: "60dp"
                background_color: "gray"
                background_nomal: ""
                on_press: 
                    # print(full)
                    file_chooser_popup.size_hint = (1,1) if not full else (.8,.8)
                    full = True if not full else False
            Button:
                text: 'X'
                on_press: root.close()
                size_hint: (None, 1)
                width: "60dp"
                background_color: "red"
                background_nomal: ""
                    
            
        FileChooser:
            id: fc
            rootpath: root.root_path
            #on_selection: app.selected_files(fc.selection)
            FileChooserIconLayout:
                
            FileChooserListLayout:

        BoxLayout:
            padding: "4dp",0,"4dp","4dp"
            size_hint: (1, None)
            height: "40dp"

            ToggleButton:
                text: "List View"
                group: "view"
                on_release: fc.view_mode = "list"
                size_hint: (.5,1)

            ToggleButton:
                text: "Icon View"
                state: "down"
                group: "view"
                on_release: fc.view_mode = "icon"
                size_hint: (.5,1)
                        
            Button:
                text: "Ok"
                size_hint: (.5,1)
                on_press: 
                    fc.on_selection = app.selected_files(fc.selection)
                    root.close()
""")


class ModalFileChooser(ModalView):
    root_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.8,.8)
        if platform == "win":
            # self.root_path = "C:/Users/user/Downloads"
            self.root_path = storage_path
        elif platform == "android":
            # self.root_path = "/storage/emulated/0/"
            self.root_path = storage_path
        elif platform == "linux":
            self.root_path = "/home/"

    def close(self):
        self.dismiss()

    

