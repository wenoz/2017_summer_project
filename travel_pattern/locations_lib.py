######   Store All locations   #####
ud_1 = ['7th Ave NE and NE 50th St, Seattle', 'NE 45th St and Union Bay PI NE, Seattle']
ud_2 = ['7th Ave NE and NE 45th St, Seattle', 'Walla Walla Rd and Snohomish Ln N, Seattle']
ud_3 = ['NE Pacific St and NE Boat St, Seattle', '2802 E Park Dr E, Seattle']

ud_combine = ['7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle']

ch_1 = ['Bellevue Ave E and E Mercer St, Seattle', '15th Ave and E Olive St, Seattle']
ch_2 = ['Bellevue Ave and E Olive St, Seattle', '15th Ave and E Union St, Seattle']
ch_3 = ['Pike St and Boren Ave, Seattle', '15th Ave and E Jefferson St, Seattle']


ch_combine = ['Bellevue Ave E and E Mercer St, Seattle', '15th Ave and E Jefferson St, Seattle']

pc_combine = ['62nd Ave NW and 24th St NW, Artondale', '120th St E and 214th Ave E, Tacoma']

# origin = [pc_combine]
# destination = [ud_1, ud_2, ud_3]

#get_count_matrix(origin, destination, input_year = 2015, input_uw = False )
#get_count_matrix(origin, destination, input_year = 2016, input_uw = False )

'''
get_count_matrix(origin, destination, input_year = 2016)
get_count_matrix(origin, destination, input_year = 2015)
pattern = get_travel_pattern(pc_combine[0], pc_combine[1], ud_combine[0], ud_combine[1], input_year =2016)
old_pattern = get_travel_pattern(pc_combine[0], pc_combine[1], ud_combine[0], ud_combine[1], input_year =2015)

'''

'''
pc_1 =[  ,   ]
pc_2 = [  ,  ]
pc_3 = [  ,   ] '''

'''
origin = [ud_1, ud_2, ud_3]
destination = [ch_1, ch_2, ch_3]


origin = [ud_combine]
destination = [ch_combine]

origin = [ud_1, ud_2, ud_3]
destination = [ud_1, ud_2, ud_3]

get_count_matrix(origin, destination, input_year = 2015, input_uw = True )
get_count_matrix(origin, destination, input_year = 2016, input_uw = True )


'''

'''
get_travel_pattern(ud_1[0], ud_1[1], ch_1[0],ch_1[1])
get_travel_pattern(ud_1[0], ud_1[1], ch_2[0],ch_2[1])
get_travel_pattern(ud_1[0], ud_1[1], ch_3[0],ch_3[1])

get_travel_pattern(ud_2[0], ud_2[1], ch_1[0],ch_1[1])
get_travel_pattern(ud_2[0], ud_2[1], ch_2[0],ch_2[1])
get_travel_pattern(ud_2[0], ud_2[1], ch_3[0],ch_3[1])

get_travel_pattern(ud_3[0], ud_3[1], ch_1[0],ch_1[1])
get_travel_pattern(ud_3[0], ud_3[1], ch_2[0],ch_2[1])
get_travel_pattern(ud_3[0], ud_3[1], ch_3[0],ch_3[1])




internal travelling within u district 
internal_use_15  = get_travel_pattern('7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle', '7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle', input_year= 2015, input_uw =True)
internal_use_16 = get_travel_pattern('7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle', '7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle', input_year= 2016, input_uw =True )


internal_use_15 = get_travel_pattern( ud_combine[0], ud_combine[1], ud_combine[0], ud_combine[1], input_year= 2015, input_uw =True)
internal_use_16 = get_travel_pattern( ud_combine[0], ud_combine[1], ud_combine[0], ud_combine[1], input_year= 2016, input_uw =True)



uw_to_cap_16 = get_travel_pattern('7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle, Seattle', 'Bellevue Ave E and E Mercer St, Seattle', '15th Ave and E Jefferson St, Seattle', input_year= 2016 )
uw_to_cap_15 = get_travel_pattern('7th Ave NE and NE 50th St, Seattle', '2802 E Park Dr E, Seattle', 'Bellevue Ave E and E Mercer St, Seattle', '15th Ave and E Jefferson St, Seattle', input_year= 2015 )

'''




