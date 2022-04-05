class UIBaseStyle():
    def __init__(self):
        self.btn_style1 = '''
                         QPushButton
                         {background-color : #FFEBCD;
                         font: bold;
                         border-color: #F4A460;
                         border-width: 3px;
                         border-radius: 5px;
                         padding: 4px;
                         border-style: outset;}
                         QPushButton:pressed
                         {text-align : center;
                         background-color : light gray;
                         font: bold;
                         border-color: gray;
                         border-width: 2px;
                         border-radius: 10px;
                         padding: 6px;
                         height : 14px;
                         border-style: outset;}
                         '''
        self.btn_style2 = '''
                         QPushButton
                         {background-color : #F0FFFF;
                         font: bold;
                         border-color: #1E90FF;
                         border-width: 2px;
                         border-radius: 5px;
                         padding: 6px;
                         border-style: outset;}
                         QPushButton:pressed
                         {text-align : center;
                         background-color : light gray;
                         font: bold;
                         border-color: gray;
                         border-width: 2px;
                         border-radius: 10px;
                         padding: 6px;
                         height : 14px;
                         border-style: outset;}
                         '''
        self.label_style1 = '''
                             background-color : #E1FFFF;
                             font: bold;
                             color: #888888;
                             border-color: #999999;
                             border-width: 1px;
                             padding: 6px;
                             border-style: outset;
                            '''
        self.label_style2 = '''
                                background-color: #FFE4E1;
                                border-width: 1px;
                                color: #888888;
                                border-color: #999999;
                                border-style: outset;
                                font: bold;
                                padding: 6px;
                                '''
        self.label_style3 = '''
                                background-color: #F0FFF0;
                                border-width: 1px;
                                color: #888888;
                                border-color: #999999;
                                border-style: outset;
                                font: bold;
                                padding: 6px;
                                '''
        self.label_style4 = '''
                                background-color: #FAFAD2;
                                border-width: 1px;
                                color: #888888;
                                border-color: #999999;
                                border-style: outset;
                                font: bold;
                                padding: 6px;
                                '''
        self.label_style5 = '''
                                background-color: #EEEEEE;
                                border-width: 1px;
                                color: #888888;
                                border-color: #999999;
                                border-style: outset;
                                font: bold;
                                padding: 6px;
                                '''
        self.checkbox_style = '''
                                background-color: #EEEEEE;
                                border-width: 1px;
                                border-color: #999999;
                                border-style: outset;
                                border-radius: 10px;
                                font: bold;
                                padding: 6px;
                                '''
        self.editline_style = '''
                                background-color: white;
                                border-width: 1px;
                                border-color: #222222;
                                border-style: outset;
                                border-radius: 3px;
                                font: bold;
                                padding: 6px;
                                '''

        self.about_style = '''
                         background-color: white;
                         border-width: 1px;
                         border-color: #222222;
                         border-style: outset;
                         border-radius: 3px;
                         font: bold;
                         font-style: italic;
                         padding: 6px;
                        '''