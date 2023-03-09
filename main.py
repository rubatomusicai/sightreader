from kivy.properties import StringProperty, ColorProperty
from kivy.factory import Factory
import asynckivy as ak
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy_garden.draggable import KXDroppableBehavior, KXDraggableBehavior
from kivymd.uix.snackbar import Snackbar
import time
from kivymd.app import MDApp
from kivy.metrics import dp

import random
import itertools
import SightReaderQuizModule

from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from random import randrange
from sightreader_levels import tcL0_note_img_map, bcL0_note_img_map, both_clef_L0_note_img_map,both_clef_L1_note_img_map,tcL1_note_img_map,bcL1_note_img_map


drag_all_questions_success_num = 0
drag_questions_repetition = 0  # used to just have a count of number of times the game is played in one session.


def play_sound(filename, file_format='.wav', button_code='wrong'):
    sound = SoundLoader.load('sounds/' + filename + file_format)
    sound.play()


class MenuScreen(Screen):
    pass


class SightReaderScreen(Screen):
    pass


class SightReaderDragDrop(MDGridLayout):

    def runDragDropSightReader(self, note_map):
        global drag_questions_repetition
        drag_questions_repetition = drag_questions_repetition+1
        all_notes = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
        note_class_set = set()
        add_widget = sr.ids.where_the_items_initially_live.add_widget
        window_sizes = Window.size
        items = set()

        # Try to add elem to set until set length is less than 10
        i = 0
        for i in itertools.takewhile(lambda x: len(items) < 4, gen):
            x = int(randrange(note_map.__len__()))
            if x not in items:
                items.add(x)
                # print(items)
                current_note = note_map[x]
                # print(current_note)
                note_class_set.add(current_note[0])
                item = DraggableButton(color_cls=current_note[0], )
                item.background_normal = 'images/' + current_note + '.png'
                item.icon = 'images/' + current_note + '.png'
                item.size_hint = (1, None)
                item.pos_hint = {'right': 1, 'center_y': 0.8}
                #item.size = (window_sizes[0], 200)
                # print(item)
                # print("Before adding widget-" + str(len(sr.ids.where_the_items_initially_live.children)))
                add_widget(item)

        font_size = str(int(window_sizes[0] / 10))
        other_notes = all_notes.difference(note_class_set)
        note_class_list = list(note_class_set)
        other_notes_list = list(other_notes)
        result = note_class_set.copy()
        if len(note_class_set) < 4:
            result.update(other_notes_list[:4 - len(note_class_set)])

        note_class_list = list(result)

        sr.ids.box_1.color_cls = note_class_list[0]
        sr.ids.box_1.text = note_class_list[0]
        sr.ids.box_2.color_cls = note_class_list[1]
        sr.ids.box_2.text = note_class_list[1]
        sr.ids.box_3.color_cls = note_class_list[2]
        sr.ids.box_3.text = note_class_list[2]
        sr.ids.box_4.color_cls = note_class_list[3]
        sr.ids.box_4.text = note_class_list[3]

        # Remove the dropable box if we have only 3 or 2 in our note set. This can happen when we have 2 of the same notes like C4 and C3 and so on.
        # if (len(note_class_list) == 3):
        # print("note_class_len=" + str(len(note_class_list)))
        # sr.ids.dropable_layout.remove_widget(sr.ids.box_4)
        # sr.ids.box_4.opacity = 0
        # if (len(note_class_list) == 2):
        # print("note_class_len=" + str(len(note_class_list)))
        # sr.ids.dropable_layout.remove_widget(sr.ids.box_4)
        # sr.ids.dropable_layout.remove_widget(sr.ids.box_3)
        # sr.ids.box_4.opacity = 0
        # sr.ids.box_3.opacity = 0

        sr.ids.box_1.font_size = dp(font_size)
        sr.ids.box_2.font_size = dp(font_size)
        sr.ids.box_3.font_size = dp(font_size)
        sr.ids.box_4.font_size = dp(font_size)

    def startDragDropSightReader(self, l, treble_clef, bass_clef, mode):
        # print(sr.ids)
        if treble_clef and bass_clef:
            if l == 1:
                self.runDragDropSightReader(both_clef_L0_note_img_map)
            elif l == 2:
                self.runDragDropSightReader(both_clef_L1_note_img_map)
            else:
                pass
        elif treble_clef:
            if l == 1:
                self.runDragDropSightReader(tcL0_note_img_map)
            elif l == 2:
                self.runDragDropSightReader(tcL1_note_img_map)
            else:
                pass
        else:
            if l == 1:
                self.runDragDropSightReader(bcL0_note_img_map)
            elif l == 2:
                self.runDragDropSightReader(bcL1_note_img_map)
            else:
                pass

    def remove_all(self, instance):
        for child in self.children:
            self.remove_widget(child)


