# {0: 'A-10-S-TANDEM', 1: 'A-10-TRIDEM', 2: 'AXLE', 3: 'COMBINED', 4: 'TYPE-2', 5: 'TYPE-2-S2', 6: 'TYPE-3', 7: 'UC'}
# modified


def predict_raised_axle_perpendicular_dist_approach(axle_data,threshhold):

    import numpy as np

    if(len(axle_data)==0):
        return False
    if(len(axle_data)==5):
        return True

    has_raised_axle = False
    slopes = []
    axle_count = len(axle_data)-1
    
    np.sort(axle_data)


    for i in range(0,axle_count):
        slopes.append(int(-1)*(axle_data[axle_count][0]-axle_data[i][0])/(axle_data[axle_count][1]-axle_data[i][1]))

    # print(slopes)
    std_dev = np.std(slopes)

    if(std_dev>=threshhold):
        has_raised_axle = True

    return has_raised_axle


def get_axle_inside_bounding_box(bounding_box,axle_data): # both in [x,y,x,y] format

    axles_inside_bounding_box = []

    bounding_box_x_top = bounding_box[0]
    bounding_box_y_top = bounding_box[1]
    bounding_box_x_bot = bounding_box[2]
    bounding_box_y_bot = bounding_box[3] 


    for data in axle_data:
        x_top = int(data[0])
        y_top = int(data[1])

        if(bounding_box_x_top<=x_top and x_top<=bounding_box_x_bot and bounding_box_y_top<=y_top and y_top<=bounding_box_y_bot):
            axles_inside_bounding_box.append([(data[0]+data[2])/2,(data[1]+data[3])/2])
    
    return axles_inside_bounding_box


def contains_raised_axle(result,threshold):

    import numpy

    predicted_boxes = []
    predicted_classes = []
    axles = []
    axles_inside_bounding_box = []

    if len(result[0]) !=0:
        predicted_boxes = result[0].boxes.xyxy.cpu().numpy()
        predicted_classes= result[0].boxes.cls.cpu().numpy()

    for classes in range(len(predicted_classes)):
        if(predicted_classes[classes]==2):
            axles.append(predicted_boxes[classes])

    for classes in range(len(predicted_classes)):
        if(predicted_classes[classes] == 3):
            axles_inside_bounding_box = get_axle_inside_bounding_box(predicted_boxes[classes],axles)

    return predict_raised_axle_perpendicular_dist_approach(axles_inside_bounding_box,threshold)

