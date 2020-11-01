import bpy


class Macros(Init):
    '''
    Custom scripts with assigned hotkeys.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''
        '''


    def setMacros(self, macros=[]):
        '''
        Extends setMacro to accept a list of tuples.
        '''
        if not macros:
            macros = [
                ('hk_back_face_culling', '1', 'Display', 'Toggle back-face culling.'),
                ('hk_smooth_preview', '2', 'Display', 'Toggle smooth mesh preview.'),
                ('hk_isolate_selected', 'F2', 'Display', 'Isolate current selection.'),
                ('hk_grid_and_image_planes', 'F1', 'Display', 'Toggle grid and image plane visibility.'),
                ('hk_frame_selected', 'f', 'Display', 'Frame selected by a set amount.'),
                ('hk_wireframe_on_shaded', '3', 'Display', 'Toggle wireframe on shaded.'),
                ('hk_xray', 'F3', 'Display', 'Toggle xRay all.'),
                ('hk_wireframe', '5', 'Display', 'Toggle wireframe/shaded/shaded w/texture display.'),
                ('hk_shading', '6', 'Display', 'Toggle viewport shading.'),
                ('hk_selection_mode', 'sht+q', 'Edit', 'Toggle between object selection & last component selection.'),
                ('hk_paste_and_rename', 'ctl+v', 'Edit', 'Paste and rename removing keyword \'paste\'.'),
                ('hk_multi_component', 'F5', 'Edit', 'Multi-Component Selection.'),
                ('hk_toggle_component_mask', 'F4', 'Edit', 'Toggle Component Selection Mask.'),
                ('hk_tk_show', 'F12', 'UI', 'Display tk marking menu.'),
                ('hk_hotbox_full', 'sht+z', 'UI', 'Display the full version of the hotbox.'),
                ('hk_toggle_panels', '9', 'UI', 'Toggle UI toolbars.'),
                ('hk_toggle_UV_select_type', 'sht+t', 'Edit', 'Toggle UV / UV shell component selection.'),
                ('hk_merge_vertices', 'ctl+m', 'Edit', 'Merge vertices on selection.'),
            ]

        for m in macros:
            self.setMacro(*m)


    def setMacro(self, name=None, k=None, cat=None, ann=None):
        '''
        Sets a default runtime command with a keyboard shotcut.

        args:
            name (str) = The command name you provide must be unique. The name itself must begin with an alphabetic character or underscore followed by alphanumeric characters or underscores.
            cat (str) = catagory - Category for the command.
            ann (str) = annotation - Description of the command.
            k (str) = keyShortcut - Specify what key is being set.
                        key modifier values are set by adding a '+' between chars. ie. 'sht+z'.
                        modifiers:
                            alt, ctl, sht
                        additional valid keywords are:
                            Up, Down, Right, Left,
                            Home, End, Page_Up, Page_Down, Insert
                            Return, Space
                            F1 to F12
                            Tab (Will only work when modifiers are specified)
                            Delete, Backspace (Will only work when modifiers are specified)
        '''
        command = self.formatSource(name, removeTabs=2)

        #set runTimeCommand
        pm.runTimeCommand(
                name,
                annotation=ann,
                category=cat,
                command=command,
                default=True,
        )

        #set command
        nameCommand = pm.nameCommand(
                '{0}Command'.format(name),
                annotation=ann,
                command=name,
        )

        #set hotkey
        #modifiers
        ctl=False; alt=False; sht=False
        for char in k.split('+'):
            if char=='ctl':
                ctl = True
            elif char=='alt':
                alt = True
            elif char=='sht':
                sht = True
            else:
                key = char

        # print(name, char, ctl, alt, sht)
        pm.hotkey(keyShortcut=key, name=nameCommand, ctl=ctl, alt=alt, sht=sht) #set only the key press.


    def formatSource(self, cmd, removeTabs=0):
        '''
        Return the text of the source code for an object.
        The source code is returned as a single string.
        Removes lines containing '@' or 'def ' ie. @staticmethod.

        args:
            cmd = module, class, method, function, traceback, frame, or code object.
            removeTabs (int) = remove x instances of '\t' from each line.

        returns:
            A Multi-line string.
        '''
        from inspect import getsource
        source = getsource(getattr(Macros, cmd))

        l = [s.replace('\t', '', removeTabs) for s in source.split('\n') if s and not '@' in s and not 'def ' in s]
        return '\n'.join(l)



addon_keymaps=[]

def register():
    bpy.utils.register_class(Macros)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='hk_', space_type='hk_') #(name, space_type='EMPTY', region_type='WINDOW', modal=False) #Returns the Added key map.
        kmi = km.keymap_items.new('', type='', value='PRESS', shift=True) #(idname, type, value, any=False, shift=False, ctrl=False, alt=False, oskey=False, key_modifier='NONE', repeat=True, head=False) #Returns the added key map item.

        addon_keymaps.append((km, kmi))
        
        
        
