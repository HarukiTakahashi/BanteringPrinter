;FLAVOR:Marlin
;TIME:1001
;Filament used: 0.608168m
;Layer height: 0.2
;MINX:62.277
;MINY:59.436
;MINZ:0.2
;MAXX:90.577
;MAXY:89.038
;MAXZ:5
;TARGET_MACHINE.NAME:Creality Ender-2
;Generated with Cura_SteamEngine 5.5.0
M82 ;absolute extrusion mode

G28 ;Home


M140 S0
M107
G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z5 ;Raise Z more
G90 ;Absolute positioning

G1 X0 Y10 ;Present print
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z

M82 ;absolute extrusion mode
M104 S0
;End of Gcode
;SETTING_3 {"global_quality": "[general]\\nversion = 4\\nname = Standard Quality
;SETTING_3  #2\\ndefinition = creality_ender2\\n\\n[metadata]\\ntype = quality_c
;SETTING_3 hanges\\nquality_type = standard\\nsetting_version = 22\\n\\n[values]
;SETTING_3 \\nadhesion_type = none\\n\\n", "extruder_quality": ["[general]\\nver
;SETTING_3 sion = 4\\nname = Standard Quality #2\\ndefinition = creality_base\\n
;SETTING_3 \\n[metadata]\\ntype = quality_changes\\nquality_type = standard\\nse
;SETTING_3 tting_version = 22\\nposition = 0\\n\\n[values]\\n\\n"]}
