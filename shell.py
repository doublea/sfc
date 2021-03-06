#!/usr/bin/env python
import time
import os
import readline
from models import *
from campaign import *

os.environ['PYTHONINSPECT'] = 'True'

ship_fieldnames = ['race',
                   'hull_type',
                   'ship_class',
                   'class_type',
                   'bpv',
                   'special_role',
                   'year_first_available',
                   'year_last_available',
                   'size_class',
                   'turn_mode',
                   'move_cost',
                   'het_2_turns_nimble',
                   'het_breakdown',
                   'stealth_ecm',
                   'regular_crew',
                   'boarding_parties_base',
                   'boarding_parties_max',
                   'deck_crews',
                   'total_crew',
                   'min_crew',
                   'shield_1',
                   'shield_2___6',
                   'shield_3___5',
                   'shield_4',
                   'shield_total',
                   'cloak',
                   'heavy_weapon_1_num',
                   'heavy_weapon_1',
                   'heavy_weapon_1_arc',
                   'heavy_weapon_2_num',
                   'heavy_weapon_2',
                   'heavy_weapon_2_arc',
                   'heavy_weapon_3_num',
                   'heavy_weapon_3',
                   'heavy_weapon_3_arc',
                   'heavy_weapon_4_num',
                   'heavy_weapon_4',
                   'heavy_weapon_4_arc',
                   'heavy_weapon_5_num',
                   'heavy_weapon_5',
                   'heavy_weapon_5_arc',
                   'heavy_weapon_6_num',
                   'heavy_weapon_6',
                   'heavy_weapon_6_arc',
                   'heavy_weapon_7_num',
                   'heavy_weapon_7',
                   'heavy_weapon_7_arc',
                   'heavy_weapon_8_num',
                   'heavy_weapon_8',
                   'heavy_weapon_8_arc',
                   'heavy_weapon_9_num',
                   'heavy_weapon_9',
                   'heavy_weapon_9_arc',
                   'heavy_weapon_10_num',
                   'heavy_weapon_10',
                   'heavy_weapon_10_arc',
                   'weapon_11_num',
                   'weapon_11',
                   'weapon_11_arc',
                   'weapon_12_num',
                   'weapon_12',
                   'weapon_12_arc',
                   'weapon_13_num',
                   'weapon_13',
                   'weapon_13_arc',
                   'weapon_14_num',
                   'weapon_14',
                   'weapon_14_arc',
                   'weapon_15_num',
                   'weapon_15',
                   'weapon_15_arc',
                   'weapon_16_num',
                   'weapon_16',
                   'weapon_16_arc',
                   'weapon_17_num',
                   'weapon_17',
                   'weapon_17_arc',
                   'weapon_18_num',
                   'weapon_18',
                   'weapon_18_arc',
                   'weapon_19_num',
                   'weapon_19',
                   'weapon_19_arc',
                   'weapon_20_num',
                   'weapon_20',
                   'weapon_20_arc',
                   'weapon_21_num',
                   'weapon_21',
                   'weapon_21_arc',
                   'weapon_22_num',
                   'weapon_22',
                   'weapon_22_arc',
                   'weapon_23_num',
                   'weapon_23',
                   'weapon_23_arc',
                   'weapon_24_num',
                   'weapon_24',
                   'weapon_24_arc',
                   'weapon_25_num',
                   'weapon_25',
                   'weapon_25_arc',
                   'probes',
                   't_bombs_base',
                   't_bombs_max',
                   'nuclear_mine_base',
                   'nuclear_mine_max',
                   'drone_control',
                   'add_6',
                   'add_12',
                   'shuttles_size',
                   'launch_rate',
                   'general_base',
                   'general_max',
                   'fighter_bay_1',
                   'fighter_type_1',
                   'fighter_bay_2',
                   'fighter_type_2',
                   'fighter_bay_3',
                   'fighter_type_3',
                   'fighter_bay_4',
                   'fighter_type_4',
                   'armor',
                   'forward_hull',
                   'center_hull',
                   'aft_hull',
                   'cargo',
                   'barracks',
                   'repair',
                   'r_l_warp',
                   'c_warp',
                   'impulse',
                   'apr',
                   'battery',
                   'bridge',
                   'security',
                   'lab',
                   'transporters',
                   'tractors',
                   'mech_tractors',
                   'special_sensors',
                   'sensors',
                   'scanners',
                   'explosion_strength',
                   'acceleration',
                   'damage_control',
                   'extra_damage',
                   'ship_cost',
                   'refit_base_class',
                   'geometry',
                   'ui',
                   'full_name',
                   'refits',
                   'balance',
                   'end',
                   '',
                   'w1',
                   'w2',
                   'w3',
                   'w4',
                   'w5',
                   'w6',
                   'w7',
                   'w8',
                   'w9',
                   'w10',
                   'w11',
                   'w12',
                   'w13',
                   'w14',
                   'w15',
                   'w16',
                   'w17',
                   'w18',
                   'w19',
                   'w20',
                   'w21',
                   'w22',
                   'w23',
                   'w24',
                   'w25',
                   'weapon_bpv',
                   'fb1',
                   'fb2',
                   'fb3',
                   'fb4',
                   'fighter_subtotal',
                   'system_bpv',
                   'bpv_subtotal',
                   'yfa',
                   'yla',
                   'enhanced_class_type',
                   'role',
                   'secondary_role',
                   'xtech',
                   'productionavailability',
]

def iter_ships(path):
    seen_headers = False
    with open(path) as file:
        for line in file:
            if len(line.strip()) == 0 or line[0] == '\t':
                continue
            if not seen_headers:
                seen_headers = True
                continue
            s = ShipModel()
            for attr, value in zip(ship_fieldnames, line.strip().split('\t')):
                if attr:
                    setattr(s, attr, value)
            yield s

def import_shiplist(path='./shiplist.txt'):
    t0 = time.time()
    this_sec = 0
    total = 0
    for ship in iter_ships(path):
        db.session.add(ship)
        if time.time() - t0 >= 1:
            print this_sec, "per second.", total, "total."
            this_sec = 0
            t0 = time.time()
        else:
            this_sec += 1
        total += 1
    print "Commiting to DB..."
    db.session.commit()
    print "Imported", total, "ships."

def set_up():
    print "Creating database schema...",
    db.create_all()
    print "Done"

    print "Importing ships from shiplist..."
    import_shiplist()
    print "Done"

