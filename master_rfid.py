#Have To Check RSSI Values
#Header Files
import math
import numpy as np
import pandas as pd
import bezier
from shapely import geometry
from matplotlib import pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import itertools

#Function Definitions
def check(str1,str2):
	arr1= str1.split(',')
	arr2= str2.split(',')
	arr1 = map(int, arr1)
	arr2 = map(int, arr2)
	for j in arr1:
		for i in arr2:
			if j/5==i/5:
				return False
	return True


def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def findantenna(polycol,antennaid,powerlevel):
    polygon_antenna=polycol[antennaid-1][(powerlevel-10)/5]
    ring_patch3 = PolygonPatch(polygon_antenna,color="blue")
    return polygon_antenna

def find_antenna_coordinates(antennaid):
    xcor=antenna_x_values[antennaid-1]
    ycor=antenna_y_values[antennaid-1]
    return (xcor,ycor)

def distanceRssi(rssi,rand):
    return (pow(10,(-52-rssi)/10*rand))*100

def position_calculate_x(direction , x ,cosx , dist):

    if(direction=="u"):
        return x-(dist*cosx)

    elif (direction=="d"):
        return x + (dist*cosx)

    elif(direction == "l"):
        return x - (dist*cosx)

    else:
        return x + (dist*cosx)

def position_calculate_y(direction , x ,cosx , dist):

    if(direction=="u"):
        return x+(dist*cosx)

    elif (direction=="d"):
        return x - (dist*cosx)

    elif(direction == "l"):
        return x - (dist*cosx)

    else:
        return x + (dist*cosx)

def sortGroup(string):
	arr= string.split(',')
	arr = map(int, arr)
	final_list=[]
	key_string=''
	for num in sorted(arr):
        	if num not in final_list:
           	 	final_list.append(num)
           	 	key_string=key_string+','+str(num)
    	return key_string[1:]


#Main Function

bezier_curve_values={
10: [30,55,69,81,90,81,69,55,30],
15: [35,70,89,126,187,126,89,70,35],
20: [58,87,154,206,326,206,154,87,58],
25: [64,256,340,412,587,412,340,256,64],
30: [210,480,547,760,1080,760,547,480,210]
}
no_of_antenna = int(input("Enter the number of antennas:"))
pointrtree=[]
nodes = []
poly_each_antenna=[]
antenna_points=[]
#Have To Generalize The Antenna Position Code
antenna_x_values=[350,350,1550,1550]
antenna_y_values=[250,600,250,600]
direction_values=['r','r','l','l']

for l in range(0,no_of_antenna):
	position = direction_values[l]
	antenna_points.append((antenna_x_values[l],antenna_y_values[l]))
	xcor=[None]*9
	ycor=[None]*9
	curve =[None]*10
	poly_each_level=[]
	j=0
	for power in [10,15,20,25,30]:
		j=0
		pointList=[]
		for angle in [0,30,45,60,90,120,135,150,180]:
			max_distance_from_antenna= bezier_curve_values[power][j]
			if position == 'l':
				angle = 90 -angle
			if position == 'r':
				angle = 90 - angle
			cosx=math.cos(math.radians(angle))
			sinx=math.sin(math.radians(angle))
			xcor[j] = position_calculate_x(position,antenna_x_values[l],cosx,max_distance_from_antenna)
			ycor[j] = position_calculate_y(position,antenna_y_values[l],sinx,max_distance_from_antenna)
			pointList.append(geometry.Point(xcor[j],ycor[j]))
			j=j+1

		nodesA_1_10_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3],xcor[4]],[ycor[0],ycor[1],ycor[2],ycor[3],ycor[4]]])
		nodesA_1_10_2 = np.array([[xcor[4],xcor[5],xcor[6],xcor[7],xcor[8]],[ycor[4],ycor[5],ycor[6],ycor[7],ycor[8]]])
		nodes.append(nodesA_1_10_1)
		nodes.append(nodesA_1_10_2)
		#del pointList[7]
		#del pointList[5]
		#del pointList[3]
		#del pointList[1]
		poly = geometry.Polygon([[p.x, p.y] for p in pointList])
		poly_each_level.append(poly)
	poly_each_antenna.append(poly_each_level)


curve1 = bezier.Curve(nodes[0], degree=3)
ax = curve1.plot(num_pts=256)
del nodes[0]
for n in nodes:
    curve1 = bezier.Curve(n, degree=3)
    curve1.plot(num_pts=256, ax=ax)

total_polygons = []
for x in poly_each_antenna:
    for y in x:
        total_polygons.append(y)


#Code To Perfect The polygons without overlapping
new_total_polygons=[]
for i in range(0,len(total_polygons)):
    if i%5==0:
        new_total_polygons.append(total_polygons[i])
        continue
    else:
        previous_polygon=total_polygons[i-1]
        current_polygon=total_polygons[i]
        current_polygon=current_polygon.difference(previous_polygon)
        new_total_polygons.append(current_polygon)


total_polygons=new_total_polygons