class DraggableButton(KXDraggableBehavior, Factory.MDIconButton, Factory.MDTooltip):
    color_cls = StringProperty()

    def on_drag_fail(self, touch):
        ctx = self.drag_context
        if ctx.droppable is not None:
            # print(f"Incorrect! {self.text} is not {ctx.droppable.color_cls}")
            #Snackbar(text=f"Incorrect that's not {ctx.droppable.color_cls}, try again.", bg_color=(1, 0, 0, 0.3),duration=0.3).open()
            play_sound("wrong")
            time.sleep(0.5)
        return super().on_drag_fail(touch)

    async def on_drag_success(self, touch):
        # print("Correct")
        global drag_questions_repetition
        global drag_all_questions_success_num
        drag_all_questions_success_num = drag_all_questions_success_num + 1
        self.center = self.to_window(*self.drag_context.droppable.center)
        # Snackbar(bg_color=(1,1,1, 0.3), _fading_out=True ,opacity=0.98,duration = 0.3, background='images/correct.png',size_hint_max_x="70dp", widget_style="ios",ripple_color=(1,1,1, 0.8),snackbar_x=Window.width/2-50,snackbar_y=250).open()
        # Snackbar(text="Correct!!!.", bg_color=(0, 0.7, 0.8, 0.4), duration=0.2).open()
        #ran = random.randint(0, 3)
        ran = drag_questions_repetition % 3 #changing from playing sounds at random to having one sound for each repitition using modulus operation.
        if drag_all_questions_success_num >= 4:
            play_sound("task-success")
        elif ran == 0:
            play_sound("congrats")
        elif ran == 2:
            play_sound("short-success-sound", file_format=".mp3")
        else:
            play_sound("success_bell")
        time.sleep(1)
        await ak.animate(self, opacity=0, d=.5)
        self.parent.remove_widget(self)
        # print(drag_all_questions_success_num)
        if drag_all_questions_success_num >= 4:
            # print("Al correct restart")
            SightReaderDragDrop().runDragDropSightReader(both_clef_L0_note_img_map)
            drag_all_questions_success_num = 0


class DroppableArea(KXDroppableBehavior, Factory.MDRectangleFlatButton):
    line_color = ColorProperty()
    color_cls = StringProperty()

    def accepts_drag(self, touch, draggable):
        return draggable.color_cls == self.color_cls


def random_gen(low, high):
    while True:
        yield random.randrange(low, high)


gen = random_gen(1, 10)


class MenuLayout(GridLayout):
    pass


class MenuItems(GridLayout):

    def start_dragdrop_sightreader(self, l, treble_clef, bass_clef, mode):
        # print(self.ids)

        sr1 = SightReaderDragDrop().startDragDropSightReader(l, treble_clef, bass_clef, mode)

    def start_sight_reader_quiz(self, l, treble_clef, bass_clef, mode):
        #print(self.ids)

        srq = SightReaderQuizModule.SightReaderQuiz.start_sight_reader(l=l, treble_clef=treble_clef,
                                                                       bass_clef=bass_clef, mode=mode)


class ClefSelectionSwitchTreble(MDGridLayout):
    pass


class ClefSelection(MDGridLayout):
    pass


sr = None


class SightReaderApp(MDApp):
    root = None

    def build(self):
        root = Builder.load_file("app.kv")
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "BlueGray"
        self.theme_cls.accent_hue = "A200"
        self.theme_cls.accent_light_hue = "50"
        self.theme_cls.accent_dark_hue = "100"
        # self.theme_cls.

        window_sizes = Window.size
        #print('window_sizes=' + str(window_sizes))
        # root = Builder.load_string(KV_CODE)

        self.icon = 'images/icons8-48.png'
        # global sm
        # transition=WipeTransition()
        # sm = ScreenManager(transition=RiseInTransition())
        # sm.add_widget(MenuScreen(name='menu'))
        # sm.add_widget(SightReaderScreen(name='sightreader'))

        # return sm
        # print(root.ids)
        return root

        # root = Builder.load_file('menu.kv')
        # return MenuLayout()

    def on_start(self):
        global sr
        sr = self.root.ids.sightreader
        # print(sr.ids)
        # print(self.root.get_screen('menu').ids)

    global sr

    def delete_widget(self):
        global drag_all_questions_success_num
        try:
            # self.root.ids.sightreader.remove_widget(self.root.ids.sightreader.ids.where_the_items_initially_live)
            # print("where children-live going to delete-" + str(
            # len(self.root.ids.sightreader.ids.where_the_items_initially_live.children)))
            grid = self.root.ids.sightreader.ids.where_the_items_initially_live
            grid.clear_widgets()
            drag_all_questions_success_num = 0
            # ("where children-live after delete-" + str(
            # len(self.root.ids.sightreader.ids.where_the_items_initially_live.children)))
        except:
            print("Widget may not be there- so cannot delete.")

    def home_callback(self, x):
        # print(self.root.ids.sightreader.ids)
        # print(len(self.root.ids.sightreader.children))
        self.delete_widget()
        # print(self.root.ids.sightreader.ids.where_the_items_initially_live)
        # arg x is currently not used.
        self.root.current = 'menu'


if __name__ == '__main__':
    #Window.size = (1536,1904)
    SightReaderApp().run()
