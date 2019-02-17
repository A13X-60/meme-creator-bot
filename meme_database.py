# 'Areas' variable is a dict structured like this:
#                   {(width_of_the_area, height_of_the_area): (x_of_the_left_top_corner, y_of_the_left_top_corner), ...}


class Meme:
    def __init__(self, areas, font_name, font_colour):
        self.areas = areas
        self.font_name = font_name
        self.font_colour = font_colour
        self.text_fields_file_id = None


drake = Meme({(319, 256): (322, 0), (319, 289): (322, 261)},
             'impact.ttf',
             (0, 0, 0))
scroll_of_truth = Meme({(96, 119): (95, 288)},
                       'impact.ttf',
                       (0, 0, 0))
expanding_brain = Meme({(422, 296): (0, 0), (420, 301): (2, 303), (417, 269): (2, 611), (419, 304): (2, 895)},
                       'impact.ttf',
                       (0, 0, 0))
who_would_win = Meme({(404, 398): (5, 97), (371, 396): (424, 97)},
                     'impact.ttf',
                     (0, 0, 0))
the_rock_driving = Meme({(241, 116): (316, 31), (229, 106): (330, 263)},
                        'impact.ttf',
                        (0, 0, 0))
sleeping_shaq = Meme({(309, 335): (2, 2), (304, 285): (2, 342)},
                     'impact.ttf',
                     (0, 0, 0))
nut_button = Meme({(308, 222): (12, 179), (315, 318): (270, 41)},
                  'impact.ttf',
                  (255, 255, 255))
batman_slapping_robin = Meme({(167, 75): (21, 3), (169, 82): (223, 2)},
                             'impact.ttf',
                             (0, 0, 0))
is_this_a_pigeon = Meme({(326, 110): (28, 65), (217, 84): (416, 91), (568, 90): (33, 478)},
                        'impact.ttf',
                        (255, 255, 255))
distracted_boyfriend = Meme({(161, 88): (97, 271), (150, 62): (309, 163), (151, 75): (449, 222)},
                            'impact.ttf',
                            (255, 255, 255))
croatia_bosnia_border = Meme({(418, 157): (305, 128), (449, 137): (360, 370), (528, 130): (40, 623)},
                             'impact.ttf',
                             (0, 0, 0))
left_exit_12_off_ramp = Meme({(262, 181): (101, 88), (276, 182): (369, 88), (427, 143): (195, 501)},
                             'impact.ttf',
                             (255, 255, 255))
hard_to_swallow_pills = Meme({(278, 216): (135, 558)},
                             'impact.ttf',
                             (0, 0, 0))
trump_presenting = Meme({(289, 96): (2, 251), (308, 100): (133, 146), (409, 199): (383, 274)},
                        'impact.ttf',
                        (255, 255, 255))
double_d_facts_book = Meme({(264, 130): (20, 494)},
                           'impact.ttf',
                           (0, 0, 0))
water_gun = Meme({(383, 112): (106, 343), (295, 214): (500, 369)},
                 'impact.ttf',
                 (255, 255, 255))
man_bear_fish = Meme({(561, 116): (103, 388), (333, 114): (219, 219), (232, 253): (560, 172)},
                     'impact.ttf',
                     (255, 255, 255))
upvotes = Meme({(177, 45): (8, 392)},
               'impact.ttf',
               (0, 0, 0))
who_killed_hannibal = Meme({(319, 275): (513, 178), (307, 234): (83, 229), (930, 118): (15, 958)},
                           'impact.ttf',
                           (255, 255, 255))
american_chopper_argument = Meme(
    {(232, 88): (12, 185), (311, 108): (185, 477), (282, 90): (1, 790), (228, 118): (1, 1066), (281, 98): (219, 1374)},
    'impact.ttf',
    (0, 0, 0))
battle_with_giant = Meme({(260, 224): (228, 96), (242, 153): (67, 506)},
                         'impact.ttf',
                         (255, 255, 255))
this_is_brilliant_but_i_like_this = Meme({(270, 166): (319, 127), (244, 172): (32, 460)},
                                         'impact.ttf',
                                         (255, 255, 255))
trojan_horse = Meme({(349, 131): (43, 207), (378, 147): (26, 346), (343, 135): (368, 41), (311, 155): (363, 527)},
                    'impact.ttf',
                    (255, 255, 255))
homers_fat = Meme({(222, 99): (426, 157), (284, 199): (130, 128), (319, 236): (124, 594)},
                  'impact.ttf',
                  (255, 255, 255))
you_cant_defeat_me = Meme({(262, 123): (221, 136), (243, 119): (431, 439), (357, 225): (195, 629)},
                          'impact.ttf',
                          (255, 255, 255))
beefy_tom = Meme({(412, 203): (288, 122), (307, 103): (13, 312)},
                 'impact.ttf',
                 (0, 0, 0))
disappointed_black_guy = Meme({(340, 298): (0, 0), (338, 298): (1, 305)},
                              'impact.ttf',
                              (0, 0, 0))
handshake = Meme({(333, 253): (7, 286), (375, 265): (525, 229), (337, 223): (179, 0)},
                 'impact.ttf',
                 (255, 255, 255))
spiderman_stops_bus = Meme({(361, 190): (0, 0), (456, 241): (116, 189), (410, 235): (340, 522)},
                           'impact.ttf',
                           (255, 255, 255))
man_throwing_card = Meme({(382, 184): (206, 0), (409, 331): (285, 254), (444, 259): (22, 642)},
                         'impact.ttf',
                         (255, 255, 255))
zac_efron_shrugs = Meme({(718, 91): (0, 0), (351, 216): (20, 385)},
                        'impact.ttf',
                        (0, 0, 0))