plt.margins(x=0)
plt.margins(y=0)
plt.xticks(np.arange(-50, 1800, step=50))
plt.yticks(np.arange(-50, 1800, step=50))


#Finished Splitting the regions according to antennas power level  ie: for 4 antennas 20 regions
#Have to take into account overlapping sub regions
first_level_polygons={}



for i in range(0,len(total_polygons)):
	first_level_polygons[str(i)]=total_polygons[i]

#For Checking
#first_level_polygons[str(4)]=total_polygons[4]
#first_level_polygons[str(13)]=total_polygons[13]
#first_level_polygons[str(14)]=total_polygons[14]
#first_level_polygons[str(19)]=total_polygons[19]


#All Single Power Level
polygon_complete_list=[]
temp_dict={}
for key,value in first_level_polygons.items():
	temp_dict['key']=key
	temp_dict['value']=value
	polygon_complete_list.append(temp_dict)
	temp_dict={}


print "Only One Power Level"
for i in polygon_complete_list:
	print i['key']
loop_polygons=polygon_complete_list



#Finding The Two Power Level Intersection Combination of 1 and 1
temp_dict={}
iteration_no=1
two_item_set_polygons=[]
for outer in loop_polygons:
	for inner in loop_polygons:
		iteration_no=iteration_no+1
		if(outer['value']!=inner['value']):
			if( outer['value'].intersects(inner['value'])  and (  (int(outer['key'])/5)!=(int(inner['key'])/5) ) and( (outer['value'].intersection(inner['value'])).geom_type == 'Polygon' or (outer['value'].intersection(inner['value'])).geom_type == 'MultiPolygon') ):

				temp_dict={}
				temp_dict['key']=sortGroup(str(outer['key'])+','+str(inner['key']))
				temp_dict['value']=outer['value'].intersection(inner['value'])
				two_item_set_polygons.append(temp_dict)
				outer_change=outer['value'].difference(inner['value'])
				inner_change=inner['value'].difference(outer['value'])
				outer['value']=outer_change
				inner['value']=inner_change

two_item_set_polygons = { each['key'] : each for each in two_item_set_polygons }.values()

print "Two power Level"
for i in two_item_set_polygons:
	print i['key']


#Finding The Three Power Level Intersection Combination of 1 and 2
three_item_set_polygons=[]
for outer in loop_polygons:
	for inner in two_item_set_polygons:
		iteration_no=iteration_no+1
		if(outer['value']!=inner['value']):
			if( outer['value'].intersects(inner['value'])and( (outer['value'].intersection(inner['value'])).geom_type == 'Polygon' or (outer['value'].intersection(inner['value'])).geom_type == 'MultiPolygon')and check(outer['key'],inner['key'])):
				temp_dict={}
				temp_dict['key']=sortGroup(str(outer['key'])+','+str(inner['key']))
				temp_dict['value']=outer['value'].intersection(inner['value'])
				three_item_set_polygons.append(temp_dict)
				outer_change=outer['value'].difference(inner['value'])
				inner_change=inner['value'].difference(outer['value'])
				outer['value']=outer_change
				inner['value']=inner_change
three_item_set_polygons = { each['key'] : each for each in three_item_set_polygons }.values()
print "Three Power Level"
for i in three_item_set_polygons:
	print i['key']

final_item_set=three_item_set_polygons+two_item_set_polygons+loop_polygons


#poly22=(total_polygons[4].intersection(total_polygons[9])).intersection(total_polygons[14])
#ring_patch3 = PolygonPatch(poly22,color="blue")
#ax.add_patch(ring_patch3)




#Finding The 4 Power Level Intersection Combination of 2 and 2    or 1 and 3
four_item_set_polygons=[]
for outer in loop_polygons:
	#print outer
	for inner in three_item_set_polygons:
		iteration_no=iteration_no+1
		if(outer['value']!=inner['value']):
			if( outer['value'].intersects(inner['value'])and( (outer['value'].intersection(inner['value'])).geom_type == 'Polygon' or (outer['value'].intersection(inner['value'])).geom_type == 'MultiPolygon')and check(outer['key'],inner['key'])):
				temp_dict={}
				temp_dict['key']=sortGroup(str(outer['key'])+','+str(inner['key']))
				temp_dict['value']=outer['value'].intersection(inner['value'])
				four_item_set_polygons.append(temp_dict)
				outer_change=outer['value'].difference(inner['value'])
				inner_change=inner['value'].difference(outer['value'])
				outer['value']=outer_change
				inner['value']=inner_change

for outer in two_item_set_polygons:
	#print outer
	for inner in two_item_set_polygons:
		iteration_no=iteration_no+1
		#print iteration_no
		#print "Length:"+str(len(loop_polygons))
		if(outer['value']!=inner['value']):
			if( outer['value'].intersects(inner['value'])and( (outer['value'].intersection(inner['value'])).geom_type == 'Polygon' or (outer['value'].intersection(inner['value'])).geom_type == 'MultiPolygon')and check(outer['key'],inner['key'])):
				temp_dict={}
				temp_dict['key']=sortGroup(str(outer['key'])+','+str(inner['key']))
				temp_dict['value']=outer['value'].intersection(inner['value'])
				four_item_set_polygons.append(temp_dict)
				outer_change=outer['value'].difference(inner['value'])
				inner_change=inner['value'].difference(outer['value'])
				outer['value']=outer_change
				inner['value']=inner_change






