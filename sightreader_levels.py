
## Beginner Level Notes

#treble_clef_only_L0 = ('C4', 'D4', 'E4', 'F4', 'G4', 'B5', 'A5', 'A4', 'B4', 'C5')
treble_clef_only_L0 = ('C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4')
number_of_notes_treble_clef_L0 = 7
tcL0_note_img_map = {i: treble_clef_only_L0[i]
                     for i in range(len(treble_clef_only_L0))}

#bass_clef_only_L0 = ('B3B', 'A3B', 'G3B', 'F3B', 'D4B', 'E4B', 'E3B', 'D3B', 'C3B', 'C4B')
bass_clef_only_L0 = ('B3B', 'A3B', 'G3B', 'F3B', 'D4B', 'E4B')
number_of_notes_bass_clef_L0 = 7
bcL0_note_img_map = {i: bass_clef_only_L0[i]
                     for i in range(len(bass_clef_only_L0))}

both_clef_L0 = treble_clef_only_L0 + bass_clef_only_L0
number_of_notes_both_clef_L0 = 14
both_clef_L0_note_img_map = {i: both_clef_L0[i]
                             for i in range(len(both_clef_L0))}



## Intermediate Level Notes

treble_clef_only_L1 = ('C4', 'D4', 'E4', 'F4', 'G4', 'B5', 'A5', 'A4', 'B4', 'C5','G3','D5','E5','F5','G5','A6','B6','C6')
number_of_notes_treble_clef_L1 = 18
tcL1_note_img_map = {i: treble_clef_only_L1[i]
                     for i in range(len(treble_clef_only_L1))}

bass_clef_only_L1 = ('A2B','B2B','C2B','D2B','E2B','F2B','G2B','B3B', 'A3B', 'G3B', 'F3B', 'D4B', 'E4B', 'E3B', 'D3B', 'C3B', 'C4B','F4B')
number_of_notes_bass_clef_L1 = 18
bcL1_note_img_map = {i: bass_clef_only_L1[i]
                     for i in range(len(bass_clef_only_L1))}

both_clef_L1 = treble_clef_only_L1 + bass_clef_only_L1
number_of_notes_both_clef_L1 = 36
both_clef_L1_note_img_map = {i: both_clef_L1[i]
                             for i in range(len(both_clef_L1))}