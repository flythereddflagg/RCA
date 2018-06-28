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

start_point = 510, 1756
end_point = 3100, 1910

x, y = start_point
size = 24, 24
scale = 2
size = 24 * scale, 24 * scale
angle = 0

while y < end_point[1]:
    block_list.append(','.join([
        sprite, 
        str(x), 
        str(y), 
        str(scale), 
        str(angle)]))
    if x < end_point[0]:
        x += size[0]
    else:
        x = start_point[0]
        y += size[1]
        
        

#pprint(block_list)

with open('zone1.csv', 'w') as f:
    strn1 = '\n'.join(block_list)
    f.write(strn1)