four_item_set_polygons = { each['key'] : each for each in four_item_set_polygons }.values()
print "Four Power Level"
for i in four_item_set_polygons:
	print i['key']

#Adding All The Intersecting Regions

final_item_set=three_item_set_polygons+two_item_set_polygons+loop_polygons+four_item_set_polygons
print len(final_item_set)
'''
Checking By Filling Color On  a particular area or polygon
for i in final_item_set:
	if i['key']=='4,9,13,19':
		poly22=i['value']
		ring_patch3 = PolygonPatch(poly22,color="red")
		ax.add_patch(ring_patch3)

	if i['key']=='4,14,19':
		poly22=i['value']
		ring_patch3 = PolygonPatch(poly22,color="blue")
		ax.add_patch(ring_patch3)
	if i['key']=='4,9,19':
		poly22=i['value']
		ring_patch3 = PolygonPatch(poly22,color="green")
		ax.add_patch(ring_patch3)
	if i['key']=='4,9,14':
		poly22=i['value']
		ring_patch3 = PolygonPatch(poly22,color="yellow")
		ax.add_patch(ring_patch3)
	if i['key']=='9,14':
		poly22=i['value']
		ring_patch3 = PolygonPatch(poly22,color="pink")
		ax.add_patch(ring_patch3)

'''
main_dict={}
for i in final_item_set:
	main_dict[i['key']]=i['value']

#print polygons_dict['4,9,14']


#Reading The Data Sheet
rfid_readings=pd.read_csv(os.getcwd()+"exp_rfid_20-12-2018_csv.csv")
xcor=rfid_readings["x"]
ycor=rfid_readings["y"]
sno_list=rfid_readings["Point"]


#Plotting The Points
i=0
plt.plot(xcor, ycor, 'ro')
for x,y in zip(xcor,ycor):
    plt.annotate(xy=[x,y], s=str(sno_list)[i])
    i+=1
data_read={}
for sno in sno_list:
	data_read[str(sno)]=[]



power_list=rfid_readings["Power"]
antenna_list=rfid_readings["Antenna"]
print "Reading The Data Sheet"

for key,record in rfid_readings.iterrows():
	if(str(record["Point"]) in data_read):
		data_read[str(record["Point"])].append((record["Antenna"]-1)*4+(record["Power"]-10)/5)
	else:
		data_read[str(record["Point"])]=(record["Antenna"]-1)*4+(record["Power"]-10)/5

for key,value in data_read.items():
	print "Key:"+str(key) +" Value:"+str(value)

#acomab=str(raw_input("Enter The Query Point"))
acomab=str('400,500')
xco=float(acomab.split(',')[0])
yco=float(acomab.split(',')[1])
query_point=Point(xco,yco)


polygon_set=[]

for key,value in main_dict.items():
    print key
    polygon_set.append(value)


keep_dict={}
tag_name_dict={}
for key,value in data_read.items():
	print str(value)
	polygon_name=main_dict[str(value[0])]
	if str(polygon_name) in keep_dict:
        	keep_dict[str(polygon_name)]+=1
		tag_name_dict[str(polygon_name)].append(key)
	else:
		keep_dict[str(polygon_name)]=1
		tag_name_dict[str(polygon_name)]=[key]

#print "Polygon Count Of Tags"
#for key,value in keep_dict.items():
#	print " Value:"+str(value)


k=5
for radius in range(1,12):
    total_tags=[]
    radi=radius*100
    circle = query_point.buffer(radi)
    ration_value=0
    total_tags_detected=0
    total_polygons=polygon_set
    dict3=keep_dict

    for poly in total_polygons:
        if circle.intersects(poly):
            # list_of_points=dict3[poly]
            no_of_tags=0
            if str(poly) in dict3.keys():
	    	no_of_tags=dict3[str(poly)]
            	print "no. of tags detected"
            	print no_of_tags
           	 # dict3[str(powerlevelpoly)]+=1
            	total_tags_detected+=no_of_tags
            	print "tags detected id"
            	getid=tag_name_dict[str(poly)]
            	list_of_points=getid
            	total_tags.append(list_of_points)
            	print list_of_points
            	intersection_area=circle.intersection(poly).area
            	poly_area=poly.area
            	ra_value=(intersection_area/poly_area)*float(no_of_tags)
            	ration_value+=ra_value
            	print "ratio value for this curve"
            	print ra_value
    	print "ratio value for this iteration"
    	print ration_value

    	if ration_value>=k:
        	print "breaking"
        	print "total_tags_detected"
        	print total_tags_detected
        	print "tags detected are"
        	arr=np.array(total_tags)
        	arr.flatten()
        	print arr
        	break








plt.show()