heart_attack = Meme({(298, 174): (0, 0), (296, 178): (2, 179), (295, 186): (1, 363)},
                    'impact.ttf',
                    (0, 0, 0))
tom_and_boys = Meme({(252, 105): (50, 115), (243, 115): (256, 223), (252, 127): (403, 109)},
                    'impact.ttf',
                    (255, 255, 255))
persian_cat = Meme({(692, 256): (14, 11)},
                   'helveticaneue.ttf',
                   (0, 0, 0))
tom_shoots_himself = Meme({(313, 132): (253, 271), (317, 133): (11, 427), (316, 122): (0, 140)},
                          'impact.ttf',
                          (255, 255, 255))
goodbye_high_school = Meme(
    {(377, 117): (17, 16), (213, 127): (207, 263), (228, 102): (0, 349), (265, 105): (416, 8), (223, 176): (144, 576), (335, 133): (483, 603)},
    'impact.ttf',
    (0, 0, 0))
kissing_pair = Meme({(253, 96): (11, 29), (217, 82): (316, 49), (264, 91): (14, 316)},
                    'impact.ttf',
                    (0, 0, 0))
useless_gun = Meme({(265, 80): (347, 3), (286, 209): (21, 16), (411, 239): (47, 555)},
                   'impact.ttf',
                   (255, 255, 255))
connor_pushes_circle = Meme({(606, 67): (69, 16), (607, 67): (69, 86), (605, 67): (69, 156), (604, 67): (69, 226)},
                            'impact.ttf',
                            (0, 0, 0))
lisa_simpson_presentation = Meme({(488, 262): (178, 103)},
                                 'arial.ttf',
                                 (0, 0, 0))
offering_sword = Meme({(426, 254): (121, 28), (497, 148): (256, 299), (458, 290): (437, 352)},
                      'impact.ttf',
                      (255, 255, 255))
domino_effect = Meme({(392, 108): (141, 435), (315, 171): (0, 83), (314, 125): (316, 239)},
                     'impact.ttf',
                     (255, 255, 255))
prince_charles_steals_wheel = Meme({(398, 225): (0, 128), (326, 236): (150, 393), (408, 279): (368, 234)},
                                   'impact.ttf',
                                   (255, 255, 255))
woman_with_microphones = Meme({(381, 233): (28, 157), (415, 221): (465, 161)},
                              'impact.ttf',
                              (255, 255, 255))
gillette_ad = Meme({(323, 160): (468, 205), (367, 245): (58, 287), (368, 332): (71, 831)},
                   'impact.ttf',
                   (255, 255, 255))
angry_crowd = Meme({(384, 122): (82, 39), (502, 258): (562, 260), (408, 145): (70, 560)},
                   'impact.ttf',
                   (0, 0, 0))
professionals_have_standards = Meme({(800, 247): (0, 0)},
                                    'helveticaneue.ttf',
                                    (0, 0, 0))
you_act_like_youre_better = Meme(
    {(295, 251): (152, 0), (170, 209): (25, 348), (129, 87): (198, 369), (155, 175): (307, 337)},
    'impact.ttf',
    (255, 255, 255))
let_me_in = Meme({(300, 187): (279, 186), (268, 226): (3, 194)},
                 'impact.ttf',
                 (255, 255, 255))
well_yes_but_no = Meme({(800, 156): (0, 0)},
                       'helveticaneue.ttf',
                       (0, 0, 0))
and_thats_a_fact = Meme({(331, 253): (809, 179)},
                        'impact.ttf',
                        (0, 0, 0))
Memes = {'drake': drake, 'scroll of truth': scroll_of_truth, 'expanding brain': expanding_brain,
         'who would win': who_would_win, 'the rock driving': the_rock_driving, 'sleeping shaq': sleeping_shaq,
         'nut button': nut_button, 'batman slapping robin': batman_slapping_robin, 'is this a pigeon': is_this_a_pigeon,
         'distracted boyfriend': distracted_boyfriend, 'croatia bosnia border': croatia_bosnia_border,
         'left exit 12 off ramp': left_exit_12_off_ramp, 'hard to swallow pills': hard_to_swallow_pills,
         'trump presenting': trump_presenting, 'double d facts book': double_d_facts_book, 'water gun': water_gun,
         'man bear fish': man_bear_fish, 'upvotes': upvotes, 'who killed hannibal': who_killed_hannibal,
         'american chopper argument': american_chopper_argument,
         'battle with giant': battle_with_giant, 'this is brilliant but i like this': this_is_brilliant_but_i_like_this,
         'trojan horse': trojan_horse, 'homer\'s fat': homers_fat, 'you can\'t defeat me': you_cant_defeat_me,
         'beefy tom': beefy_tom, 'disappointed black guy': disappointed_black_guy, 'handshake': handshake,
         'spiderman stops bus': spiderman_stops_bus, 'man throwing card': man_throwing_card,
         'zac efron shrugs': zac_efron_shrugs,
         'heart attack': heart_attack, 'tom and boys': tom_and_boys, 'persian cat': persian_cat,
         'tom shoots himself': tom_shoots_himself, 'goodbye high school': goodbye_high_school,
         'kissing pair': kissing_pair, 'useless gun': useless_gun, 'connor pushes circle': connor_pushes_circle,
         'lisa simpson presentation': lisa_simpson_presentation, 'offering sword': offering_sword,
         'domino effect': domino_effect, 'prince charles steals wheel': prince_charles_steals_wheel,
         'woman with microphones': woman_with_microphones, 'gillette ad': gillette_ad, 'angry crowd': angry_crowd,
         'professionals have standards': professionals_have_standards,
         'you act like you\'re better': you_act_like_youre_better, 'let me in': let_me_in,
         'well yes, but no': well_yes_but_no, 'and that\'s a fact': and_thats_a_fact}
