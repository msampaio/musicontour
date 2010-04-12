#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour as c
import subprocess

### data
## soprano, choral 002
contour = [440.00, 493.88, 392.00, 369.99, 329.63, 493.88, 554.37,
493.88, 440.00, 415.30, 369.99, 415.30, 369.99, 329.63, 659.26,
587.33, 554.37, 493.88, 440.00, 493.88, 554.37, 493.88, 554.37,
587.33, 554.37, 493.88, 466.16, 493.88, 329.63, 440.00, 493.88,
554.37, 587.33, 659.26, 587.33, 554.37, 493.88, 587.33, 554.37,
493.88, 659.26, 587.33, 554.37, 493.88, 440.00, 493.88, 554.37,
493.88, 440.00]

contour_cc = c.contour_class(contour)

# print(c.contours_count(contour_cc, 4))

# c.kern_file_process('/tmp/teste-python/002.krn')

files = ['001.freq', '002.freq', '003.freq', '004.freq', '005.freq',
         '006.freq', '007.freq', '008.freq', '009.freq', '010.freq',
         '011.freq', '012.freq', '013.freq', '014.freq', '015.freq',
         '016.freq', '017.freq', '018.freq', '019.freq', '020.freq',
         '021.freq', '022.freq', '023.freq', '024.freq', '025.freq',
         '026.freq', '027.freq', '028.freq', '029.freq', '030.freq',
         '031.freq', '032.freq', '033.freq', '034.freq', '035.freq',
         '036.freq', '037.freq', '038.freq', '039.freq', '040.freq',
         '041.freq', '042.freq', '043.freq', '044.freq', '045.freq',
         '046.freq', '047.freq', '048.freq', '049.freq', '050.freq',
         '051.freq', '052.freq', '053.freq', '054.freq', '055.freq',
         '056.freq', '057.freq', '058.freq', '059.freq', '060.freq',
         '061.freq', '062.freq', '063.freq', '064.freq', '065.freq',
         '066.freq', '067.freq', '068.freq', '069.freq', '070.freq',
         '071.freq', '072.freq', '073.freq', '074.freq', '075.freq',
         '076.freq', '077.freq', '078.freq', '079.freq', '080.freq',
         '081.freq', '082.freq', '083.freq', '084.freq', '085.freq',
         '086.freq', '087.freq', '088.freq', '089.freq', '090.freq',
         '091.freq', '092.freq', '093.freq', '094.freq', '095.freq',
         '096.freq', '097.freq', '098.freq', '099.freq', '100.freq',
         '101.freq', '102.freq', '103.freq', '104.freq', '105.freq',
         '106.freq', '107.freq', '108.freq', '109.freq', '110.freq',
         '111.freq', '112.freq', '113.freq', '114.freq', '115.freq',
         '116.freq', '117.freq', '118.freq', '119.freq', '120.freq',
         '121.freq', '122.freq', '123.freq', '124.freq', '125.freq',
         '126.freq', '127.freq', '128.freq', '129.freq', '130.freq',
         '131.freq', '132.freq', '133.freq', '134.freq', '135.freq',
         '136.freq', '137.freq', '138.freq', '139.freq', '140.freq',
         '141.freq', '142.freq', '143.freq', '144.freq', '145.freq',
         '146.freq', '147.freq', '148.freq', '149.freq', '151.freq',
         '152.freq', '153.freq', '154.freq', '155.freq', '156.freq',
         '157.freq', '158.freq', '159.freq', '160.freq', '161.freq',
         '162.freq', '163.freq', '164.freq', '165.freq', '166.freq',
         '167.freq', '168.freq', '169.freq', '170.freq', '171.freq',
         '172.freq', '173.freq', '174.freq', '175.freq', '176.freq',
         '177.freq', '178.freq', '179.freq', '180.freq', '181.freq',
         '182.freq', '183.freq', '184.freq', '185.freq', '186.freq',
         '187.freq', '188.freq', '189.freq', '190.freq', '191.freq',
         '192.freq', '193.freq', '194.freq', '195.freq', '196.freq',
         '197.freq', '198.freq', '199.freq', '200.freq', '201.freq',
         '202.freq', '203.freq', '204.freq', '205.freq', '206.freq',
         '207.freq', '208.freq', '209.freq', '210.freq', '211.freq',
         '212.freq', '213.freq', '214.freq', '215.freq', '216.freq',
         '217.freq', '218.freq', '219.freq', '220.freq', '221.freq',
         '222.freq', '223.freq', '224.freq', '225.freq', '226.freq',
         '227.freq', '228.freq', '229.freq', '230.freq', '231.freq',
         '232.freq', '233.freq', '234.freq', '235.freq', '236.freq',
         '237.freq', '238.freq', '239.freq', '240.freq', '241.freq',
         '242.freq', '243.freq', '244.freq', '245.freq', '246.freq',
         '247.freq', '248.freq', '249.freq', '250.freq', '251.freq',
         '252.freq', '253.freq', '254.freq', '255.freq', '256.freq',
         '257.freq', '258.freq', '259.freq', '260.freq', '261.freq',
         '262.freq', '263.freq', '264.freq', '265.freq', '266.freq',
         '267.freq', '268.freq', '269.freq', '270.freq', '271.freq',
         '272.freq', '273.freq', '274.freq', '275.freq', '276.freq',
         '277.freq', '278.freq', '279.freq', '280.freq', '281.freq',
         '282.freq', '283.freq', '284.freq', '285.freq', '286.freq',
         '287.freq', '288.freq', '289.freq', '290.freq', '291.freq',
         '292.freq', '293.freq', '294.freq', '295.freq', '296.freq',
         '297.freq', '298.freq', '299.freq', '300.freq', '301.freq',
         '302.freq', '303.freq', '304.freq', '305.freq', '306.freq',
         '307.freq', '308.freq', '309.freq', '310.freq', '311.freq',
         '312.freq', '313.freq', '314.freq', '315.freq', '316.freq',
         '317.freq', '318.freq', '319.freq', '320.freq', '321.freq',
         '322.freq', '323.freq', '324.freq', '325.freq', '326.freq',
         '327.freq', '328.freq', '329.freq', '330.freq', '331.freq',
         '332.freq', '333.freq', '334.freq', '335.freq', '336.freq',
         '337.freq', '338.freq', '339.freq', '340.freq', '341.freq',
         '342.freq', '343.freq', '344.freq', '345.freq', '346.freq',
         '347.freq', '348.freq', '349.freq', '350.freq', '351.freq',
         '352.freq', '353.freq', '354.freq', '355.freq', '356.freq',
         '357.freq', '358.freq', '359.freq', '360.freq', '361.freq',
         '362.freq', '363.freq', '364.freq', '365.freq', '366.freq',
         '367.freq', '368.freq', '369.freq', '370.freq', '371.freq']

test_file = "/tmp/freq/371.freq"
path = "/tmp/freq/"

saida = c.frequency_file_contour_count(path, "371.freq", 2)

# print(saida)

chorals = [c.frequency_file_contour_count(path, f, 2) for f in files]

# print(chorals)

tf = "371.freq"
n = 4
z = c.count_contours_list_of_files(path, files, 3)

print(c.percent(z))