def unregister():
    for km, kmi in addon_keymaps:
        km.kwyaps_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(Macros)



    # Display --------------------------------------------------------------------------------------------------------------------------------


    # Edit -----------------------------------------------------------------------------------------------------------------------------------


    # Selection ------------------------------------------------------------------------------------------------------------------------------


    # UI -------------------------------------------------------------------------------------------------------------------------------------








# -----------------------------------------------
# Notes
# -----------------------------------------------

'''
NONE Undocumented.

LEFTMOUSE Left Mouse, LMB.
MIDDLEMOUSE Middle Mouse, MMB.
RIGHTMOUSE Right Mouse, RMB.

BUTTON4MOUSE Button4 Mouse, MB4.
BUTTON5MOUSE Button5 Mouse, MB5.
BUTTON6MOUSE Button6 Mouse, MB6.
BUTTON7MOUSE Button7 Mouse, MB7.

PEN Pen.

ERASER Eraser.

MOUSEMOVE Mouse Move, MsMov.
INBETWEEN_MOUSEMOVE In-between Move, MsSubMov.

TRACKPADPAN Mouse/Trackpad Pan, MsPan.
TRACKPADZOOM Mouse/Trackpad Zoom, MsZoom.

MOUSEROTATE Mouse/Trackpad Rotate, MsRot.
MOUSESMARTZOOM Mouse/Trackpad Smart Zoom, MsSmartZoom.

WHEELUPMOUSE Wheel Up, WhUp.
WHEELDOWNMOUSE Wheel Down, WhDown.
WHEELINMOUSE Wheel In, WhIn.
WHEELOUTMOUSE Wheel Out, WhOut.

EVT_TWEAK_L Tweak Left, TwkL.
EVT_TWEAK_M Tweak Middle, TwkM.
EVT_TWEAK_R Tweak Right, TwkR.

ZERO 0.
ONE 1.
TWO 2.
THREE 3.
FOUR 4.
FIVE 5.
SIX 6.
SEVEN 7.
EIGHT 8.
NINE 9.

LEFT_CTRL Left Ctrl, CtrlL.
LEFT_ALT Left Alt, AltL.
LEFT_SHIFT Left Shift, ShiftL.
RIGHT_ALT Right Alt, AltR.
RIGHT_CTRL Right Ctrl, CtrlR.
RIGHT_SHIFT Right Shift, ShiftR.

OSKEY OS Key, Cmd.

APP Application, App.

GRLESS Grless.

ESC Esc.

TAB Tab.

RET Return, Enter.

SPACE Spacebar, Space.

LINE_FEED Line Feed.

BACK_SPACE Backspace, BkSpace.

DEL Delete, Del.

SEMI_COLON ;.

PERIOD ..

COMMA ,.

QUOTE “.

ACCENT_GRAVE `.

MINUS -.

PLUS +.

SLASH /.

BACK_SLASH \.

EQUAL =.

LEFT_BRACKET [.
RIGHT_BRACKET ].

LEFT_ARROW Left Arrow, ←.
DOWN_ARROW Down Arrow, ↓.
RIGHT_ARROW Right Arrow, →.
UP_ARROW Up Arrow, ↑.

NUMPAD_2 Numpad 2, Pad2.
NUMPAD_4 Numpad 4, Pad4.
NUMPAD_6 Numpad 6, Pad6.
NUMPAD_8 Numpad 8, Pad8.
NUMPAD_1 Numpad 1, Pad1.
NUMPAD_3 Numpad 3, Pad3.
NUMPAD_5 Numpad 5, Pad5.
NUMPAD_7 Numpad 7, Pad7.
NUMPAD_9 Numpad 9, Pad9.

NUMPAD_PERIOD Numpad ., Pad..
NUMPAD_SLASH Numpad /, Pad/.
NUMPAD_ASTERIX Numpad *, Pad*.
NUMPAD_0 Numpad 0, Pad0.
NUMPAD_MINUS Numpad -, Pad-.
NUMPAD_ENTER Numpad Enter, PadEnter.
NUMPAD_PLUS Numpad +, Pad+.

F1 F1.
F2 F2.
F3 F3.
F4 F4.
F5 F5.
F6 F6.
F7 F7.
F8 F8.
F9 F9.
F10 F10.
F11 F11.
F12 F12.
F13 F13.
F14 F14.
F15 F15.
F16 F16.
F17 F17.
F18 F18.
F19 F19.
F20 F20.
F21 F21.
F22 F22.
F23 F23.
F24 F24.

PAUSE Pause.

INSERT Insert, Ins.

HOME Home.

PAGE_UP Page Up, PgUp.
PAGE_DOWN Page Down, PgDown.

END End.

MEDIA_PLAY Media Play/Pause, >/||.
MEDIA_STOP Media Stop, Stop.
MEDIA_FIRST Media First, |<<.
MEDIA_LAST Media Last, >>|.

TEXTINPUT Text Input, TxtIn.

WINDOW_DEACTIVATE Window Deactivate.

TIMER Timer, Tmr.
TIMER0 Timer 0, Tmr0.
TIMER1 Timer 1, Tmr1.
TIMER2 Timer 2, Tmr2.

TIMER_JOBS Timer Jobs, TmrJob.

TIMER_AUTOSAVE Timer Autosave, TmrSave.
TIMER_REPORT Timer Report, TmrReport.
TIMERREGION Timer Region, TmrReg.

NDOF_MOTION NDOF Motion, NdofMov.
NDOF_BUTTON_MENU NDOF Menu, NdofMenu.
NDOF_BUTTON_FIT NDOF Fit, NdofFit.
NDOF_BUTTON_TOP NDOF Top, Ndof↑.
NDOF_BUTTON_BOTTOM NDOF Bottom, Ndof↓.
NDOF_BUTTON_LEFT NDOF Left, Ndof←.
NDOF_BUTTON_RIGHT NDOF Right, Ndof→.
NDOF_BUTTON_FRONT NDOF Front, NdofFront.
NDOF_BUTTON_BACK NDOF Back, NdofBack.
NDOF_BUTTON_ISO1 NDOF Isometric 1, NdofIso1.
NDOF_BUTTON_ISO2 NDOF Isometric 2, NdofIso2.
NDOF_BUTTON_ROLL_CW NDOF Roll CW, NdofRCW.
NDOF_BUTTON_ROLL_CCW NDOF Roll CCW, NdofRCCW.
NDOF_BUTTON_SPIN_CW NDOF Spin CW, NdofSCW.
NDOF_BUTTON_SPIN_CCW NDOF Spin CCW, NdofSCCW.
NDOF_BUTTON_TILT_CW NDOF Tilt CW, NdofTCW.
NDOF_BUTTON_TILT_CCW NDOF Tilt CCW, NdofTCCW.
NDOF_BUTTON_ROTATE NDOF Rotate, NdofRot.
NDOF_BUTTON_PANZOOM NDOF Pan/Zoom, NdofPanZoom.
NDOF_BUTTON_DOMINANT NDOF Dominant, NdofDom.
NDOF_BUTTON_PLUS NDOF Plus, Ndof+.
NDOF_BUTTON_MINUS NDOF Minus, Ndof-.
NDOF_BUTTON_ESC NDOF Esc, NdofEsc.
NDOF_BUTTON_ALT NDOF Alt, NdofAlt.
NDOF_BUTTON_SHIFT NDOF Shift, NdofShift.
NDOF_BUTTON_CTRL NDOF Ctrl, NdofCtrl.
NDOF_BUTTON_1 NDOF Button 1, NdofB1.
NDOF_BUTTON_2 NDOF Button 2, NdofB2.
NDOF_BUTTON_3 NDOF Button 3, NdofB3.
NDOF_BUTTON_4 NDOF Button 4, NdofB4.
NDOF_BUTTON_5 NDOF Button 5, NdofB5.
NDOF_BUTTON_6 NDOF Button 6, NdofB6.
NDOF_BUTTON_7 NDOF Button 7, NdofB7.
NDOF_BUTTON_8 NDOF Button 8, NdofB8.
NDOF_BUTTON_9 NDOF Button 9, NdofB9.
NDOF_BUTTON_10 NDOF Button 10, NdofB10.
NDOF_BUTTON_A NDOF Button A, NdofBA.
NDOF_BUTTON_B NDOF Button B, NdofBB.
NDOF_BUTTON_C NDOF Button C, NdofBC.

ACTIONZONE_AREA ActionZone Area, AZone Area.
ACTIONZONE_REGION ActionZone Region, AZone Region.
ACTIONZONE_FULLSCREEN ActionZone Fullscreen, AZone FullScr.

value (enum in ['ANY', 'PRESS', 'RELEASE', 'CLICK', 'DOUBLE_CLICK', 'CLICK_DRAG', 'NORTH', 'NORTH_EAST', 'EAST', 'SOUTH_EAST', 'SOUTH', 'SOUTH_WEST', 'WEST', 'NORTH_WEST', 'NOTHING']) – Value

any (boolean, (optional)) – Any

shift (boolean, (optional)) – Shift

ctrl (boolean, (optional)) – Ctrl

alt (boolean, (optional)) – Alt

oskey (boolean, (optional)) – OS Key
'''