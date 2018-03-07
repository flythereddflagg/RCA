from pprint import pprint

sprite = './sprites/blocks/rock_blk.png'
block_list = []
with open('zone1.csv', 'r') as f:
    for line in f:
        if line[0] == '#': continue
        row = line.split(',')
        if not(len(row) == 5 or len(row) == 0):
            raise RCAException(
                "Invalid in-game configuration file syntax")
        block_list.append(row)

#pprint(block_list) # 60x27

start_point = 510, 1620
end_point = 3390, 2100

x, y = start_point

while y < end_point[1]:
    block_list.append(','.join([sprite, str(x), str(y), str(1), str(0)]))
    if x < end_point[0]:
        x += 24
    else:
        x = start_point[0]
        y += 24
        
        

#pprint(block_list)

with open('zone1.csv', 'w') as f:
    strn1 = '\n'.join(block_list)
    f.write(strn1)
